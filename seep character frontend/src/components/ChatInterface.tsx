import React from 'react';
import './ChatInterface.scss';

const ChatInterface: React.FC = () => {
    return (
        <div className="chat-interface">
            <div className="chat-header">
                <h2>Time Traveler Chat</h2>
            </div>
            <div className="chat-window">
                <div className="message-container">
                    {/* Messages will be dynamically rendered here */}
                </div>
            </div>
            <div className="chat-input">
                <input type="text" placeholder="Type your message..." />
                <button type="submit">Send</button>
            </div>
        </div>
    );
};

export default ChatInterface;