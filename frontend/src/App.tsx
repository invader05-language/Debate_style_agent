import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import DebatePage from './pages/DebatePage';
import HistoryPage from './pages/HistoryPage';
import MemoryPage from './pages/MemoryPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold text-gray-900">
                Multi-AI Debate Agent
              </h1>
              <nav className="flex space-x-4">
                <Link
                  to="/"
                  className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg"
                >
                  新辩论
                </Link>
                <Link
                  to="/history"
                  className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg"
                >
                  历史记录
                </Link>
                <Link
                  to="/memories"
                  className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg"
                >
                  记忆库
                </Link>
              </nav>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<DebatePage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/memories" element={<MemoryPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
