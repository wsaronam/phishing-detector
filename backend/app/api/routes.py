from fastapi import APIRouter, Depends
from app.models.schemas import AnalyzeResponse, AnalyzeRequest, ScanHistoryItem
from app.services.scanner import scan_url, get_scan_history
from app.database import get_db
from sqlalchemy.orm import Session



router = APIRouter()


@router.post('/analyze', response_model=AnalyzeResponse)
async def analyze_url(request: AnalyzeRequest, db: Session = Depends(get_db)) -> AnalyzeResponse:
    return await scan_url(request.url, db)


# depends will call get_db everytime a request needs it
@router.get('/history', response_model=list[ScanHistoryItem])
def scan_history(db: Session = Depends(get_db)) -> list[ScanHistoryItem]:
    return get_scan_history(db)