import io

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse

from services import file_download, sheet_data_processing

app = FastAPI(docs_url='', redoc_url='')

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/api/upload', status_code=200)
async def upload_file():
    """Realiza o processamento da planilha e retorna o arquivo consolidado"""
    csv_output = sheet_data_processing.start()

    return StreamingResponse(
        io.BytesIO(csv_output.getvalue().encode('utf-8')),
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=consolidado.csv'},
    )


@app.get('/api/check-file')
async def check_file_status():
    """Verifica se o arquivo final foi processado pelo n8n."""
    response = file_download.check_file_response()

    return response


@app.get('/api/download/{file_name}', status_code=200)
async def download_file(file_name: str):
    """Retorna o arquivo para download."""
    file_path = file_download.return_file(file_name)

    if file_path:
        return FileResponse(file_path, filename=file_name)

    raise HTTPException(status_code=404, detail='File not found!')


@app.get('/api/read_file_sample/{file_name}', status_code=200)
async def get_file_sample(file_name: str):
    """Retorna um json do arquivo lido"""
    content = file_download.read_file_sample(file_name)

    if content:
        return content

    raise HTTPException(status_code=404, detail='File not found!')


@app.post('/api/activate')
async def trigger_webhook():
    """Dispara o webhook do n8n."""
    response = file_download.activate_flow()

    if response:
        return response

    raise HTTPException(status_code=500, detail='Signal could not be sent...')
