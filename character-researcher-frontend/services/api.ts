import {
  ResearchQueryResponse,
  ResearchStatusResponse,
  ResearchResultResponse,
  ChatMessageResponse,
  GetCharactersResponse,
  CharacterSearchFilters,
  Document,
  ChatHistory,
  UserSearch,
} from '../types/types';

/**
 * Base URL for API requests, set via environment variable.
 */
const API_URL = process.env.NEXT_PUBLIC_API_URL;

if (!API_URL) throw new Error('API URL not set');

/**
 * Submit a research query for a given character.
 * @param character The character's name
 * @param query The research question
 * @returns ResearchQueryResponse with a taskId
 */
export async function postResearchQuery(
  character: string,
  query: string
): Promise<ResearchQueryResponse> {
  const res = await fetch(`${API_URL}/api/research`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ character, query }),
  });
  if (!res.ok) {
    throw new Error(`Failed to submit research: ${res.statusText}`);
  }
  return res.json() as Promise<ResearchQueryResponse>;
}

/**
 * Get the status of a research task.
 * @param taskId The ID of the research task
 * @returns ResearchStatusResponse with status and progress
 */
export async function getResearchStatus(
  taskId: string
): Promise<ResearchStatusResponse> {
  const res = await fetch(`${API_URL}/api/research/${taskId}/status`);
  if (!res.ok) {
    throw new Error(`Failed to fetch status: ${res.statusText}`);
  }
  return res.json() as Promise<ResearchStatusResponse>;
}

/**
 * Get the result of a completed research task.
 * @param taskId The ID of the research task
 * @returns ResearchResultResponse with result and sources
 */
export async function getResearchResult(
  taskId: string
): Promise<ResearchResultResponse> {
  const res = await fetch(`${API_URL}/api/research/${taskId}/result`);
  if (!res.ok) {
    throw new Error(`Failed to fetch result: ${res.statusText}`);
  }
  return res.json() as Promise<ResearchResultResponse>;
}

/**
 * Send a chat message to a character.
 * @param character The character's name
 * @param message The user's message
 * @returns ChatMessageResponse with the character's reply
 */
export async function sendChatMessage(
  character: string,
  message: string
): Promise<ChatMessageResponse> {
  const res = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ character, message }),
  });
  if (!res.ok) {
    throw new Error(`Failed to send chat message: ${res.statusText}`);
  }
  return res.json() as Promise<ChatMessageResponse>;
}

/**
 * Fetch a list of historical figures, optionally filtered by era and type.
 * @param filters Optional filters for era and type
 * @returns Array of HistoricalFigure objects
 */
export const getCharacters = async (
  filters?: CharacterSearchFilters
): Promise<GetCharactersResponse> => {
  const params = new URLSearchParams();
  const safeFilters = filters || {};
  if (safeFilters.era) params.append('era', safeFilters.era);
  if (safeFilters.type) params.append('type', safeFilters.type);
  if (safeFilters.profession) params.append('profession', safeFilters.profession);
  if (safeFilters.name) params.append('name', safeFilters.name);
  if (safeFilters.keywords) params.append('keywords', safeFilters.keywords);
  if (safeFilters.field) params.append('field', safeFilters.field);
  const res = await fetch(`${API_URL}/api/characters?${params.toString()}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch characters: ${res.statusText}`);
  }
  return res.json() as Promise<GetCharactersResponse>;
};

/**
 * --- CRUD for Historical Figures ---
 */
export async function createCharacter(name: string): Promise<HistoricalFigure> {
  const res = await fetch(`${API_URL}/api/characters`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name }),
  });
  if (!res.ok) throw new Error(`Failed to create character: ${res.statusText}`);
  return res.json() as Promise<HistoricalFigure>;
}

export async function getCharacter(id: number): Promise<HistoricalFigure> {
  const res = await fetch(`${API_URL}/api/characters/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch character: ${res.statusText}`);
  return res.json() as Promise<HistoricalFigure>;
}

export async function updateCharacter(id: number, name: string): Promise<HistoricalFigure> {
  const res = await fetch(`${API_URL}/api/characters/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name }),
  });
  if (!res.ok) throw new Error(`Failed to update character: ${res.statusText}`);
  return res.json() as Promise<HistoricalFigure>;
}

export async function deleteCharacter(id: number): Promise<void> {
  const res = await fetch(`${API_URL}/api/characters/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error(`Failed to delete character: ${res.statusText}`);
}

/**
 * --- CRUD for Documents ---
 */
export async function createDocument(doc: Omit<Document, 'id'>): Promise<Document> {
  const res = await fetch(`${API_URL}/api/documents`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(doc),
  });
  if (!res.ok) throw new Error(`Failed to create document: ${res.statusText}`);
  return res.json() as Promise<Document>;
}

export async function getDocument(id: number): Promise<Document> {
  const res = await fetch(`${API_URL}/api/documents/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch document: ${res.statusText}`);
  return res.json() as Promise<Document>;
}

export async function updateDocument(id: number, doc: Partial<Document>): Promise<Document> {
  const res = await fetch(`${API_URL}/api/documents/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(doc),
  });
  if (!res.ok) throw new Error(`Failed to update document: ${res.statusText}`);
  return res.json() as Promise<Document>;
}

export async function deleteDocument(id: number): Promise<void> {
  const res = await fetch(`${API_URL}/api/documents/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error(`Failed to delete document: ${res.statusText}`);
}

/**
 * --- CRUD for Chat History ---
 */
export async function createChatHistory(entry: Omit<ChatHistory, 'id' | 'timestamp'>): Promise<ChatHistory> {
  const res = await fetch(`${API_URL}/api/chat_history`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(entry),
  });
  if (!res.ok) throw new Error(`Failed to create chat history: ${res.statusText}`);
  return res.json() as Promise<ChatHistory>;
}

export async function getChatHistory(id: number): Promise<ChatHistory> {
  const res = await fetch(`${API_URL}/api/chat_history/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch chat history: ${res.statusText}`);
  return res.json() as Promise<ChatHistory>;
}

export async function deleteChatHistory(id: number): Promise<void> {
  const res = await fetch(`${API_URL}/api/chat_history/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error(`Failed to delete chat history: ${res.statusText}`);
}

/**
 * --- CRUD for User Searches ---
 */
export async function createUserSearch(entry: Omit<UserSearch, 'id' | 'search_time'>): Promise<UserSearch> {
  const res = await fetch(`${API_URL}/api/user_searches`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(entry),
  });
  if (!res.ok) throw new Error(`Failed to create user search: ${res.statusText}`);
  return res.json() as Promise<UserSearch>;
}

export async function getUserSearch(id: number): Promise<UserSearch> {
  const res = await fetch(`${API_URL}/api/user_searches/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch user search: ${res.statusText}`);
  return res.json() as Promise<UserSearch>;
}

export async function deleteUserSearch(id: number): Promise<void> {
  const res = await fetch(`${API_URL}/api/user_searches/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error(`Failed to delete user search: ${res.statusText}`);
}