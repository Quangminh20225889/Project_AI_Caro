import { useState, useEffect, useRef, useCallback } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Board from '../components/Board';
import { playMove, saveMatchHistory } from '../services/api';
import { User, Cpu, Info, Clock, Hash, Activity } from 'lucide-react';

const DEFAULT_SETUP = { mode: 'PvA', difficulty: 'medium', boardSize: 15, firstPlayer: 1 };

export default function Game() {
  const location = useLocation();
  const navigate = useNavigate();
  const setup = location.state?.setup || DEFAULT_SETUP;
  
  const [board, setBoard] = useState(Array(setup.boardSize).fill().map(() => Array(setup.boardSize).fill(0)));
  const [currentPlayer, setCurrentPlayer] = useState(setup.mode === 'PvA' ? setup.firstPlayer : 1); // 1 = X, 2 = O
  const [winner, setWinner] = useState(0); // 0 = playing, 1 = P1, 2 = P2/AI, 3 = Draw
  const [isProcessing, setIsProcessing] = useState(false);
  const [moveHistory, setMoveHistory] = useState([]);
  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [aiError, setAiError] = useState(null);
  const [winLine, setWinLine] = useState(null);
  const isAiThinking = useRef(false);
  const lastAiTurnKey = useRef(null);

  // Check win locally to prevent unnecessary API calls
  const checkWin = useCallback((grid, player) => {
    const size = grid.length;
    const dirs = [[0, 1], [1, 0], [1, 1], [1, -1]];
    for (let r = 0; r < size; r++) {
      for (let c = 0; c < size; c++) {
        if (grid[r][c] !== player) continue;
        for (let [dr, dc] of dirs) {
          let count = 1;
          const line = [[r, c]];
          for (let step = 1; step < 5; step++) {
            const nr = r + dr * step, nc = c + dc * step;
            if (nr >= 0 && nr < size && nc >= 0 && nc < size && grid[nr][nc] === player) {
              count++;
              line.push([nr, nc]);
            } else break;
          }
          if (count >= 5) return line;
        }
      }
    }
    return null;
  }, []);

  const isFull = useCallback((grid) => grid.every(row => row.every(cell => cell !== 0)), []);

  const handleWin = useCallback(async (winPlayer, totalMoves) => {
    setWinner(winPlayer);
    try {
      await saveMatchHistory({
        mode: setup.mode,
        difficulty: setup.difficulty,
        board_size: setup.boardSize,
        winner: winPlayer,
        moves: totalMoves
      });
    } catch {
      console.error("Failed to save history");
    }
  }, [setup.mode, setup.difficulty, setup.boardSize]);

  const makeMove = useCallback(async (r, c, player) => {
    if (board[r][c] !== 0 || winner !== 0 || isProcessing) return false;
    
    const newBoard = board.map(row => [...row]);
    newBoard[r][c] = player;
    setBoard(newBoard);
    
    const moveInfo = { player, r, c };
    const nextMoveCount = moveHistory.length + 1;
    setMoveHistory(prev => [...prev, moveInfo]);

    const winCells = checkWin(newBoard, player);
    if (winCells) {
      setWinLine(winCells);
      handleWin(player, nextMoveCount);
      return true;
    } else if (isFull(newBoard)) {
      handleWin(3, nextMoveCount); // Draw
      return true;
    }

    setCurrentPlayer(3 - player);
    return true;
  }, [board, winner, isProcessing, moveHistory.length, checkWin, isFull, handleWin]);

  const handleCellClick = async (r, c) => {
    if (winner !== 0 || isProcessing) return;
    
    // In PvA, player 2 is the AI.
    if (setup.mode === 'PvA' && currentPlayer === 2) return;
    
    // In AvA, human should never click
    if (setup.mode === 'AvA') return;

    setAiError(null);
    await makeMove(r, c, currentPlayer);
  };

  // AI Turn Effect
  useEffect(() => {
    if (winner !== 0) return;

    const isAiTurn = 
      (setup.mode === 'PvA' && currentPlayer === 2) ||
      (setup.mode === 'AvA');

    if (!isAiTurn) return;

    const aiTurnKey = `${currentPlayer}-${moveHistory.length}`;
    if (isAiThinking.current || lastAiTurnKey.current === aiTurnKey) return;

    let isCancelled = false;

    const runAiTurn = async () => {
      if (isCancelled) return;

      lastAiTurnKey.current = aiTurnKey;
      isAiThinking.current = true;
      setIsProcessing(true);
      setAiError(null);

      try {
        const res = await playMove(board, currentPlayer, setup.difficulty, setup.boardSize);
        if (isCancelled) return;

        if (res.row < 0 || res.col < 0 || board[res.row]?.[res.col] !== 0) {
          throw new Error('AI returned an invalid move');
        }

        setAiAnalysis(res);

        const newBoard = board.map(row => [...row]);
        newBoard[res.row][res.col] = currentPlayer;
        setBoard(newBoard);

        const nextMoveCount = moveHistory.length + 1;
        setMoveHistory(prev => [...prev, { player: currentPlayer, r: res.row, c: res.col }]);

        const winCells = checkWin(newBoard, currentPlayer);
        if (winCells) {
          setWinLine(winCells);
          handleWin(currentPlayer, nextMoveCount);
        } else if (isFull(newBoard)) {
          handleWin(3, nextMoveCount);
        } else {
          setCurrentPlayer(3 - currentPlayer);
        }
      } catch (err) {
        console.error(err);
        if (!isCancelled) {
          setAiError('AI move failed. Check backend is running.');
        }
      } finally {
        if (!isCancelled) {
          isAiThinking.current = false;
          setIsProcessing(false);
        }
      }
    };

    const timeoutId = window.setTimeout(runAiTurn, 0);

    return () => {
      isCancelled = true;
      window.clearTimeout(timeoutId);
    };
  }, [
    currentPlayer,
    board,
    winner,
    moveHistory.length,
    setup.mode,
    setup.difficulty,
    setup.boardSize,
    checkWin,
    isFull,
    handleWin,
  ]);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
      {/* Left Column: Game Info */}
      <div className="lg:col-span-1 space-y-4">
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
          <h2 className="text-xl font-bold mb-4 flex items-center space-x-2 text-gray-800">
            <Info size={20} className="text-indigo-500" />
            <span>Match Info</span>
          </h2>
          <div className="space-y-4 text-sm">
            <div className="flex justify-between items-center pb-2 border-b">
              <span className="text-gray-500">Mode</span>
              <span className="font-semibold text-gray-800">{setup.mode}</span>
            </div>
            {setup.mode !== 'PvP' && (
              <div className="flex justify-between items-center pb-2 border-b">
                <span className="text-gray-500">Difficulty</span>
                <span className="font-semibold text-gray-800 capitalize">{setup.difficulty}</span>
              </div>
            )}
            <div className="flex justify-between items-center pb-2 border-b">
              <span className="text-gray-500">Board Size</span>
              <span className="font-semibold text-gray-800">{setup.boardSize}x{setup.boardSize}</span>
            </div>
            <div className="pt-2">
              <div className={`p-3 rounded-lg border flex items-center justify-between ${currentPlayer === 1 && winner === 0 ? 'bg-red-50 border-red-200 shadow-inner' : 'bg-gray-50 border-gray-200'}`}>
                <div className="flex items-center space-x-2">
                  {setup.mode === 'PvP' ? <User size={16} /> : (setup.mode === 'AvA' ? <Cpu size={16} /> : <User size={16} />)}
                  <span className="font-bold text-red-600">Player 1 (X)</span>
                </div>
              </div>
              <div className={`mt-2 p-3 rounded-lg border flex items-center justify-between ${currentPlayer === 2 && winner === 0 ? 'bg-blue-50 border-blue-200 shadow-inner' : 'bg-gray-50 border-gray-200'}`}>
                <div className="flex items-center space-x-2">
                  {setup.mode === 'PvP' ? <User size={16} /> : (setup.mode === 'AvA' ? <Cpu size={16} /> : <Cpu size={16} />)}
                  <span className="font-bold text-blue-600">Player 2 (O)</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {winner !== 0 && (
          <div className="bg-gradient-to-r from-emerald-400 to-emerald-500 p-6 rounded-2xl shadow-md text-white text-center">
            <h3 className="text-2xl font-bold mb-2">Game Over!</h3>
            <p className="text-lg">
              {winner === 3 ? "It's a Draw!" : `Player ${winner} (${winner === 1 ? 'X' : 'O'}) Wins!`}
            </p>
            <button 
              onClick={() => navigate('/setup')}
              className="mt-4 px-6 py-2 bg-white text-emerald-600 rounded-lg font-bold hover:bg-gray-50 transition-colors w-full"
            >
              Play Again
            </button>
          </div>
        )}
      </div>

      {/* Center Column: The Board */}
      <div className="lg:col-span-2 overflow-x-auto pb-4">
        <div className="flex justify-center min-w-max px-2">
          <div className="bg-white p-4 rounded-2xl shadow-md border border-gray-200 inline-block">
            <Board board={board} onCellClick={handleCellClick} winningCells={winLine} />
          </div>
        </div>
      </div>

      {/* Right Column: AI Analysis & History */}
      <div className="lg:col-span-1 space-y-4">
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
          <h2 className="text-xl font-bold mb-4 flex items-center space-x-2 text-gray-800">
            <Activity size={20} className="text-emerald-500" />
            <span>AI Analysis</span>
          </h2>
          
          <div className="min-h-[196px] flex flex-col justify-center">
            {isProcessing ? (
              <div className="flex flex-col items-center justify-center text-gray-500">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mb-4"></div>
                <p>AI is thinking...</p>
              </div>
            ) : aiError ? (
              <div className="bg-red-50 p-3 rounded-lg border border-red-100 text-center text-sm text-red-700">
                {aiError}
              </div>
            ) : aiAnalysis ? (
              <div className="space-y-4 text-sm">
                <div className="bg-gray-50 p-3 rounded-lg border border-gray-200 min-h-[72px]">
                  <p className="text-xs text-gray-500 mb-1">Reasoning</p>
                  <p className="font-medium text-gray-800">{aiAnalysis.reason}</p>
                </div>
                
                <div className="grid grid-cols-2 gap-2">
                  <div className="bg-indigo-50 p-3 rounded-lg border border-indigo-100 flex flex-col items-center justify-center min-h-[72px]">
                    <Activity size={18} className="text-indigo-500 mb-1" />
                    <span className="text-xs text-gray-500">Score</span>
                    <span className="font-bold text-indigo-700">{aiAnalysis.heuristic_score}</span>
                  </div>
                  <div className="bg-emerald-50 p-3 rounded-lg border border-emerald-100 flex flex-col items-center justify-center min-h-[72px]">
                    <Clock size={18} className="text-emerald-500 mb-1" />
                    <span className="text-xs text-gray-500">Time (s)</span>
                    <span className="font-bold text-emerald-700">{aiAnalysis.evaluation_time.toFixed(3)}</span>
                  </div>
                  <div className="bg-amber-50 p-3 rounded-lg border border-amber-100 flex flex-col items-center justify-center col-span-2 min-h-[72px]">
                    <Hash size={18} className="text-amber-500 mb-1" />
                    <span className="text-xs text-gray-500">Nodes Evaluated</span>
                    <span className="font-bold text-amber-700">{aiAnalysis.nodes_evaluated.toLocaleString()}</span>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center text-gray-400 italic">
                Waiting for AI move...
              </div>
            )}
          </div>
        </div>

        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col min-h-[190px] max-h-[400px]">
          <h2 className="text-xl font-bold mb-4 flex items-center space-x-2 text-gray-800">
            <Clock size={20} className="text-blue-500" />
            <span>Move History</span>
          </h2>
          <div className="overflow-y-auto flex-1 space-y-2 pr-2">
            {moveHistory.length === 0 ? (
              <p className="text-gray-400 italic text-center py-4">No moves yet</p>
            ) : (
              [...moveHistory].reverse().map((move, idx) => (
                <div key={idx} className="flex justify-between items-center p-2 bg-gray-50 rounded border text-sm">
                  <span className="text-gray-500">Move {moveHistory.length - idx}</span>
                  <span className={`font-bold ${move.player === 1 ? 'text-blue-600' : 'text-red-600'}`}>
                    {move.player === 1 ? 'X' : 'O'} at ({move.r}, {move.c})
                  </span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
