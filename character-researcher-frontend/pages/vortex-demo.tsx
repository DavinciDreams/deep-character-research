import React from 'react';
import PortalVortex from '../components/PortalVortex';
import { useDemoToggles } from '../src/demoUtils';

const VortexDemoPage = () => {
  const { active, setActive, isSearching, setIsSearching } = useDemoToggles();

  return (
    <div style={{ width: '100vw', height: '100vh', background: '#111', position: 'relative' }}>
      <PortalVortex active={active} isSearching={isSearching} />
      <div style={{
        position: 'absolute', top: 20, left: 20, color: '#fff', zIndex: 2,
        background: 'rgba(0,0,0,0.5)', padding: '8px 16px', borderRadius: 8
      }}>
        <h2>Portal Vortex Demo</h2>
        <button onClick={() => setActive((a: boolean) => !a)} style={{ marginRight: 8 }}>
          Toggle Active ({active ? 'On' : 'Off'})
        </button>
        <button onClick={() => setIsSearching((s: boolean) => !s)}>
          Toggle Searching ({isSearching ? 'On' : 'Off'})
        </button>
      </div>
    </div>
  );
};

export default VortexDemoPage;