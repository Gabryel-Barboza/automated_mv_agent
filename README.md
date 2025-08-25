# Agente de Automação para VR

* [Sobre o Projeto](https://github.com/Gabryel-Barboza/automated_mv_agent/tree/main?tab=readme-ov-file#-sobre-o-projeto)
* [Instalação e Configuração](https://github.com/Gabryel-Barboza/automated_mv_agent/tree/main?tab=readme-ov-file#%EF%B8%8F-instala%C3%A7%C3%A3o-e-configura%C3%A7%C3%A3o)
* [Configuração do Agente (n8n)](https://github.com/Gabryel-Barboza/automated_mv_agent/tree/main?tab=readme-ov-file#%EF%B8%8F-instala%C3%A7%C3%A3o-e-configura%C3%A7%C3%A3o)
* [Acessando a Interface Web](https://github.com/Gabryel-Barboza/automated_mv_agent/tree/main?tab=readme-ov-file#%EF%B8%8F-acesso-%C3%A0-interface-web)

## 🤖 Sobre o Projeto

O **Agente de Automação para VR** é uma solução que agiliza o processo de cálculo e compra de vales-refeição e alimentação. O projeto automatiza a análise e o tratamento de planilhas com dados de funcionários, calculando os valores de VR/VA para cada um de forma precisa e eficiente.

Este agente autônomo utiliza a API Gemini da Google para interpretar as planilhas e o **n8n** como orquestrador de todo o backend. A interface web, desenvolvida em **Python** (usando o Streamlit), permite que você carregue as planilhas e defina os parâmetros do cálculo.

O projeto ainda está em **desenvolvimento**, mas já é totalmente funcional. Ele serve como uma prova de conceito robusta sobre o potencial da automação assistida por IA para otimizar fluxos de trabalho corporativos, especialmente aqueles que envolvem o tratamento de dados em planilhas.

-----

## ⚙️ Instalação e Configuração

### 🐳 Requisitos

Para rodar o projeto, você precisa ter o **Docker** e o **Docker Compose** instalados na sua máquina.

  * **Windows**: Baixe o Docker Desktop no [site oficial](https://www.docker.com/products/docker-desktop/).
  * **Linux**: Siga as instruções de instalação para sua distribuição no [site do Docker](https://docs.docker.com/engine/install/).

### 📦 Baixando o Projeto

Você pode baixar o projeto de duas maneiras:

#### **Opção 1: Clonando com Git**

Abra o terminal no diretório desejado e execute o seguinte comando:

```bash
git clone https://github.com/Gabryel-Barboza/automated_mv_agent.git
cd automated_mv_agent
```

#### **Opção 2: Baixando o ZIP**

1.  Acesse a [página do projeto no GitHub](https://github.com/Gabryel-Barboza/automated_mv_agent).
2.  Clique no botão verde **`<> Code`**.
3.  Selecione **`Download ZIP`**.
4.  Extraia o arquivo `automated_mv_agent-main.zip` em uma pasta de sua preferência.

### 🚀 Rodando com Docker Compose

**Renomeie o arquivo .env.example para .env antes de continuar!**

Com o Docker instalado e o projeto baixado, navegue até a pasta raiz do projeto no seu terminal e execute o comando adiante, certifique-se de estar vendo o arquivo `compose.yml`. 
* No Windows, você pode abrir o terminal pesquisando por CMD ou abrir a pasta e na barra de endereço digitar CMD e pressionar `ENTER`.
* No Linux, utilize o seu terminal de preferência para navegar até o diretório.

```bash
docker compose up
```

Este comando irá baixar as imagens do Docker e subir os contêineres do n8n e da interface web. Isso pode levar alguns minutos na primeira vez.

-----

## 🤖 Configuração do Agente (n8n)

Após subir o projeto, você precisa configurar o n8n para que o agente funcione corretamente.

1.  Acesse o n8n pelo seu navegador no endpoint: **`http://localhost:5678`**.
2.  **Criação da Conta**: Na primeira vez que acessar, o n8n irá pedir para você criar uma conta de usuário. Preencha os campos e crie seu login.
3.  **Importação do Fluxo**:
      * Clique no ícone de "fluxo" .
      * No canto superior direito, clique em **`New`** e depois em **`Import from File`**.
      * Selecione o arquivo `automated_mv_agent.json`, que está na pasta raiz do projeto que você baixou.
4.  **Criação das Credenciais do Gemini**:
      * Clique no menu **`Credentials`** no canto inferior esquerdo.
      * Clique em **`New Credential`** e procure por **`Gemini`**.
      * Dê um nome à credencial (ex: "n8n_API") e cole sua chave de API do Gemini no campo **`API Key`**. Você pode obter sua chave no [AI Studio da Google](https://aistudio.google.com/app/apikey).

Com o fluxo importado e as credenciais configuradas, o seu agente está pronto para ser ativado.

Para desligar o projeto, no terminal pressione as teclas `CTRL` + `C` e depois digite o comando `docker compose down`, isso estando no mesmo diretório de anteriormente.

-----

## 🖥️ Acesso à Interface Web

### TODO
