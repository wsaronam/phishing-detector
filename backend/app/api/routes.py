from fastapi import APIRouter, Depends
from app.models.schemas import AnalyzeResponse, AnalyzeRequest, ScanHistoryItem
from app.services.scanner import scan_url, get_scan_history, delete_scan
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


@router.delete('/history/{scan_id}', status_code=204)
def delete_scan_record(scan_id: int, db: Session = Depends(get_db)) -> None:
    deleted = delete_scan(db, scan_id)
    if not deleted:
        print(f'Scan {scan_id} not found')