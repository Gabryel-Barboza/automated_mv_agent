import io

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from services import sheet_data_processing

app = FastAPI(docs_url='', redoc_url='')


@app.get('/api/upload', status_code=200)
async def upload_file():
    csv_output = sheet_data_processing.start()

    return StreamingResponse(
        io.BytesIO(csv_output.getvalue().encode('utf-8')),
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=consolidado.csv'},
    )
