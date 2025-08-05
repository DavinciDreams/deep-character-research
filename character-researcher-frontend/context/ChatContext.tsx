import React, { createContext, useContext, useState } from 'react';
import { Message, ChatContextType, ChatProviderProps } from '../types/types';

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};


export const ChatProvider: React.FC<ChatProviderProps> = ({ children }) => {
  const [messages, setMessages] = useState<Message[]>([]);

  const sendMessage = (text: string, sender: 'user' | 'figure') => {
    const newMessage: Message = {
      sender,
      text,
      timestamp: Date.now(),
    };
    
    setMessages(prevMessages => [...prevMessages, newMessage]);
  };

  const clearMessages = () => {
    setMessages([]);
  };

  return (
    <ChatContext.Provider value={{ messages, sendMessage, clearMessages }}>
      {children}
    </ChatContext.Provider>
  );
};