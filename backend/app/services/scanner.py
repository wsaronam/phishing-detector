from app.signals.tld import SuspiciousTldSignal
from app.signals.ip_url import IpUrlSignal
from app.signals.typosquatting import TyposquattingSignal
from app.signals.url_shortener import UrlShortenerSignal
from app.signals.domain_age import DomainAgeSignal
from app.models.schemas import AnalyzeResponse, SignalResult
from app.signals.base import Signal
from sqlalchemy.orm import Session
from app.models.db_models import ScanRecord




# List of all created signals go here.
# Add new signals here
SIGNALS: list[Signal] = [
    SuspiciousTldSignal(),
    IpUrlSignal(),
    TyposquattingSignal(),
    UrlShortenerSignal(),
    DomainAgeSignal()
]


# Use to normalize the score to account for all signals and all new signals
MAX_POSSIBLE_SCORE = sum(signal.weight for signal in SIGNALS)



def _calculate_verdict(score: int) -> str:
    if score >= 70:
        return 'high_risk'
    if score >= 35:
        return 'medium_risk'
    return 'low_risk'


async def scan_url(url: str, db: Session) -> AnalyzeResponse:
    '''
    Runs all signals against the URL to get the results
    Saves and returns results too
    '''
    results: list[SignalResult] = [await signal.analyze(url) for signal in SIGNALS]

    raw_score = sum(result.weight for result in results if result.flagged)
    normalized_score = round((raw_score / MAX_POSSIBLE_SCORE) * 100) if MAX_POSSIBLE_SCORE else 0
    verdict = _calculate_verdict(normalized_score)

    record = ScanRecord(
        url=url,
        risk_score=normalized_score,
        verdict=verdict,
        signals=[result.model_dump() for result in results]
    )
    db.add(record)
    db.commit()

    return AnalyzeResponse(
        url=url,
        risk_score=normalized_score,
        verdict=verdict,
        signals=results
    )


def get_scan_history(db: Session, limit: int = 20) -> list[ScanRecord]:
    '''
    Returns the most recent scans sorted by the newest first
    '''
    return (
        db.query(ScanRecord)
        .order_by(ScanRecord.scanned_at.desc())
        .limit(limit)
        .all()
    )