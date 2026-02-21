import React from 'react'
import './Header.css'

interface HeaderProps {
  onBackClick?: () => void
}

export default function Header({ onBackClick }: HeaderProps) {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo-section">
          <h1 className="logo">🚦 Traffic Management</h1>
          <p className="tagline">AI-Powered Traffic Simulation for Indian Cities</p>
        </div>
        <nav className="nav">
          {onBackClick ? (
            <button onClick={onBackClick} className="nav-link-btn">
              ← Back to Dashboard
            </button>
          ) : (
            <a href="/" className="nav-link">Dashboard</a>
          )}
        </nav>
      </div>
    </header>
  )
}
