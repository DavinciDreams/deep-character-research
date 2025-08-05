import React from 'react';
import TimePortalSearch from './TimePortalSearch';
import './styles/retro.scss';
import './styles/futuristic.scss';

const LandingPage: React.FC = () => {
    return (
        <div className="landing-page">
            <h1 className="title">Welcome to the Deep Character Research App</h1>
            <div className="time-portal">
                <h2 className="portal-title">Enter the Time Portal</h2>
                <TimePortalSearch />
            </div>
        </div>
    );
};

export default LandingPage;