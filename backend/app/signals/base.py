from abc import ABC, abstractmethod
from app.models.schemas import SignalResult




class Signal(ABC):
    '''
    Base class to be implemented by detection signals

    A 'Signal' is an independent check run against URL
        such as TLD, IP URLs, or typosquaating
    '''
    name: str = 'base_signal'
    weight: int = 0
    

    @abstractmethod
    def analyze(self, url: str) -> SignalResult:
        '''
        Run this check against URL

        Return a SignalResult regardless of flag result
        '''
        raise NotImplementedError