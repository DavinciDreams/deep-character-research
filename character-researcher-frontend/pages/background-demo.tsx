import React from 'react';
import dynamic from 'next/dynamic';

const BackgroundEffects = dynamic(() => import('../components/BackgroundEffects'), {
  ssr: false,
  loading: () => <div style={{ width: '100vw', height: '100vh', background: '#181a1b' }} />,
});

const BackgroundDemoPage = () => (
  <div style={{ width: '100vw', height: '100vh', position: 'relative', overflow: 'hidden' }}>
    <BackgroundEffects />
    <div style={{
      position: 'absolute', top: 20, left: 20, color: '#fff', zIndex: 2,
      background: 'rgba(0,0,0,0.5)', padding: '8px 16px', borderRadius: 8
    }}>
      <h2>Background Effects Demo</h2>
      <p>This page demonstrates the animated background effects component.</p>
    </div>
  </div>
);

export default BackgroundDemoPage;