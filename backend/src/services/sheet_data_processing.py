import io
import os
import re
import shutil
from pathlib import Path

import pandas as pd
import requests

FILE_URL = os.environ.get('FILE_URL', None)

base_dir = Path(__file__).parent
input_dir = Path(base_dir / 'input')


def start():
    # Criar diretório e baixar o arquivo se não existir
    if os.path.isdir(input_dir) and os.path.isfile(input_dir / 'dados.zip'):
        pass
    else:
        input_dir.mkdir(exist_ok=True)

        if not FILE_URL:
            raise requests.exceptions.InvalidURL(
                'URL para download inválida! Adicione a URL do arquivo em .env'
            )

        response = requests.get(FILE_URL)

        if not response.ok:
            raise Exception('Arquivo não encontrado')

        file = response.content

        # Criar e Descompactar o arquivo
        with open(input_dir / 'dados.zip', 'wb') as f:
            f.write(file)

        shutil.unpack_archive(input_dir / 'dados.zip', input_dir)

    def clean_column_name(name):
        name = str(name).strip()
        acentos = {
            'á': 'a',
            'é': 'e',
            'í': 'i',
            'ó': 'o',
            'ú': 'u',
            'à': 'a',
            'è': 'e',
            'ì': 'i',
            'ò': 'o',
            'ù': 'u',
            'ã': 'a',
            'õ': 'o',
            'â': 'a',
            'ê': 'e',
            'î': 'i',
            'ô': 'o',
            'û': 'u',
            'ç': 'c',
            'Á': 'A',
            'É': 'E',
            'Í': 'I',
            'Ó': 'O',
            'Ú': 'U',
            'À': 'A',
            'È': 'E',
            'Ì': 'I',
            'Ò': 'O',
            'Ù': 'U',
            'Ã': 'A',
            'Õ': 'O',
            'Â': 'A',
            'Ê': 'E',
            'Î': 'I',
            'Ô': 'O',
            'Û': 'U',
            'Ç': 'C',
        }
        for a, n in acentos.items():
            name = name.replace(a, n)
        name = name.upper()
        name = re.sub(r'[^0-9A-Z]+', '_', name)
        return name

    def load_excel(filepath, header_try=[0, 1]):
        for h in header_try:
            try:
                return pd.read_excel(filepath, header=h)
            except Exception as e:
                exc = e
                continue
        raise ValueError(f'Erro ao carregar {filepath}\n Exception: {exc}')

    def load_and_prepare(filepath, origem, header_try=[0, 1]):
        df = load_excel(filepath, header_try=header_try)
        df.columns = [clean_column_name(c) for c in df.columns]
        df['ORIGEM'] = origem
        return df

    # ETAPA 1 - empilhamento principais
    ativos_df = load_and_prepare(os.path.join(input_dir, 'ATIVOS.xlsx'), 'ATIVOS')
    estagio_df = load_and_prepare(os.path.join(input_dir, 'ESTÁGIO.xlsx'), 'ESTAGIO')
    aprendiz_df = load_and_prepare(os.path.join(input_dir, 'APRENDIZ.xlsx'), 'APRENDIZ')

    all_cols = (
        set(ativos_df.columns)
        | set(estagio_df.columns)
        | set(aprendiz_df.columns)
        | {'SINDICATO'}
    )
    for df in [ativos_df, estagio_df, aprendiz_df]:
        for col in all_cols:
            if col not in df.columns:
                df[col] = pd.NA

    consolidado = pd.concat([ativos_df, estagio_df, aprendiz_df], ignore_index=True)

    if 'NA_COMPRA_' in consolidado.columns:
        consolidado = consolidado.drop(columns=['NA_COMPRA_'])

    # Garantir TITULO_DO_CARGO
    if 'TITULO_DO_CARGO' not in consolidado.columns:
        consolidado['TITULO_DO_CARGO'] = ''
    consolidado['TITULO_DO_CARGO'] = consolidado['TITULO_DO_CARGO'].fillna('')

    # ETAPA 2 - enriquecer demais arquivos
    arquivos = [
        f
        for f in os.listdir(input_dir)
        if f.endswith('.xlsx')
        and f.upper()
        not in [
            'ATIVOS.XLSX',
            'ESTÁGIO.XLSX',
            'APRENDIZ.XLSX',
            'VR MENSAL 05.2025.XLSX',
        ]
    ]

    for arquivo in arquivos:
        path = os.path.join(input_dir, arquivo)
        apelido = clean_column_name(os.path.splitext(arquivo)[0])

        if 'BASE_DIAS_UTEIS' in apelido:
            # carregar com header linha 2 (índice 1)
            df = load_excel(path, header_try=[1])
            df.columns = [clean_column_name(c) for c in df.columns]
            # corrigir nome errado da chave
            if 'SINDICADO' in df.columns:
                df = df.rename(columns={'SINDICADO': 'SINDICATO'})
            chave = 'SINDICATO'
            merge_df = df

        elif 'BASE_SINDICATO_X_VALOR' in apelido:
            df = load_and_prepare(path, apelido)
            df = df.drop(columns=['ORIGEM'])
            if 'SINDICADO' in df.columns:
                df = df.rename(columns={'SINDICADO': 'SINDICATO'})

            chave = 'SINDICATO'
            merge_df = df

        elif 'EXTERIOR' in apelido:
            df = load_and_prepare(path, apelido)
            df = df.drop(columns=['ORIGEM'])
            if 'CADASTRO' in df.columns:
                df = df.rename(columns={'CADASTRO': 'MATRICULA'})
            chave = 'MATRICULA'
            merge_df = df

        else:
            df = load_and_prepare(path, apelido)
            df = df.drop(columns=['ORIGEM'])
            chave = 'MATRICULA'
            merge_df = df

        # renomear colunas exceto chave
        new_cols = {}
        for col in merge_df.columns:
            if col != chave:
                new_cols[col] = f'{apelido}_{col}'
        merge_df = merge_df.rename(columns=new_cols)

        # Garante que a coluna da chave esteja no merge_df se for 'SINDICATO'
        if chave == 'SINDICATO' and 'SINDICATO' not in merge_df.columns:
            merge_df['SINDICATO'] = pd.NA

        consolidado = pd.merge(consolidado, merge_df, on=chave, how='outer')

    # ETAPA 3 - salvar csv
    output = io.StringIO()
    consolidado.to_csv(output, sep=',', index=False)
    output.seek(0)

    # Limpar diretório
    for file in input_dir.glob('*'):
        file.unlink()
    input_dir.rmdir()

    return output
