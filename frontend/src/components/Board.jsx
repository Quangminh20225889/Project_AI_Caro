export default function Board({ board, onCellClick, winningCells }) {
  const size = board.length;
  
  return (
    <div 
      className="board-grid select-none" 
      style={{ gridTemplateColumns: `repeat(${size}, minmax(0, 1fr))` }}
    >
      {board.map((row, r) => (
        row.map((cell, c) => {
          const isWinning = winningCells?.some(([wr, wc]) => wr === r && wc === c);
          return (
            <div
              key={`${r}-${c}`}
              className={`cell ${isWinning ? 'win-cell' : ''}`}
              onClick={() => onCellClick(r, c)}
            >
              {cell === 1 && <span className="piece-x">X</span>}
              {cell === 2 && <span className="piece-o">O</span>}
            </div>
          );
        })
      ))}
    </div>
  );
}
