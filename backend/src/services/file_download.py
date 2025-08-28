import os
from datetime import datetime

import requests

WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL', 'http://n8n:5678/webhook/activate')
DOWNLOAD_DIR = '/app/downloads'

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


def check_file_response():
    try:
        response = requests.get(f'{WEBHOOK_URL}/status')
        response.raise_for_status()
        data = response.json()
        if 'file' in data:
            file_data = data['file']
            file_name = f'output_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            file_path = os.path.join(DOWNLOAD_DIR, file_name)
            with open(file_path, 'wb') as f:
                f.write(file_data)
            return {'status': 'success', 'file_path': file_path, 'file_name': file_name}
        return {'status': 'pending', 'message': 'Aguardando arquivo do n8n...'}
    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'message': f'Erro ao verificar arquivo: {str(e)}'}


def activate_flow():
    try:
        response = requests.post(WEBHOOK_URL)
        response.raise_for_status()
        
        return {"status": "success", "message": "Sinal de ativação enviado com sucesso!"}
    except requests.exceptions.RequestException:
        return None


def return_file(file_name: str):
    file_path = os.path.join(DOWNLOAD_DIR, file_name)

    if os.path.exists(file_path):
        return file_path
