import { useState } from 'react'
import UrlForm from './components/UrlForm.jsx';
import RiskScore from './components/RiskScore.jsx';
import SignalList from './components/SignalList.jsx';
import { analyzeUrl } from './services/api.js';
import './App.css'




function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [apiError, setApiError] = useState('');


  const handleAnalyze = async (url) => {
    setIsLoading(true);
    setApiError('');
    setResult(null);

    try {
      const data = await analyzeUrl(url);
      setResult(data);
    }
    catch (err) {
      setApiError(err)
    }
    finally {
      setIsLoading(false);
    }
  };


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
    </div>
  );
}




export default App;
