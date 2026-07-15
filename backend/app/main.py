from fastapi import FastAPI



app = FastAPI(
    title='Phishing URL Detector API',
    description='Analyzes URLs for phishing indicators and returns a risk score',
    version='1.0'
)



@app.get('/health')
def health_check():
    '''
    Simple check to confirm the API is running
    '''
    return {'status': 'ok'}