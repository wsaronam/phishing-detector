from app.signals.base import Signal
from app.models.schemas import SignalResult
from urllib.parse import urlparse
from datetime import datetime, timezone
import asyncio
import whois




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
        loop = asyncio.get_event_loop()
        result = await asyncio.wait_for(
            loop.run_in_executor(None, whois.whois, hostname),
            timeout=WHOIS_TIMEOUT_SECONDS
        )
        creation_date = result.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0] if creation_date else None

        if creation_date is None:
            return None

        if creation_date.tzinfo is None:
            creation_date = creation_date.replace(tzinfo=timezone.utc)

        return creation_date


    def _unknown_result(self, detail: str) -> SignalResult:
        '''
        Returns non-flagged result when we can't get the age
        '''
        return SignalResult(
            name=self.name,
            flagged=False,
            detail=detail,
            weight=self.weight
        )


    async def analyze(self, url: str) -> SignalResult:
        hostname = urlparse(url).hostname or ''

        if not hostname:
            return self._unknown_result('Could not determine the domain to check')

        try:
            creation_date = await self._lookup_creation_date(hostname)
        except asyncio.TimeoutError:
            return self._unknown_result('WHOIS lookup timed out')
        except Exception:
            return self._unknown_result('WHOIS data unavailable for this domain')

        if creation_date is None:
            return self._unknown_result('WHOIS data unavailable for this domain')

        age_days = (datetime.now(timezone.utc) - creation_date).days 

        if age_days < SUSPICIOUS_AGE_DAYS:
            return SignalResult(
                name=self.name,
                flagged=True,
                detail=f'Domain was registered {age_days} days ago - Younger than {SUSPICIOUS_AGE_DAYS}-day limit',
                weight=self.weight
            )

        return SignalResult(
            name=self.name,
            flagged=False,
            detail=f'Domain was registered {age_days} days ago',
            weight=self.weight
        )