import ipaddress
from urllib.parse import urlparse
from app.signals.base import Signal
from app.models.schemas import SignalResult




class IpUrlSignal(Signal):
    name = 'ip_based_url'
    weight = 20


    @staticmethod
    def _is_ip_address(hostname: str) -> bool:
        '''
        '''
        try:
            ipaddress.ip_address(hostname)
            return True
        except ValueError:
            return False

    
    def analyze(self, url: str) -> SignalResult:
        hostname = urlparse(url).hostname or ''

        if self._is_ip_address(hostname):
            return SignalResult(
                name=self.name,
                flagged=True,
                detail=f'URL uses a IP address ({hostname}) instead of a domain name',
                weight=self.weight
            )

        return SignalResult(
            name=self.name,
            flagged=False,
            detail="URL uses a domain name, not a IP address",
            weight=self.weight,
        )