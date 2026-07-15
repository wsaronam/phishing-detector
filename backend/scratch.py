from app.models.schemas import SignalResult, AnalyzeRequest, AnalyzeResponse




req = AnalyzeRequest(url='http://paypa1-secure.tk/login')
print(req)

resp = AnalyzeResponse(
    url=req.url, 
    risk_score=87, 
    verdict='high_risk', 
    signals=[SignalResult(name="suspicious_tld", flagged=True, detail=".tk domain", weight=15)]
)
print(resp.model_dump_json(indent=2))