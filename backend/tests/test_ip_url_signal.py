from app.signals.ip_url import IpUrlSignal




def test_ipv4_url():
    signal = IpUrlSignal()
    result = signal.analyze("http://192.168.1.1/login")
    assert result.flagged is True
    assert result.weight == 20


def test_ipv6_url():
    signal = IpUrlSignal()
    result = signal.analyze("http://[2001:db8::1]/login")
    assert result.flagged is True


def test_normal_domain():
    signal = IpUrlSignal()
    result = signal.analyze("https://www.google.com")
    assert result.flagged is False


def test_domain_containing_numbers():
    signal = IpUrlSignal()
    result = signal.analyze("https://123movies.com")
    assert result.flagged is False


def test_malformed_url():
    signal = IpUrlSignal()
    result = signal.analyze("fake-url")
    assert result.flagged is False