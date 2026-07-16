from app.signals.tld import SuspiciousTldSignal




def test_flags_suspicious_tld():
    signal = SuspiciousTldSignal()
    result = signal.analyze("http://paypa1-secure.tk/login")
    assert result.flagged is True
    assert result.weight == 15


def test_does_not_flag_normal_tld():
    signal = SuspiciousTldSignal()
    result = signal.analyze("https://www.google.com")
    assert result.flagged is False


def test_handles_url_with_path_and_query():
    signal = SuspiciousTldSignal()
    result = signal.analyze("http://example.xyz/some/path?query=1")
    assert result.flagged is True


def test_handles_malformed_url_gracefully():
    signal = SuspiciousTldSignal()
    result = signal.analyze("this-is-a-faake-url")
    assert result.flagged is False