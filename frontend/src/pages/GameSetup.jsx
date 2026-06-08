import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Settings, Play } from 'lucide-react';

export default function GameSetup() {
  const navigate = useNavigate();
  const [setup, setSetup] = useState({
    mode: 'PvA', // PvA, PvP, AvA
    difficulty: 'medium', // easy, medium, hard
    boardSize: 15,
    firstPlayer: 1, // 1 for Player 1 (X), 2 for Player 2 / AI (O)
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate('/game', { state: { setup } });
  };

  return (
    <div className="max-w-2xl mx-auto bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="bg-gradient-to-r from-indigo-500 to-indigo-600 p-6 text-white flex items-center space-x-3">
        <Settings className="text-white opacity-80" size={28} />
        <h2 className="text-2xl font-bold">Game Setup</h2>
      </div>

      <form onSubmit={handleSubmit} className="p-8 space-y-6">
        {/* Game Mode */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-3">Game Mode</label>
          <div className="grid grid-cols-3 gap-3">
            {['PvA', 'PvP', 'AvA'].map((mode) => (
              <button
                key={mode}
                type="button"
                onClick={() => setSetup({...setup, mode})}
                className={`py-3 rounded-xl border font-medium transition-all ${
                  setup.mode === mode 
                    ? 'border-indigo-600 bg-indigo-50 text-indigo-700 ring-2 ring-indigo-600/20' 
                    : 'border-gray-200 text-gray-600 hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                {mode === 'PvA' ? 'Player vs AI' : mode === 'PvP' ? 'Player vs Player' : 'AI vs AI'}
              </button>
            ))}
          </div>
        </div>

        {/* Difficulty (only show if AI is involved) */}
        {setup.mode !== 'PvP' && (
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">AI Difficulty</label>
            <div className="grid grid-cols-3 gap-3">
              {['easy', 'medium', 'hard'].map((level) => (
                <button
                  key={level}
                  type="button"
                  onClick={() => setSetup({...setup, difficulty: level})}
                  className={`py-3 rounded-xl border font-medium capitalize transition-all ${
                    setup.difficulty === level 
                      ? 'border-emerald-500 bg-emerald-50 text-emerald-700 ring-2 ring-emerald-500/20' 
                      : 'border-gray-200 text-gray-600 hover:border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  {level}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Board Size */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-3">Board Size</label>
          <div className="grid grid-cols-3 gap-3">
            {[10, 15, 20].map((size) => (
              <button
                key={size}
                type="button"
                onClick={() => setSetup({...setup, boardSize: size})}
                className={`py-3 rounded-xl border font-medium transition-all ${
                  setup.boardSize === size 
                    ? 'border-indigo-600 bg-indigo-50 text-indigo-700 ring-2 ring-indigo-600/20' 
                    : 'border-gray-200 text-gray-600 hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                {size}x{size}
              </button>
            ))}
          </div>
        </div>

        {/* First Player (only for PvA) */}
        {setup.mode === 'PvA' && (
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">Who Goes First?</label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setSetup({...setup, firstPlayer: 1})}
                className={`py-3 rounded-xl border font-medium transition-all ${
                  setup.firstPlayer === 1 
                    ? 'border-blue-500 bg-blue-50 text-blue-700 ring-2 ring-blue-500/20' 
                    : 'border-gray-200 text-gray-600 hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                Player (X)
              </button>
              <button
                type="button"
                onClick={() => setSetup({...setup, firstPlayer: 2})}
                className={`py-3 rounded-xl border font-medium transition-all ${
                  setup.firstPlayer === 2 
                    ? 'border-red-500 bg-red-50 text-red-700 ring-2 ring-red-500/20' 
                    : 'border-gray-200 text-gray-600 hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                AI (O)
              </button>
            </div>
          </div>
        )}

        <div className="pt-4">
          <button 
            type="submit"
            className="w-full flex items-center justify-center space-x-2 bg-indigo-600 text-white p-4 rounded-xl font-bold text-lg hover:bg-indigo-700 transition-colors"
          >
            <Play size={20} />
            <span>Start Game</span>
          </button>
        </div>
      </form>
    </div>
  );
}
