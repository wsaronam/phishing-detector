import pytest
from app.models.schemas import SignalResult
from app.services import scanner
from app.services.scanner import scan_url, _calculate_verdict




class FakeDb:
    '''stands in for a SQLAlchemy session and records what gets saved'''
    def __init__(self):
        self.added = []
        self.committed = False

    def add(self, record):
        self.added.append(record)

    def commit(self):
        self.committed = True


@pytest.fixture
def no_whois(monkeypatch):
    async def fake_domain_age(self, url):
        return SignalResult(name='domain_age', flagged=False, detail='skipped in tests', weight=self.weight)
    monkeypatch.setattr(scanner.DomainAgeSignal, 'analyze', fake_domain_age)


@pytest.mark.parametrize('score, verdict', [
    (0, 'low_risk'), (34, 'low_risk'),
    (35, 'medium_risk'), (69, 'medium_risk'),
    (70, 'high_risk'), (100, 'high_risk'),
])
def test_verdict_thresholds(score, verdict):
    assert _calculate_verdict(score) == verdict


async def test_safe_url_scores_low(no_whois):
    db = FakeDb()
    result = await scan_url('https://www.google.com', db)
    assert result.verdict == 'low_risk'
    assert result.risk_score == 0
    assert len(result.signals) == len(scanner.SIGNALS)


async def test_obvious_phishing_url_scores_higher(no_whois):
    db = FakeDb()
    result = await scan_url('http://paypa1-secure.tk/login', db)
    assert result.risk_score > 0
    flagged = {s.name for s in result.signals if s.flagged}
    assert {'suspicious_tld', 'typosquatting'} <= flagged


async def test_scan_is_saved_to_database(no_whois):
    db = FakeDb()
    await scan_url('https://bit.ly/abc', db)
    assert db.committed is True
    assert len(db.added) == 1
    assert db.added[0].url == 'https://bit.ly/abc'
