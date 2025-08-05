const API_URL = process.env.NEXT_PUBLIC_API_URL;

if (!API_URL) throw new Error('API URL not set');

export async function postResearchQuery(character: string, query: string) {
  const res = await fetch(`${API_URL}/api/research`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ character, query }),
  });
  if (!res.ok) {
    throw new Error(`Failed to submit research: ${res.statusText}`);
  }
  return res.json();
}

export async function getResearchStatus(taskId: string) {
  const res = await fetch(`${API_URL}/api/research/${taskId}/status`);
  if (!res.ok) {
    throw new Error(`Failed to fetch status: ${res.statusText}`);
  }
  return res.json();
}

export async function getResearchResult(taskId: string) {
  const res = await fetch(`${API_URL}/api/research/${taskId}/result`);
  if (!res.ok) {
    throw new Error(`Failed to fetch result: ${res.statusText}`);
  }
  return res.json();
}

export async function sendChatMessage(character: string, message: string) {
  const res = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ character, message }),
  });
  if (!res.ok) {
    throw new Error(`Failed to send chat message: ${res.statusText}`);
  }
  return res.json();
}

// Fetch characters with optional filters for era and type
export const getCharacters = async (filters?: { era?: string; type?: string }) => {
  const params = new URLSearchParams();
  const safeFilters = filters || {};
  if (safeFilters.era) params.append('era', safeFilters.era);
  if (safeFilters.type) params.append('type', safeFilters.type);
  const res = await fetch(`${API_URL}/api/characters?${params.toString()}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch characters: ${res.statusText}`);
  }
  return res.json();
};