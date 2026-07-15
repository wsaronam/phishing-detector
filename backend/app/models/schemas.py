from pydantic import BaseModel, Field
from typing import Literal




class SignalResult(BaseModel):
    '''
    Result from a detection signal (ex. typosquatting)
    '''
    name: str = Field(..., description='Identifier for the signal ex. \'suspicious_tld\'')
    flagged: bool = Field(..., description='If this signal is a red flag')
    detail: str = Field(..., description='Explanation of the result')
    weight: int = Field(..., description='Points of this signal that contribute to the risk score if flagged')



class AnalyzeRequest(BaseModel):
    '''
    Request body for the /analyze endpoint
    '''
    url: str = Field(..., description='The URL to be analyzed', examples=['http://paypa1-secure.tk/login'])



class AnalyzeResponse(BaseModel):
    '''
    Response body for the /analyze endpoint
    '''
    url: str
    risk_score: int = Field(..., ge=0, le=100, description='Overall risk score from 0-100')
    verdict: Literal['low_risk', 'medium_risk', 'high_risk']
    signals: list[SignalResult]