import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import GameSetup from './pages/GameSetup';
import Game from './pages/Game';
import MatchHistory from './pages/MatchHistory';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 text-gray-800 font-sans">
        <header className="bg-white shadow-sm p-4 sticky top-0 z-10 glass-panel">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <a href="/" className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-emerald-500">
              Caro Online
            </a>
            <nav className="space-x-4">
              <a href="/" className="hover:text-indigo-500 font-medium transition-colors">Home</a>
              <a href="/setup" className="hover:text-indigo-500 font-medium transition-colors">Play</a>
              <a href="/history" className="hover:text-indigo-500 font-medium transition-colors">History</a>
            </nav>
          </div>
        </header>
        
        <main className="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/setup" element={<GameSetup />} />
            <Route path="/game" element={<Game />} />
            <Route path="/history" element={<MatchHistory />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
