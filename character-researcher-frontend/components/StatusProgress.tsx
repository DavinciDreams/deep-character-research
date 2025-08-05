import React, { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { getResearchStatus } from '../services/api';

const POLL_INTERVAL = 2000;

const StatusProgress: React.FC = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const taskId = searchParams.get('task_id');
  const [status, setStatus] = useState<string>('pending');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!taskId) {
      setError('No task ID provided.');
      return;
    }
    let cancelled = false;
    let interval: NodeJS.Timeout;

    const poll = async () => {
      try {
        const data = await getResearchStatus(taskId);
        if (!cancelled) {
          setStatus(data.status);
          if (data.status === 'complete') {
            router.push(`/results?task_id=${encodeURIComponent(taskId)}`);
          }
        }
      } catch (err: any) {
        if (!cancelled) setError(err.message || 'Failed to fetch status.');
      }
    };

    poll();
    interval = setInterval(poll, POLL_INTERVAL);

    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, [taskId, router]);

  if (error) {
    return <aside><p style={{ color: 'red' }}>Error: {error}</p></aside>;
  }

  return (
    <aside>
      <p>Status: {status === 'pending' ? 'Processing...' : status}</p>
      {status === 'pending' && <p>Polling for completion...</p>}
    </aside>
  );
};

export default StatusProgress;