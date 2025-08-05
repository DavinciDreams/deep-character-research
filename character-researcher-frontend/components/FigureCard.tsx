import React from 'react';
import Image from 'next/image';
import { HistoricalFigure } from '../types/types';
import { Clock } from 'lucide-react';
// import '../src/styles/figureCard.css'; // Moved to _app.tsx for Next.js global CSS compliance
// TODO: Replace with Tailwind classes

interface FigureCardProps {
  figure: HistoricalFigure;
  onSelect: () => void;
  onDelete?: (id: number) => void;
  onEdit?: (figure: HistoricalFigure) => void;
}

const FigureCard: React.FC<FigureCardProps> = React.memo(({ figure, onSelect, onDelete, onEdit }) => {
  return (
    <div
      className="bg-[rgba(26,26,46,0.5)] border border-yellow-700 rounded-lg overflow-hidden transition-all duration-300 cursor-pointer relative shadow-lg hover:-translate-y-1 hover:shadow-xl hover:border-blue-400"
      onClick={onSelect}
      role="button"
      tabIndex={0}
      aria-label={`View details for ${figure.name}`}
      onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { onSelect(); } }}
    >
      <div className="h-44 relative border-b border-yellow-700 flex items-center justify-center bg-black">
        <Image
          src={figure.portraitUrl}
          alt={`Portrait of ${figure.name}`}
          fill
          style={{ objectFit: 'cover' }}
          sizes="(max-width: 768px) 100vw, 33vw"
          priority
        />
        <div className="absolute bottom-2 left-2 bg-[rgba(26,26,46,0.8)] border border-yellow-700 rounded-full px-3 py-1 flex items-center gap-2 text-xs text-yellow-200">
          <Clock size={16} />
          <span>{figure.era}</span>
        </div>
      </div>

      <div className="p-5">
        <h3 className="font-serif text-lg mb-1 text-yellow-200">{figure.name}</h3>
        <p className="text-sm text-gray-100 mb-3">{figure.years}</p>
        <p className="text-sm leading-tight text-gray-100 line-clamp-3">{figure.shortDescription}</p>
        {/* Display contemporaries if present */}
        {figure.contemporaries && Array.isArray(figure.contemporaries) && figure.contemporaries.length > 0 && (
          <div className="mt-3">
            <span className="font-semibold text-xs text-yellow-300">Contemporaries: </span>
            <span className="text-xs text-gray-200">
              {figure.contemporaries
                .map(c =>
                  typeof c === 'string'
                    ? c
                    : (c as any).name || ''
                )
                .filter(Boolean)
                .join(', ')}
            </span>
          </div>
        )}
      </div>
  
      <div className="flex items-center gap-2 px-5 pb-2 text-xs text-gray-100">
        <span className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_5px_#4CAF50]" />
        <span>Available for Connection</span>
      </div>
  
      <button
        className="connect-button unified-btn"
        aria-label={`Connect with ${figure.name}`}
        style={{ touchAction: 'manipulation' }}
      >
        Connect
      </button>
      <div className="flex gap-2 px-5 pb-3">
        {onEdit && (
          <button
            className="unified-btn bg-blue-600 text-white text-xs px-2 py-1 rounded"
            onClick={e => { e.stopPropagation(); onEdit(figure); }}
            aria-label={`Edit ${figure.name}`}
            type="button"
          >
            Edit
          </button>
        )}
        {onDelete && (
          <button
            className="unified-btn bg-red-600 text-white text-xs px-2 py-1 rounded"
            onClick={e => { e.stopPropagation(); onDelete(figure.id); }}
            aria-label={`Delete ${figure.name}`}
            type="button"
          >
            Delete
          </button>
        )}
      </div>
    </div>
  );
});

export default FigureCard;