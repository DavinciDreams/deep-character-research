import React from 'react';
import './styles/retro.scss';
import './styles/futuristic.scss';
import './styles/vintage-print.scss';

interface CharacterProfileProps {
    name: string;
    image: string;
    description: string;
    additionalInfo: string;
}

const CharacterProfile: React.FC<CharacterProfileProps> = ({ name, image, description, additionalInfo }) => {
    return (
        <div className="character-profile">
            <div className="profile-header">
                <h2>{name}</h2>
            </div>
            <div className="profile-image">
                <img src={image} alt={`${name} profile`} className="sepia-image" />
            </div>
            <div className="profile-description">
                <p>{description}</p>
            </div>
            <div className="profile-additional-info">
                <p>{additionalInfo}</p>
            </div>
            <HolographicOverlay />
        </div>
    );
};

const HolographicOverlay: React.FC = () => {
    return (
        <div className="holographic-overlay">
            {/* Holographic effect can be implemented here */}
        </div>
    );
};

export default CharacterProfile;