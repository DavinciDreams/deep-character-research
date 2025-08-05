/**
 * Represents a historical figure available for research and chat.
 */
export interface HistoricalFigure {
  /** Unique identifier for the figure */
  id: number;
  /** Full name of the figure */
  name: string;
  /** Lifespan or years active (e.g., "1452–1519") */
  years: string;
  /** Era or period (e.g., "Renaissance") */
  era: string;
  /** Short description or summary of the figure */
  shortDescription: string;
  /** URL to the figure's portrait image */
  portraitUrl: string;
  /** Array of contemporaries' names */
  contemporaries: string[];
}

/**
 * Represents a single chat message in the chat context.
 */
export interface Message {
  /** Who sent the message: 'user' or 'figure' */
  sender: 'user' | 'figure';
  /** Message text content */
  text: string;
  /** Unix timestamp (ms) when the message was sent */
  timestamp: number;
}

/**
 * Provides chat state and actions to components via context.
 */
export interface ChatContextType {
  /** Array of chat messages */
  messages: Message[];
  /**
   * Send a new message.
   * @param text The message text
   * @param sender 'user' or 'figure'
   */
  sendMessage: (text: string, sender: 'user' | 'figure') => void;
  /** Clear all chat messages */
  clearMessages: () => void;
}

/**
 * Props for the ChatProvider component.
 */
export interface ChatProviderProps {
  /** React children nodes */
  children: React.ReactNode;
}

/**
 * Response from submitting a research query.
 */
export interface ResearchQueryResponse {
  /** Task ID for tracking research progress */
  taskId: string;
}

/**
 * Response for research status polling.
 */
export interface ResearchStatusResponse {
  /** Status string (e.g., "pending", "complete") */
  status: string;
  /** Optional progress percentage (0-100) */
  progress?: number;
}

/**
 * Response containing the result of a completed research task.
 */
export interface ResearchResultResponse {
  /** The research result text */
  result: string;
  /** Optional array of source URLs or citations */
  sources?: string[];
}

/**
 * Response from sending a chat message to a figure.
 */
export interface ChatMessageResponse {
  /** The figure's reply text */
  reply: string;
}

/**
 * Filters for searching historical figures.
 */
export interface CharacterSearchFilters {
  era?: string;
  type?: string;
  profession?: string;
  name?: string;
  keywords?: string;
  field?: string;
}

/**
 * Response from the /api/characters endpoint.
 */
export interface GetCharactersResponse {
  characters: HistoricalFigure[];
}

/**
 * Represents a document associated with a historical figure.
 */
export interface Document {
  id: number;
  character_id: number;
  title: string;
  content: string;
  url: string;
  source_type: string;
  quality_score: number;
  metadata: Record<string, any>;
}

/**
 * Represents a chat history entry.
 */
export interface ChatHistory {
  id: number;
  character_id: number;
  user_message: string;
  character_response: string;
  timestamp: string;
}

/**
 * Represents a user search entry.
 */
export interface UserSearch {
  id: number;
  user_query: string;
  character_id: number;
  search_time: string;
  results_count: number;
}