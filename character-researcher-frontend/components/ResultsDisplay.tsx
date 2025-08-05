import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { getResearchResult } from '../services/api';

const ResultsDisplay: React.FC = () => {
  const searchParams = useSearchParams();
  const taskId = searchParams.get('task_id');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<any>(null);

  useEffect(() => {
    if (!taskId) {
      setError('No task ID provided.');
      setLoading(false);
      return;
    }
    getResearchResult(taskId)
      .then(data => setResults(data))
      .catch(err => setError(err.message || 'Failed to fetch results.'))
      .finally(() => setLoading(false));
  }, [taskId]);

  return (
    <section>
      {loading && <p>Loading results...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {!loading && !error && results && (
        <div>
          <h2>Research Results</h2>
          <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
            {JSON.stringify(results, null, 2)}
          </pre>
        </div>
      )}
    </section>
  );
};

export default ResultsDisplay;