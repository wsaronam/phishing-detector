from app.signals.base import Signal
from app.models.schemas import SignalResult
from urllib.parse import urlparse
from rapidfuzz.distance import Levenshtein




# Use this to update brands that are commonly impersonated.
# Add more to this list here
# Maybe we can make this into a config file in the future
COMMONLY_IMPERSONATED_BRANDS = {
    "paypal", "google", "microsoft", "amazon", "apple", "facebook",
    "netflix", "instagram", "linkedin", "bankofamerica", "wellsfargo",
    "chase", "dropbox", "adobe", "ebay"
}


# Use this to choose how close a domain must be in order to be considered 
# suspicious
MAX_SUSPICIOUS_DISTANCE = 2



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


    @staticmethod
    def _split_into_chunks(domain_root: str) -> list[str]:
        '''
        Splits domain root into chunks to check them individually later
        '''
        chunks = [domain_root]
        if '-' in domain_root:
            chunks.extend(chunk for chunk in domain_root.split('-') if chunk)
        return chunks


    def _closest_brand_match(self, domain_root: str) -> tuple[str | None, int]:
        '''
        Finds known brand with smallest distance to the domain_root
        '''
        if not COMMONLY_IMPERSONATED_BRANDS:
            return None, 999

        closest = min(
            COMMONLY_IMPERSONATED_BRANDS,
            key=lambda brand: Levenshtein.distance(domain_root, brand)
        )

        return closest, Levenshtein.distance(domain_root, closest)


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

        chunks = self._split_into_chunks(domain_root)
        best_match = None
        best_distance = None

        for chunk in chunks:
            closest_brand, distance = self._closest_brand_match(chunk)
            if closest_brand and (best_distance is None or distance < best_distance):
                best_match, best_distance = closest_brand, distance

        if best_match is not None and 0 <= best_distance <= MAX_SUSPICIOUS_DISTANCE:
            return SignalResult(
                name=self.name,
                flagged=True,
                detail=f'Domain \'{domain_root}\' closesly resembles known brand \'{best_match}\''
                       f'(edit distance: {best_distance})',
                weight=self.weight
            )

        return SignalResult(
            name=self.name,
            flagged=False,
            detail='Domain does not closely resemble any known brand listed here',
            weight=self.weight
        )