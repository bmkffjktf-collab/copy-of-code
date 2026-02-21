import React, { useState, useEffect } from 'react'
import { citiesAPI } from '../utils/api'
import { City, Intersection } from '../types'
import InteractiveMap from '../components/InteractiveMap'
import './Dashboard.css'

interface DashboardProps {
  onSelectIntersection: (intersectionId: number) => void
}

export default function Dashboard({ onSelectIntersection }: DashboardProps) {
  const [cities, setCities] = useState<City[]>([])
  const [selectedCity, setSelectedCity] = useState<City | null>(null)
  const [selectedIntersection, setSelectedIntersection] = useState<Intersection | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchCities()
  }, [])

  const fetchCities = async () => {
    try {
      setError(null)
      setLoading(true)
      const response = await citiesAPI.getAll()
      setCities(response.data)
      if (response.data.length > 0) {
        setSelectedCity(response.data[0])
      }
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error)
      console.error('Error fetching cities:', errorMsg)
      setError(`Failed to fetch cities: ${errorMsg}`)
    } finally {
      setLoading(false)
    }
  }

  const handleSelectIntersection = (intersection: Intersection) => {
    setSelectedIntersection(intersection)
  }

  const handleStartSimulation = () => {
    if (selectedIntersection) {
      onSelectIntersection(selectedIntersection.id)
    }
  }

  if (error) {
    return (
      <div className="dashboard error">
        <div className="error-message">
          <h2>⚠️ Error</h2>
          <p>{error}</p>
          <button className="btn-retry" onClick={() => {
            setError(null)
            fetchCities()
          }}>
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div className="header-content">
          <h1>Traffic Management System</h1>
          <p>Select a city to explore road junctions and run simulations</p>
        </div>
      </div>

      <div className="dashboard-body">
        <aside className="cities-panel">
          <h3>Cities</h3>
          <div className="cities-list">
            {loading && cities.length === 0 ? (
              <p className="loading-text">Loading cities...</p>
            ) : cities.length > 0 ? (
              cities.map((city) => (
                <button
                  key={city.id}
                  className={`city-btn ${selectedCity?.id === city.id ? 'active' : ''}`}
                  onClick={() => {
                    setSelectedCity(city)
                    setSelectedIntersection(null)
                  }}
                >
                  <span className="city-name">{city.name}</span>
                  <span className="city-state">{city.state}</span>
                </button>
              ))
            ) : (
              <p className="no-data">No cities available</p>
            )}
          </div>
        </aside>

        <main className="map-section">
          {selectedCity ? (
            <>
              <InteractiveMap
                city={selectedCity}
                onSelectIntersection={handleSelectIntersection}
                selectedIntersection={selectedIntersection}
              />

              {selectedIntersection && (
                <div className="selection-panel">
                  <div className="selected-info">
                    <h4>Selected Junction</h4>
                    <p className="junction-name">{selectedIntersection.name}</p>
                    <div className="junction-details">
                      <div className="detail-item">
                        <span className="label">Lanes:</span>
                        <span className="value">{selectedIntersection.num_lanes}</span>
                      </div>
                      <div className="detail-item">
                        <span className="label">Location:</span>
                        <span className="value">{selectedIntersection.latitude.toFixed(4)}, {selectedIntersection.longitude.toFixed(4)}</span>
                      </div>
                    </div>
                  </div>
                  <button className="btn-simulate" onClick={handleStartSimulation}>
                    ▶ Start Simulation
                  </button>
                </div>
              )}
            </>
          ) : (
            <div className="no-city-selected">
              <p>Select a city to view its traffic junctions</p>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}
