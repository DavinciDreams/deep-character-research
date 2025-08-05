import React, { useState, useEffect, useRef } from 'react';
import { HistoricalFigure, CharacterSearchFilters } from '../types/types';
import FigureCard from './FigureCard';
// import '../src/styles/historicalFigureGallery.css'; // Moved to _app.tsx for Next.js global CSS compliance
import { getCharacters, createCharacter, deleteCharacter, updateCharacter, searchUsers } from '../services/api';

export interface HistoricalFigureGalleryProps {
  onSelectFigure: (figure: HistoricalFigure) => void;
  searchFields?: CharacterSearchFilters & { description?: string };
  showFilters?: boolean;
}

const HistoricalFigureGallery: React.FC<HistoricalFigureGalleryProps> = React.memo(({
  onSelectFigure,
  searchFields,
  showFilters = true
}) => {
  const effectiveSearchFields = searchFields || {};
  const [figures, setFigures] = useState<HistoricalFigure[]>([]);
  const [adding, setAdding] = useState(false);
  const [newName, setNewName] = useState('');
  const [editingFigure, setEditingFigure] = useState<HistoricalFigure | null>(null);
  const [editName, setEditName] = useState('');
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
    // Debounce API calls for filters and search
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      const cacheKey = `${selectedEra || 'all'}|${selectedType || 'all'}|${selectedProfession || 'all'}|${effectiveSearchFields.name || ''}|${effectiveSearchFields.field || ''}|${effectiveSearchFields.era || ''}|${effectiveSearchFields.description || ''}`;
      if (cacheRef.current[cacheKey]) {
        setFigures(cacheRef.current[cacheKey]);
        setEras(Array.from(new Set(cacheRef.current[cacheKey].map((f: HistoricalFigure) => f.era))));
        setProfessions(Array.from(new Set(cacheRef.current[cacheKey].map((f: any) => f.profession).filter(Boolean))));
        setLoading(false);
        return;
      }
      const fetchFigures = async () => {
        try {
          let figuresData: HistoricalFigure[] = [];
          // If searching by user name, use user search API
          if (effectiveSearchFields.name && effectiveSearchFields.name.trim() !== '') {
            const users = await searchUsers(effectiveSearchFields.name.trim());
            // Map UserSearch results to HistoricalFigure shape if needed, or display as-is if compatible
            figuresData = users as unknown as HistoricalFigure[];
          } else {
            const data = await getCharacters({
              era: effectiveSearchFields.era || selectedEra || undefined,
              type: selectedType && selectedType !== 'All Types' ? selectedType : undefined,
              profession: selectedProfession && selectedProfession !== 'All Professions' ? selectedProfession : undefined,
              name: effectiveSearchFields.name || undefined,
              field: effectiveSearchFields.field || undefined,
              keywords: effectiveSearchFields.description || undefined
            });
            figuresData = data.characters;
          }
          setFigures(figuresData);
          cacheRef.current[cacheKey] = figuresData;
          setEras(Array.from(new Set(figuresData.map((f: HistoricalFigure) => f.era))));
          setProfessions(Array.from(new Set(figuresData.map((f: any) => f.profession).filter(Boolean))));
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
  }, [selectedEra, selectedType, selectedProfession, effectiveSearchFields.name, effectiveSearchFields.field, effectiveSearchFields.era, effectiveSearchFields.description]);

  // No longer filter by searchQuery; backend handles filtering
  const filteredFigures = figures;

  // Only show filters if showFilters is true AND gallery data is loaded and non-empty
  const shouldShowFilters = showFilters && filteredFigures.length > 0 && !loading;

  return (
    <div className="w-full flex flex-col gap-8">
      <div className="flex justify-end mb-2">
        <button
          className="unified-btn bg-green-600 text-white px-3 py-1 rounded"
          onClick={() => setAdding(true)}
          type="button"
        >
          Add Figure
        </button>
      </div>
      {adding && (
        <div className="flex items-center gap-2 mb-4">
          <input
            type="text"
            value={newName}
            onChange={e => setNewName(e.target.value)}
            placeholder="New figure name"
            className="rounded px-2 py-1 border border-yellow-700"
          />
          <button
            className="unified-btn bg-green-700 text-white px-2 py-1 rounded"
            onClick={async () => {
              if (!newName.trim()) return;
              setAdding(false);
              setNewName('');
              try {
                const created = await createCharacter(newName.trim());
                setFigures(prev => [...prev, created]);
              } catch (err) {
                // handle error
              }
            }}
            type="button"
          >
            Save
          </button>
          <button
            className="unified-btn bg-gray-500 text-white px-2 py-1 rounded"
            onClick={() => { setAdding(false); setNewName(''); }}
            type="button"
          >
            Cancel
          </button>
        </div>
      )}
      {editingFigure && (
        <div className="flex items-center gap-2 mb-4">
          <input
            type="text"
            value={editName}
            onChange={e => setEditName(e.target.value)}
            placeholder="Edit figure name"
            className="rounded px-2 py-1 border border-yellow-700"
          />
          <button
            className="unified-btn bg-blue-700 text-white px-2 py-1 rounded"
            onClick={async () => {
              if (!editName.trim()) return;
              try {
                const updated = await updateCharacter(editingFigure.id, editName.trim());
                setFigures(prev =>
                  prev.map(f => (f.id === updated.id ? updated : f))
                );
                setEditingFigure(null);
                setEditName('');
              } catch (err) {
                // handle error
              }
            }}
            type="button"
          >
            Save
          </button>
          <button
            className="unified-btn bg-gray-500 text-white px-2 py-1 rounded"
            onClick={() => { setEditingFigure(null); setEditName(''); }}
            type="button"
          >
            Cancel
          </button>
        </div>
      )}
      {shouldShowFilters && (
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