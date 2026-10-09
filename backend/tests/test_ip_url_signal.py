import pytest
from app.signals.ip_url import IpUrlSignal




async def test_ipv4_url():
    signal = IpUrlSignal()
    result = await signal.analyze("http://192.168.1.1/login")
    assert result.flagged is True
    assert result.weight == 20


async def test_ipv6_url():
    signal = IpUrlSignal()
    result = await signal.analyze("http://[2001:db8::1]/login")
    assert result.flagged is True


async def test_normal_domain():
    signal = IpUrlSignal()
    result = await signal.analyze("https://www.google.com")
    assert result.flagged is False


async def test_domain_containing_numbers():
    signal = IpUrlSignal()
    result = await signal.analyze("https://123movies.com")
    assert result.flagged is False


async def test_malformed_url():
    signal = IpUrlSignal()
    result = await signal.analyze("fake-url")
    assert result.flagged is False
