import React, { useState, useEffect, useRef } from 'react';
import { HistoricalFigure } from '../types/types';
import FigureCard from './FigureCard';
// import '../src/styles/historicalFigureGallery.css'; // Moved to _app.tsx for Next.js global CSS compliance
import { getCharacters } from '../services/api';

interface HistoricalFigureGalleryProps {
  onSelectFigure: (figure: HistoricalFigure) => void;
  searchQuery: string;
  showFilters?: boolean;
}

const HistoricalFigureGallery: React.FC<HistoricalFigureGalleryProps> = React.memo(({
  onSelectFigure,
  searchQuery,
  showFilters = true
}) => {
  const [figures, setFigures] = useState<HistoricalFigure[]>([]);
  const [selectedEra, setSelectedEra] = useState<string | null>(null);
  const [selectedType, setSelectedType] = useState<string | null>(null);
  const [selectedProfession, setSelectedProfession] = useState<string | null>(null);
  const [eras, setEras] = useState<string[]>([]);
  const [professions, setProfessions] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  // Placeholder types until backend supports "type"
  const types = ['All Types'];

  // Simple in-memory cache for filter results
  const cacheRef = useRef<{ [key: string]: HistoricalFigure[] }>({});

  // Debounce timer ref
  const debounceRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    setLoading(true);
    // Debounce API calls for filters
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      const cacheKey = `${selectedEra || 'all'}|${selectedType || 'all'}|${selectedProfession || 'all'}`;
      if (cacheRef.current[cacheKey]) {
        setFigures(cacheRef.current[cacheKey]);
        setEras(Array.from(new Set(cacheRef.current[cacheKey].map((f: HistoricalFigure) => f.era))));
        setProfessions(Array.from(new Set(cacheRef.current[cacheKey].map((f: any) => f.profession).filter(Boolean))));
        setLoading(false);
        return;
      }
      const fetchFigures = async () => {
        try {
          const data = await getCharacters({
            era: selectedEra || undefined,
            type: selectedType && selectedType !== 'All Types' ? selectedType : undefined,
            profession: selectedProfession && selectedProfession !== 'All Professions' ? selectedProfession : undefined
          });
          setFigures(data);
          cacheRef.current[cacheKey] = data;
          setEras(Array.from(new Set(data.map((f: HistoricalFigure) => f.era))));
          setProfessions(Array.from(new Set(data.map((f: any) => f.profession).filter(Boolean))));
        } catch (err) {
          setFigures([]);
          setProfessions([]);
        } finally {
          setLoading(false);
        }
      };
      fetchFigures();
    }, 400); // 400ms debounce
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, [selectedEra, selectedType, selectedProfession]);

  const filteredFigures = React.useMemo(() => figures.filter(figure => {
    const matchesSearch =
      figure.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      figure.era.toLowerCase().includes(searchQuery.toLowerCase()) ||
      figure.shortDescription.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesSearch;
  }), [figures, searchQuery]);

  return (
    <div className="w-full flex flex-col gap-8">
      {showFilters && (
        <div className="flex flex-wrap justify-center gap-2 mb-4">
          <button
            className={`unified-btn era-button${selectedEra === null ? ' active' : ''}`}
            onClick={() => setSelectedEra(null)}
            role="button"
            tabIndex={0}
            aria-label="Show all eras"
            onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { setSelectedEra(null); } }}
            style={{ touchAction: 'manipulation' }}
          >
            All Eras
          </button>
          {eras.map(era => (
            <button
              key={era}
              className={`unified-btn era-button${selectedEra === era ? ' active' : ''}`}
              onClick={() => setSelectedEra(era)}
              role="button"
              tabIndex={0}
              aria-label={`Filter by era: ${era}`}
              onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { setSelectedEra(era); } }}
              style={{ touchAction: 'manipulation' }}
            >
              {era}
            </button>
          ))}
          {/* Profession filter */}
          <select
            className="ml-4 unified-btn era-button"
            value={selectedProfession || 'All Professions'}
            onChange={e => setSelectedProfession(e.target.value)}
            aria-label="Filter by profession"
            style={{ touchAction: 'manipulation' }}
          >
            <option value="All Professions">All Professions</option>
            {professions.map(prof => (
              <option key={prof} value={prof}>
                {prof}
              </option>
            ))}
          </select>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full">
        {loading
          ? Array.from({ length: 6 }).map((_, i) => (
              <div
                key={i}
                className="animate-pulse bg-yellow-900/10 border border-yellow-700 rounded-lg h-64 w-full"
                style={{ minHeight: 220 }}
              />
            ))
          : filteredFigures.map(figure => (
              <FigureCard
                key={figure.id}
                figure={figure}
                onSelect={() => onSelectFigure(figure)}
              />
            ))}
      </div>
    </div>
  );
});


export default HistoricalFigureGallery;