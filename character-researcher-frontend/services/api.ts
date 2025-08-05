import {
  ResearchQueryResponse,
  ResearchStatusResponse,
  ResearchResultResponse,
  ChatMessageResponse,
  GetCharactersResponse,
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
  filters?: { era?: string; type?: string; profession?: string }
): Promise<GetCharactersResponse> => {
  const params = new URLSearchParams();
  const safeFilters = filters || {};
  if (safeFilters.era) params.append('era', safeFilters.era);
  if (safeFilters.type) params.append('type', safeFilters.type);
  if (safeFilters.profession) params.append('profession', safeFilters.profession);
  const res = await fetch(`${API_URL}/api/characters?${params.toString()}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch characters: ${res.statusText}`);
  }
  return res.json() as Promise<GetCharactersResponse>;
};