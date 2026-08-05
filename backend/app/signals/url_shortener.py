from app.signals.base import Signal
from app.models.schemas import SignalResult
from urllib.parse import urlparse




# Popular URL shorteners go here
KNOWN_SHORTENERS = {
    "bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly",
    "is.gd", "buff.ly", "rebrand.ly", "cutt.ly", "shorte.st",
    "tiny.cc", "lnkd.in", "rb.gy", "shorturl.at"
}



class UrlShortenerSignal(Signal):
    name = 'url_shortener'
    weight = 10

    
    async def analyze(self, url: str) -> SignalResult:
        hostname = (urlparse(url).hostname or '').lower()

        if hostname in KNOWN_SHORTENERS:
            return SignalResult(
                name=self.name,
                flagged=True,
                detail=f'URL uses a link shortener ({hostname}), which hides the real destination',
                weight = self.weight
            )
        
        return SignalResult(
            name=self.name,
            flagged=False,
            detail='URL does not use a known link shortener',
            weight=self.weight
        )