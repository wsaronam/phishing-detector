from app.signals.base import Signal
from app.models.schemas import SignalResult
from urllib.parse import urlparse




# Popular TLDs used for phishing or spams.
# Add more here
SUSPICIOUS_TLDS = {
    'tk', "ml", "ga", "cf", "gq", "top", "xyz", "work", "click", 
    "link", "buzz", "surf", "rest", "loan", "gdn"
}



class SuspiciousTldSignal(Signal):
    name = 'suspicious_tld'
    weight = 15


    def analyze(self, url: str) -> SignalResult:
        hostname = urlparse(url).hostname or ''
        tld = hostname.rsplit('.', 1)[-1].lower() if '.' in hostname else ''

        if tld in SUSPICIOUS_TLDS:
            return SignalResult(
                name=self.name,
                flagged=True,
                detail=f'Domain uses a commonly-abused TLD for phishing/spam: .{tld}',
                weight=self.weight
            )
        
        return SignalResult(
            name=self.name,
            flagged=False,
            detail=f'TLD .{tld} is not on the suspicious list' if tld else 'Could not determine TLD',
            weight=self.weight
        )