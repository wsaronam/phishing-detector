import pytest
from app.signals.typosquatting import TyposquattingSignal




@pytest.mark.parametrize('url', [
    'http://paypa1.com/login',
    'http://gooogle.com',
    'http://secure-amaz0n.net/account'
])
async def test_flags_lookalike_domains(url):
    result = await TyposquattingSignal().analyze(url)
    assert result.flagged is True
    assert result.weight == 25


@pytest.mark.parametrize('url', [
    'https://www.paypal.com',
    'https://google.com/search?q=test',
])
async def test_real_brand_domain_is_not_flagged(url):
    result = await TyposquattingSignal().analyze(url)
    assert result.flagged is False


async def test_unrelated_domain_is_not_flagged():
    result = await TyposquattingSignal().analyze('https://wikipedia.org')
    assert result.flagged is False


async def test_malformed_url_is_not_flagged():
    result = await TyposquattingSignal().analyze('not a url')
    assert result.flagged is False
