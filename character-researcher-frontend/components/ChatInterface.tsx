import React, { useState, useRef, useEffect } from 'react';
import { ArrowLeft, Send } from 'lucide-react';
import { HistoricalFigure } from '../types/types';
import { useChat } from '../context/ChatContext';

interface ChatInterfaceProps {
  figure: HistoricalFigure;
  onReturn: () => void;
  portalActive: boolean;
  soundEnabled: boolean;
}

const ChatInterface: React.FC<ChatInterfaceProps> = React.memo(({
  figure,
  onReturn,
  portalActive,
  soundEnabled
}) => {
  const [message, setMessage] = useState('');
  const { messages, sendMessage } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatInputRef = useRef<HTMLInputElement>(null);
  const messageSoundRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  useEffect(() => {
    if (portalActive && chatInputRef.current) {
      setTimeout(() => {
        chatInputRef.current?.focus();
      }, 1000);
    }
  }, [portalActive]);

  const handleSendMessage = React.useCallback(() => {
    if (message.trim() === '') return;

    if (soundEnabled && messageSoundRef.current) {
      messageSoundRef.current.volume = 0.2;
      messageSoundRef.current.currentTime = 0;
      messageSoundRef.current.play().catch(e => console.log('Audio playback prevented:', e));
    }

    sendMessage(message.trim(), 'user');

    setTimeout(() => {
      const responses = [
        `As ${figure.name}, I find your question intriguing. In my time, we would have approached this differently.`,
        `Indeed, this reminds me of my experiences in ${figure.era}.`,
        `If I were to consider this from my perspective in ${figure.years}, I would say...`,
        `How fascinating! This concept would have been quite revolutionary during my lifetime.`,
        `I must say, the advancements of your era are remarkable compared to my time in ${figure.era}.`
      ];

      const randomResponse = responses[Math.floor(Math.random() * responses.length)];

      if (soundEnabled && messageSoundRef.current) {
        messageSoundRef.current.volume = 0.2;
        messageSoundRef.current.currentTime = 0;
        messageSoundRef.current.play().catch(e => console.log('Audio playback prevented:', e));
      }

      sendMessage(randomResponse, 'figure');
    }, 1500);

    setMessage('');
  }, [message, soundEnabled, sendMessage, figure.name, figure.era, figure.years]);

  const handleKeyDown = React.useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  }, [handleSendMessage]);

  return (
    <div className={`chat-interface ${portalActive ? 'active' : ''}`}>
      {soundEnabled && (
        <audio ref={messageSoundRef} preload="auto">
          <source src="https://assets.mixkit.co/active_storage/sfx/209/209-preview.mp3" type="audio/mpeg" />
          Your browser does not support the audio element.
        </audio>
      )}
      
      <div className="chat-header">
        <button className="return-button unified-btn" type="button" tabIndex={0} onClick={onReturn} onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { onReturn(); } }}>
          <ArrowLeft size={18} />
          <span>Return</span>
        </button>
        
        <div className="chat-figure-info">
          <div
            className="chat-figure-portrait"
            style={{ backgroundImage: `url(${figure.portraitUrl})` }}
          ></div>
          <div className="chat-figure-details">
            <h3 className="chat-figure-name">{figure.name}</h3>
            <p className="chat-figure-era">{figure.era} • {figure.years}</p>
          </div>
        </div>
      </div>
      
      <div className="chat-messages">
        <div className="temporal-warning">
          <p>Temporal connection established. You are now communicating with {figure.name} across time.</p>
        </div>
        
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.sender === 'user' ? 'user-message' : 'figure-message'}`}
            aria-label={msg.sender === 'user' ? 'Your message' : `${figure.name}'s message`}
          >
            <div className="message-avatar-label">
              {msg.sender === 'user' ? (
                <>
                  <div className="avatar user-avatar" aria-hidden="true">
                    <span role="img" aria-label="You">🧑</span>
                  </div>
                  <span className="sender-label user-label">You</span>
                </>
              ) : (
                <>
                  <div
                    className="avatar figure-avatar"
                    style={{ backgroundImage: `url(${figure.portraitUrl})` }}
                    aria-hidden="true"
                  ></div>
                  <span className="sender-label figure-label">{figure.name}</span>
                </>
              )}
            </div>
            <div className="message-content">
              <p>{msg.text}</p>
              <span className="message-time">
                {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef}></div>
      </div>
      
      <div className="chat-input-container">
        <input
          type="text"
          ref={chatInputRef}
          className="chat-input"
          placeholder={`Ask ${figure.name} a question...`}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={!portalActive}
          aria-disabled={!portalActive}
          aria-describedby={!portalActive ? "chat-input-disabled-tip" : undefined}
          tabIndex={0}
        />
        {!portalActive && (
          <span
            id="chat-input-disabled-tip"
            className="input-tooltip"
            role="tooltip"
          >
            Portal must be active to chat.
          </span>
        )}
        <button
          className="send-button unified-btn"
          onClick={handleSendMessage}
          disabled={!portalActive || message.trim() === ''}
          aria-disabled={!portalActive || message.trim() === ''}
          aria-label={(!portalActive || message.trim() === '') ? "Send (disabled)" : "Send"}
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  );
});

export default ChatInterface;