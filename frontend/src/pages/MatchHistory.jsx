import { useState, useEffect } from 'react';
import { getMatchHistory } from '../services/api';
import { History, Trophy } from 'lucide-react';

export default function MatchHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMatchHistory()
      .then(data => {
        setHistory(data);
      })
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center space-x-3 mb-8">
        <History size={32} className="text-indigo-600" />
        <h1 className="text-3xl font-bold text-gray-800">Lịch Sử Trận Đấu</h1>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>
      ) : history.length === 0 ? (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-12 text-center text-gray-500">
          Chưa có trận đấu nào.
        </div>
      ) : (
        <div className="space-y-4">
          {history.map((match, idx) => (
            <div key={match.id || idx} className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 flex items-center justify-between hover:shadow-md transition-shadow">
              
              <div className="flex items-center space-x-4 w-1/3">
                <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                  match.winner === 1 ? 'bg-blue-100 text-blue-600' :
                  match.winner === 2 ? 'bg-red-100 text-red-600' : 'bg-gray-100 text-gray-600'
                }`}>
                  <Trophy size={20} />
                </div>
                <div>
                  <p className="font-bold text-gray-800">
                    {match.winner === 1 ? 'Người chơi 1 Thắng' : match.winner === 2 ? 'Người chơi 2/AI Thắng' : 'Hòa'}
                  </p>
                  <p className="text-xs text-gray-500">{new Date(match.timestamp).toLocaleString()}</p>
                </div>
              </div>

              <div className="flex items-center space-x-8 w-2/3 justify-end text-sm">
                <div className="flex flex-col items-center">
                  <span className="text-gray-500 text-xs">Chế Độ</span>
                  <span className="font-semibold text-gray-700">{match.mode}</span>
                </div>
                <div className="flex flex-col items-center">
                  <span className="text-gray-500 text-xs">Độ Khó</span>
                  <span className="font-semibold text-gray-700 capitalize">{match.difficulty === 'easy' ? 'Dễ' : match.difficulty === 'medium' ? 'Trung bình' : match.difficulty === 'hard' ? 'Khó' : '-'}</span>
                </div>
                <div className="flex flex-col items-center">
                  <span className="text-gray-500 text-xs">Bàn Cờ</span>
                  <span className="font-semibold text-gray-700">{match.board_size}x{match.board_size}</span>
                </div>
                <div className="flex flex-col items-center">
                  <span className="text-gray-500 text-xs">Số Nước</span>
                  <span className="font-semibold text-gray-700">{match.moves}</span>
                </div>
              </div>

            </div>
          ))}
        </div>
      )}
    </div>
  );
}
