import React, { useState } from 'react'
import Header from './components/Header'
import Dashboard from './pages/Dashboard'
import SimulationPage from './pages/SimulationPage'
import './App.css'

type Page = 'dashboard' | 'simulation'

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('dashboard')
  const [selectedIntersectionId, setSelectedIntersectionId] = useState<number | null>(null)

  const handleStartSimulation = (intersectionId: number) => {
    setSelectedIntersectionId(intersectionId)
    setCurrentPage('simulation')
  }

  const handleBackToDashboard = () => {
    setCurrentPage('dashboard')
    setSelectedIntersectionId(null)
  }

  return (
    <div className="app">
      <Header onBackClick={currentPage === 'simulation' ? handleBackToDashboard : undefined} />
      <main className="app-content">
        {currentPage === 'dashboard' ? (
          <Dashboard onSelectIntersection={handleStartSimulation} />
        ) : (
          <SimulationPage intersectionId={selectedIntersectionId!} onBack={handleBackToDashboard} />
        )}
      </main>
    </div>
  )
}

export default App
