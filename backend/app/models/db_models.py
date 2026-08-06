from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func




class ScanRecord(Base):
    '''
    Database table storing URL scan history
    '''
    __tablename__ = 'scan_records'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False, index=True)
    risk_score = Column(Integer, nullable=False)
    verdict = Column(String, nullable=False)
    signals = Column(JSON, nullable=False)
    scanned_at = Column(DateTime(timezone=True), server_default=func.now())