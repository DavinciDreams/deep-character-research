import React from 'react';
import dynamic from 'next/dynamic';
import { mockFigure } from '../src/demoData';
import { useDemoToggles } from '../src/demoUtils';

const TimePortal = dynamic(() => import('../components/TimePortal'), {
  ssr: false,
  loading: () => <div style={{ width: '100vw', height: '100vh', background: '#181a1b' }} />,
});

const PortalDemoPage = () => {
  const {
    active,
    setActive,
    isSearching,
    setIsSearching,
    soundEnabled,
    setSoundEnabled,
    figure,
    setFigure,
  } = useDemoToggles({ figure: mockFigure });

  return (
    <div style={{ width: '100vw', height: '100vh', background: '#181a1b', position: 'relative' }}>
      <TimePortal
        active={active}
        isSearching={isSearching}
        soundEnabled={soundEnabled}
        figure={figure}
      />
      <div style={{
        position: 'absolute', top: 20, left: 20, color: '#fff', zIndex: 2,
        background: 'rgba(0,0,0,0.5)', padding: '8px 16px', borderRadius: 8
      }}>
        <h2>Time Portal Demo</h2>
        <button onClick={() => setActive((a: boolean) => !a)} style={{ marginRight: 8 }}>
          Toggle Active ({active ? 'On' : 'Off'})
        </button>
        <button onClick={() => setIsSearching((s: boolean) => !s)} style={{ marginRight: 8 }}>
          Toggle Searching ({isSearching ? 'On' : 'Off'})
        </button>
        <button onClick={() => setSoundEnabled((se: boolean) => !se)} style={{ marginRight: 8 }}>
          Toggle Sound ({soundEnabled ? 'On' : 'Off'})
        </button>
        <button onClick={() => setFigure((f: any) => f ? null : mockFigure)}>
          Toggle Figure ({figure ? 'Shown' : 'Hidden'})
        </button>
      </div>
    </div>
  );
};

export default PortalDemoPage;