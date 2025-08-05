import { useState } from 'react';

export function useDemoToggles(initial: {
  active?: boolean;
  isSearching?: boolean;
  soundEnabled?: boolean;
  figure?: any;
} = {}) {
  const [active, setActive] = useState(initial.active ?? true);
  const [isSearching, setIsSearching] = useState(initial.isSearching ?? false);
  const [soundEnabled, setSoundEnabled] = useState(initial.soundEnabled ?? true);
  const [figure, setFigure] = useState(initial.figure ?? null);

  return {
    active,
    setActive,
    isSearching,
    setIsSearching,
    soundEnabled,
    setSoundEnabled,
    figure,
    setFigure,
  };
}