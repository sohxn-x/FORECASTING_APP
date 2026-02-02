import { useState } from 'react';
import HomePage from './pages/HomePage';
import PredictionsPage from './pages/PredictionsPage';
import CalculatorPage from './pages/CalculatorPage';

type Page = 'home' | 'predictions' | 'calculator';

export default function App() {
  const [currentPage, setCurrentPage] = useState<Page>('home');

  const handleNavigate = (page: Page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      {currentPage === 'home' && <HomePage onNavigate={handleNavigate} />}
      {currentPage === 'predictions' && <PredictionsPage onNavigate={handleNavigate} />}
      {currentPage === 'calculator' && <CalculatorPage onNavigate={handleNavigate} />}
    </div>
  );
}
