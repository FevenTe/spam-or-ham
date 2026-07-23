import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCheck = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/predict-spam', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      
      // ADD THIS LINE TO DEBUG:
      console.log("Backend Response:", data);

      setResult(data);
    } catch (error) {
      console.error('Error connecting to backend:', error);
      setResult({ prediction: 'Error connecting to server' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="card">
        <div className="first">
          <h1>SMS Spam Detector</h1>
          <p className="subtitle">Enter a text message below to find out its classification.</p>
        </div>
        <form onSubmit={handleCheck}>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type or paste your message here..."
            rows={4}
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Analyzing...' : 'Check Message'}
          </button>
        </form>

        {result && (
          <div className={`result-box ${result.prediction === 'Spam' ? 'spam' : 'safe'}`}>
            <h3>Result: <span>{result.prediction}</span></h3>

            {result.model_name && (
              <div className="metrics-row">
                <div className="metric-box">
                  <span>Model</span>
                  <strong>{result.model_name}</strong>
                </div>
                <div className="metric-box">
                  <span>F1-Score</span>
                  <strong>{result.f1_score}</strong>
                </div>
                <div className="metric-box">
                  <span>Vectorizer</span>
                  <strong>{result.vectorizer}</strong>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;