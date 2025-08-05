import React, { useEffect, useRef } from 'react';
import { Zap } from 'lucide-react';
import PortalVortex from './PortalVortex';
import { HistoricalFigure } from '../types/types';

interface TimePortalProps {
  active: boolean;
  figure: HistoricalFigure | null;
  soundEnabled: boolean;
  isSearching?: boolean;
}

const TimePortal: React.FC<TimePortalProps> = ({ active, figure, soundEnabled, isSearching }) => {
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (soundEnabled && active && audioRef.current) {
      audioRef.current.volume = 0.3;
      audioRef.current.currentTime = 0;
      audioRef.current.play().catch(e => console.log('Audio playback prevented:', e));
    }
  }, [active, soundEnabled]);

  return (
    <div className={`time-portal-container ${active ? 'active' : ''} ${isSearching ? 'searching' : ''}`}>
      {soundEnabled && (
        <audio ref={audioRef} preload="auto">
          <source src="https://assets.mixkit.co/active_storage/sfx/212/212-preview.mp3" type="audio/mpeg" />
          Your browser does not support the audio element.
        </audio>
      )}
      
      <div className="portal-outer-ring">
        <div className="portal-middle-ring">
          <div className="portal-inner-ring">
            <PortalVortex active={active} isSearching={isSearching} />
            
            {figure && active && !isSearching && (
              <div className="portal-figure-container">
                <div className="portal-figure-image" 
                     style={{ backgroundImage: `url(${figure.portraitUrl})` }} />
              </div>
            )}
          </div>
        </div>
      </div>
      
      <div className="portal-decorations">
        {Array.from({ length: 8 }).map((_, i) => (
          <div key={`gear-${i}`} className={`gear gear-${i}`}>
            <div className="gear-center"></div>
            <div className="gear-teeth"></div>
          </div>
        ))}
        
        <div className="energy-indicators">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={`energy-${i}`} className={`energy-bolt energy-${i} ${active ? 'active' : ''}`}>
              <Zap size={24} />
            </div>
          ))}
        </div>
      </div>
      
      <div className="portal-status">
        {!active && <span className="status-inactive">Portal Inactive</span>}
        {active && isSearching && <span className="status-searching">Searching Through Time...</span>}
        {active && !isSearching && !figure && <span className="status-ready">Portal Ready</span>}
        {active && !isSearching && figure && (
          <span className="status-connected">
            Connected to {figure.era}
          </span>
        )}
      </div>
    </div>
  );
};

export default TimePortal;