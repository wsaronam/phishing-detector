from app.signals.tld import SuspiciousTldSignal
from app.signals.ip_url import IpUrlSignal
from app.signals.typosquatting import TyposquattingSignal
from app.models.schemas import AnalyzeResponse, SignalResult
from app.signals.base import Signal




# List of all created signals go here.
# Add new signals here
SIGNALS: list[Signal] = [
    SuspiciousTldSignal(),
    IpUrlSignal(),
    TyposquattingSignal()
]


# Use to normalize the score to account for all signals and all new signals
MAX_POSSIBLE_SCORE = sum(signal.weight for signal in SIGNALS)



def _calculate_verdict(score: int) -> str:
    if score >= 70:
        return 'high_risk'
    if score >= 35:
        return 'medium_risk'
    return 'low_risk'


def scan_url(url: str) -> AnalyzeResponse:
    '''
    Runs all signals against the URL to get the results
    '''
    results: list[SignalResult] = [signal.analyze(url) for signal in SIGNALS]

    raw_score = sum(result.weight for result in results if result.flagged)
    normalized_score = round((raw_score / MAX_POSSIBLE_SCORE) * 100) if MAX_POSSIBLE_SCORE else 0

    return AnalyzeResponse(
        url=url,
        risk_score=normalized_score,
        verdict=_calculate_verdict(normalized_score),
        signals=results
    )