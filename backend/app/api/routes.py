from fastapi import APIRouter
from app.models.schemas import AnalyzeResponse, AnalyzeRequest
from app.services.scanner import scan_url



router = APIRouter()


@router.post('/analyze', response_model=AnalyzeResponse)
async def analyze_url(request: AnalyzeRequest) -> AnalyzeResponse:
    return await scan_url(request.url)