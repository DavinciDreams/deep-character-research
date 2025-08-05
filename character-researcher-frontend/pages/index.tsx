// Home page: Large centered search bar (ResearchInputForm) at top, gallery below.

import React from 'react';
import ResearchInputForm from '../components/ResearchInputForm';
import HistoricalFigureGallery from '../components/HistoricalFigureGallery';
import dynamic from 'next/dynamic';

const BackgroundEffects = dynamic(() => import('../components/BackgroundEffects'), {
  ssr: false,
  loading: () => <div style={{ width: '100vw', height: '100vh', background: '#181a1b' }} />,
});

export default function Home() {
  return (
    <main className="relative min-h-screen overflow-hidden bg-[#181a1b]">
      <BackgroundEffects />
      <div className="relative z-10 flex flex-col items-center w-full px-4 pt-12">
        <h1 className="text-4xl md:text-5xl font-serif font-bold text-yellow-300 drop-shadow-lg mb-8 text-center tracking-tight">
          Historical AI
        </h1>
        <div className="w-full max-w-2xl mb-8 flex justify-center">
          <div className="max-w-lg w-full search-bar-enhanced flex justify-center">
            <ResearchInputForm />
          </div>
        </div>
        <div className="w-full max-w-5xl">
          <HistoricalFigureGallery onSelectFigure={() => {}} searchQuery="" showFilters={true} />
        </div>
      </div>
    </main>
  );
}