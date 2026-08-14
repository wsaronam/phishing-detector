from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db




app = FastAPI(
    title='Phishing URL Detector API',
    description='Analyzes URLs for phishing indicators and returns a risk score',
    version='1.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   'phishing-detector-80290sc21-wsaronam1.vercel.app'
                    ],
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(router, prefix='/api')



@app.on_event('startup')
def on_startup():
    init_db()
    

@app.get('/health')
def health_check():
    '''
    Simple check to confirm the API is running
    '''
    return {'status': 'ok'}