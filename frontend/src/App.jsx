import { useState, useEffect } from 'react'
import UrlForm from './components/UrlForm.jsx';
import RiskScore from './components/RiskScore.jsx';
import SignalList from './components/SignalList.jsx';
import HistoryList from './components/HistoryList.jsx';
import { analyzeUrl, getScanHistory, deleteScan } from './services/api.js';
import './App.css'




function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [apiError, setApiError] = useState('');
  const [history, setHistory] = useState([]);
  const [isHistoryLoading, setIsHistoryLoading] = useState(true);


  useEffect(() => {
    loadHistory();
  }, [])
  

  const handleAnalyze = async (url) => {
    setIsLoading(true);
    setApiError('');
    setResult(null);

    try {
      const data = await analyzeUrl(url);
      setResult(data);
      loadHistory();
    }
    catch (err) {
      setApiError(err)
    }
    finally {
      setIsLoading(false);
    }
  };


  const loadHistory = async () => {
    setIsHistoryLoading(true);
    try {
      const data = await getScanHistory();
      setHistory(data);
    }
    catch (err) {
      console.error('Failed to load history: ' + err);
    }
    finally {
      setIsHistoryLoading(false);
    }
  }


  const handleSelectHistoryItem = (item) => {
    // reuses results from past scans so we don't have to re-run the scan
    setResult(item);
    setApiError('');
  }


  const handleDeleteHistoryItem = async (scanId) => {
    try {
      await deleteScan(scanId);
      setHistory((prev) => prev.filter((item) => item.id !== scanId));
    }
    catch (err) {
      console.error('Failed to delete scan: ' + err);
    }
  }


  return (
    <div className='app-container'>
      <h1>Phishing URL Detector</h1>
      <UrlForm onSubmit={handleAnalyze} isLoading={isLoading} />

      {apiError && <p className='api-error'>{apiError}</p>}

      {result && (
        <div className='results'>
          <RiskScore score={result.risk_score} verdict={result.verdict} />
          <SignalList signals={result.signals} />
        </div>
      )}

      <div className='history-section'>
        <h2>Recent Scans</h2>
        <HistoryList 
          history={history}
          isLoading={isHistoryLoading}
          onSelect={handleSelectHistoryItem}
          onDelete={handleDeleteHistoryItem}
        />
      </div>
    </div>
  );
}




export default App;
