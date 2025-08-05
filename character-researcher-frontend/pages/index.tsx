// Home page: Large centered search bar (ResearchInputForm) at top, gallery below.

import React, { useState } from 'react';
import dynamic from 'next/dynamic';
import HistoricalFigureGallery from '../components/HistoricalFigureGallery';

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
      <BackgroundEffects />
      <div className="relative z-10 flex flex-col items-center w-full px-4 pt-12">
        <h1 className="text-4xl md:text-5xl font-serif font-bold text-yellow-300 drop-shadow-lg mb-8 text-center tracking-tight">
          Historical AI
        </h1>
        <div className="w-full max-w-2xl mb-8 flex justify-center">
          <form
            className="max-w-lg w-full search-bar-enhanced flex flex-col gap-3 bg-yellow-900/10 p-6 rounded-lg shadow-lg"
            onSubmit={handleSearch}
            role="search"
            aria-label="Search historical figures"
          >
            <input
              type="text"
              name="name"
              value={searchFields.name}
              onChange={handleInputChange}
              placeholder="Name"
              className="rounded px-3 py-2 mb-1 bg-[#232323] text-yellow-100 placeholder-yellow-400 border border-yellow-700 focus:outline-none focus:ring-2 focus:ring-yellow-400"
              aria-label="Name"
            />
            <input
              type="text"
              name="field"
              value={searchFields.field}
              onChange={handleInputChange}
              placeholder="Field (e.g. science, art)"
              className="rounded px-3 py-2 mb-1 bg-[#232323] text-yellow-100 placeholder-yellow-400 border border-yellow-700 focus:outline-none focus:ring-2 focus:ring-yellow-400"
              aria-label="Field"
            />
            <input
              type="text"
              name="era"
              value={searchFields.era}
              onChange={handleInputChange}
              placeholder="Era (e.g. Renaissance)"
              className="rounded px-3 py-2 mb-1 bg-[#232323] text-yellow-100 placeholder-yellow-400 border border-yellow-700 focus:outline-none focus:ring-2 focus:ring-yellow-400"
              aria-label="Era"
            />
            <input
              type="text"
              name="description"
              value={searchFields.description}
              onChange={handleInputChange}
              placeholder="Description keywords"
              className="rounded px-3 py-2 mb-2 bg-[#232323] text-yellow-100 placeholder-yellow-400 border border-yellow-700 focus:outline-none focus:ring-2 focus:ring-yellow-400"
              aria-label="Description keywords"
            />
            <button
              type="submit"
              className="unified-btn bg-yellow-400 text-[#181a1b] font-bold py-2 px-4 rounded hover:bg-yellow-300 transition"
            >
              Search
            </button>
          </form>
        </div>
        <div className="w-full max-w-5xl">
          <HistoricalFigureGallery
            onSelectFigure={() => {}}
            searchFields={submittedFields}
            showFilters={true}
          />
        </div>
      </div>
    </main>
  );
}