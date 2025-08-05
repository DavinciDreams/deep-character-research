import React from 'react';
import './LoadingScreen.scss';

const LoadingScreen: React.FC = () => {
    return (
        <div className="loading-screen">
            <div className="time-portal">
                <div className="portal-effect"></div>
                <h1>Loading Time Travel...</h1>
            </div>
            <div className="loading-animation">
                <div className="time-travel-effect"></div>
            </div>
        </div>
    );
};

export default LoadingScreen;