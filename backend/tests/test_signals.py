import pytest
from pydantic import ValidationError
from app.models.schemas import SignalResult, AnalyzeRequest, AnalyzeResponse




def test_analyze_request_accepts_url():
    req = AnalyzeRequest(url='http://paypa1-secure.tk/login')
    assert req.url == 'http://paypa1-secure.tk/login'


def test_analyze_response_round_trips_to_json():
    resp = AnalyzeResponse(
        url='http://paypa1-secure.tk/login',
        risk_score=87,
        verdict='high_risk',
        signals=[SignalResult(name='suspicious_tld', flagged=True, detail='.tk domain', weight=15)]
    )
    data = resp.model_dump()
    assert data['risk_score'] == 87
    assert data['signals'][0]['name'] == 'suspicious_tld'


@pytest.mark.parametrize('bad_score', [-1, 101])
def test_risk_score_must_be_0_to_100(bad_score):
    with pytest.raises(ValidationError):
        AnalyzeResponse(url='http://x.com', risk_score=bad_score, verdict='low_risk', signals=[])


def test_verdict_must_be_a_known_value():
    with pytest.raises(ValidationError):
        AnalyzeResponse(url='http://x.com', risk_score=10, verdict='totally_fine', signals=[])
