// Home page: Large centered search bar (ResearchInputForm) at top, gallery below.

import React, { useState } from 'react';
import dynamic from 'next/dynamic';
import HistoricalFigureGallery from '../components/HistoricalFigureGallery';
import ResearchInputForm from '../components/ResearchInputForm';

const BackgroundEffects = dynamic(() => import('../components/BackgroundEffects'), {
  ssr: false,
  loading: () => <div style={{ width: '100vw', height: '100vh', background: '#181a1b' }} />,
});

export default function Home() {
  const [searchFields, setSearchFields] = useState({
    name: '',
    field: '',
    era: '',
    description: ''
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setSearchFields(prev => ({ ...prev, [name]: value }));
  };

  const [submittedFields, setSubmittedFields] = useState(searchFields);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmittedFields(searchFields);
  };

  return (
    <main className="relative min-h-screen overflow-hidden bg-[#181a1b]">
      <div className="relative z-10 flex flex-col items-center w-full px-4 pt-12">
        <h1 className="text-4xl md:text-5xl font-serif font-bold text-yellow-300 drop-shadow-lg mb-8 text-center tracking-tight">
          Historical AI
        </h1>
        <div className="w-full max-w-2xl mb-8 flex justify-center">
          <ResearchInputForm />
        </div>
        <div className="w-full max-w-5xl">
          <HistoricalFigureGallery
            onSelectFigure={() => {}}
            searchFields={submittedFields}
            showFilters={false}
          />
        </div>
      </div>
    </main>
  );
}