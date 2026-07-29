import { useState } from 'react'
import UrlForm from './components/UrlForm.jsx';
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
        <pre className='result-debug'>
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}




export default App;
