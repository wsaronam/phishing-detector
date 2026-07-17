from app.signals.base import Signal
from app.models.schemas import SignalResult
from urllib.parse import urlparse




# Use this to update brands that are commonly impersonated.
# Add more to this list here
# Maybe we can make this into a config file in the future
COMMONLY_IMPERSONATED_BRANDS = {
    "paypal", "google", "microsoft", "amazon", "apple", "facebook",
    "netflix", "instagram", "linkedin", "bankofamerica", "wellsfargo",
    "chase", "dropbox", "adobe", "ebay"
}



class TyposquattingSignal(Signal):
    name = 'typosquatting'
    weight = 25


    @staticmethod
    def _extract_root_domain(hostname: str) -> str:
        '''
        Gets the "core" domain name, for example, 'www.paypal.com' -> 'paypal'
        '''
        if not hostname:
            return ''
        parts = hostname.split('.')
        if len(parts) < 2:
            return hostname.lower()
        return parts[-2].lower()


    def analyze(self, url: str) -> SignalResult:
        hostname = urlparse(url).hostname or ''
        domain_root = self._extract_root_domain(hostname)

        if not domain_root:
            return SignalResult(
                name=self.name,
                flagged=False,
                detail='Could not determine a domain to check',
                weight=self.weight
            )
        
        if domain_root in COMMONLY_IMPERSONATED_BRANDS:
            return SignalResult(
                name=self.name,
                flagged=False,
                detail=f'Domain matches known brand \'{domain_root}\'',
                weight=self.weight
            )
        

        #CHECK FOR BRAND IMPERSONATION HERE


        return SignalResult(
            name=self.name,
            flagged=False,
            detail='Domain does not closely resemble any known brand listed here',
            weight=self.weight
        )