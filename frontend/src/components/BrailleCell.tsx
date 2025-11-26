import React from 'react';
import './BrailleCell.css';

interface BrailleCellProps {
  activeDots: number[]; // Ej: [1, 2, 5]
}

const BrailleCell: React.FC<BrailleCellProps> = ({ activeDots }) => {
  // El braille tiene 6 posiciones fijas: 1, 2, 3 (izq), 4, 5, 6 (der)
  // Mapeamos visualmente el orden de la grid:
  // 1 4
  // 2 5
  // 3 6
  const dots = [1, 4, 2, 5, 3, 6]; 

  return (
    <div className="braille-cell" aria-label={`Puntos braille: ${activeDots.join(',')}`}>
      {dots.map((dotNumber) => (
        <div
          key={dotNumber}
          className={`braille-dot ${activeDots.includes(dotNumber) ? 'active' : ''}`}
        />
      ))}
    </div>
  );
};

export default BrailleCell;