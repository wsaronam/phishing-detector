from app.signals.url_shortener import UrlShortenerSignal




async def test_flags_known_shortener():
    result = await UrlShortenerSignal().analyze('https://bit.ly/3abcXYZ')
    assert result.flagged is True
    assert result.weight == 10


async def test_shortener_check_is_case_insensitive():
    result = await UrlShortenerSignal().analyze('https://TinyURL.com/abc')
    assert result.flagged is True


async def test_normal_domain_is_not_flagged():
    result = await UrlShortenerSignal().analyze('https://www.github.com')
    assert result.flagged is False
