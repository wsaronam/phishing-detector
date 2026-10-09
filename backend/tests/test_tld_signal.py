from app.signals.tld import SuspiciousTldSignal




async def test_flags_suspicious_tld():
    signal = SuspiciousTldSignal()
    result = await signal.analyze("http://paypa1-secure.tk/login")
    assert result.flagged is True
    assert result.weight == 15


async def test_does_not_flag_normal_tld():
    signal = SuspiciousTldSignal()
    result = await signal.analyze("https://www.google.com")
    assert result.flagged is False


async def test_handles_url_with_path_and_query():
    signal = SuspiciousTldSignal()
    result = await signal.analyze("http://example.xyz/some/path?query=1")
    assert result.flagged is True


async def test_handles_malformed_url_gracefully():
    signal = SuspiciousTldSignal()
    result = await signal.analyze("this-is-a-faake-url")
    assert result.flagged is False


async def test_tld_check_is_case_insensitive():
    signal = SuspiciousTldSignal()
    result = await signal.analyze("http://EXAMPLE.TK/login")
    assert result.flagged is True