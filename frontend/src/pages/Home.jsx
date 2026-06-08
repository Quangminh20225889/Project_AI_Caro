import { useNavigate } from 'react-router-dom';
import { BrainCircuit, Swords, Trophy } from 'lucide-react';

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center py-12 px-4">
      <div className="max-w-3xl text-center space-y-8">
        <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight text-gray-900">
          Master Gomoku against <br className="hidden md:block"/>
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-emerald-500">
            Advanced AI
          </span>
        </h1>
        
        <p className="text-xl text-gray-600 leading-relaxed max-w-2xl mx-auto">
          Built as a final project for Intro to Artificial Intelligence. 
          Challenge our Minimax + Alpha-Beta Pruning agent or play against a friend locally!
        </p>

        <button 
          onClick={() => navigate('/setup')}
          className="mt-8 px-8 py-4 bg-indigo-600 text-white rounded-full font-bold text-lg hover:bg-indigo-700 hover:shadow-xl hover:-translate-y-1 transition-all duration-200"
        >
          Play Now
        </button>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16 text-left">
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-indigo-100 text-indigo-600 rounded-xl flex items-center justify-center mb-4">
              <BrainCircuit size={24} />
            </div>
            <h3 className="text-xl font-bold mb-2">Smart AI</h3>
            <p className="text-gray-600">Three difficulty levels utilizing rule-based heuristics and Minimax search tree.</p>
          </div>
          
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-emerald-100 text-emerald-600 rounded-xl flex items-center justify-center mb-4">
              <Swords size={24} />
            </div>
            <h3 className="text-xl font-bold mb-2">Multiple Modes</h3>
            <p className="text-gray-600">Play Player vs AI, Player vs Player (Hotseat), or watch AI vs AI battles.</p>
          </div>
          
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-amber-100 text-amber-600 rounded-xl flex items-center justify-center mb-4">
              <Trophy size={24} />
            </div>
            <h3 className="text-xl font-bold mb-2">Detailed Analysis</h3>
            <p className="text-gray-600">See real-time analytics: evaluation scores, search depth, and node counts.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
