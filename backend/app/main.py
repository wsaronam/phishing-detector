from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(
    title='Phishing URL Detector API',
    description='Analyzes URLs for phishing indicators and returns a risk score',
    version='1.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(router, prefix='/api')



@app.get('/health')
def health_check():
    '''
    Simple check to confirm the API is running
    '''
    return {'status': 'ok'}