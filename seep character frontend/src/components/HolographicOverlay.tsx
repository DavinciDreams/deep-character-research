import React from 'react';
import './HolographicOverlay.scss';

const HolographicOverlay: React.FC<{ imageUrl: string; title: string; description: string }> = ({ imageUrl, title, description }) => {
    return (
        <div className="holographic-overlay">
            <img src={imageUrl} alt={title} className="holographic-image" />
            <div className="holographic-content">
                <h2 className="holographic-title">{title}</h2>
                <p className="holographic-description">{description}</p>
            </div>
        </div>
    );
};

export default HolographicOverlay;