from app.signals.base import Signal
from app.models.schemas import SignalResult
from urllib.parse import urlparse
from datetime import datetime
import asyncio




# Domains that are younger than this parameter are considered suspicious
SUSPICIOUS_AGE_DAYS = 90

# Timeout for WHOIS server's response
WHOIS_TIMEOUT_SECONDS = 5




class DomainAgeSignal(Signal):
    name='domain_age'
    weight = 20


    async def _lookup_creation_date(self, hostname: str) -> datetime | None:
        '''
        Lookup WHOIS in the background with a timeout        
        '''
        pass


    async def analyze(self, url: str) -> SignalResult:
        hostname = urlparse(url).hostname or ''

        if not hostname:
            return SignalResult(
                name=self.name,
                flagged=False,
                detail=f'Could not determine the domain to check',
                weight=self.weight
            )

        try:
            creation_date = await self._lookup_creation_date(hostname)
        except asyncio.TimeoutError:
            return SignalResult(
                name=self.name,
                flagged=False,
                detail=f'WHOIS lookup timed out',
                weight=self.weight
            )
        except:
            return SignalResult(
                name=self.name,
                flagged=False,
                detail=f'WHOIS data unavailable for this domain',
                weight=self.weight
            )

        if creation_date is None:
            return SignalResult(
                name=self.name,
                flagged=False,
                detail=f'WHOIS data unavailable for this domain',
                weight=self.weight
            )