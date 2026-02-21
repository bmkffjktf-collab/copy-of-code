import React, { useState, useEffect } from 'react'
import { citiesAPI, intersectionsAPI } from '../utils/api'
import { City, Intersection } from '../types'
import './Dashboard.css'

interface DashboardProps {
  onSelectIntersection: (intersectionId: number) => void
}

export default function Dashboard({ onSelectIntersection }: DashboardProps) {
  const [cities, setCities] = useState<City[]>([])
  const [allIntersections, setAllIntersections] = useState<Intersection[]>([])
  const [selectedIntersection, setSelectedIntersection] = useState<Intersection | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    fetchAllData()
  }, [])

  const fetchAllData = async () => {
    try {
      setError(null)
      setLoading(true)
      
      // Fetch all cities
      const citiesResponse = await citiesAPI.getAll()
      setCities(citiesResponse.data)
      
      // Fetch junctions from all cities
      const allJunctions: Intersection[] = []
      for (const city of citiesResponse.data) {
        const response = await intersectionsAPI.getAll(city.id)
        allJunctions.push(...response.data)
      }
      setAllIntersections(allJunctions)
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error)
      console.error('Error fetching data:', errorMsg)
      setError(`Failed to fetch data: ${errorMsg}`)
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

  const filteredIntersections = allIntersections.filter(j =>
    j.name.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const getCity = (intersection: Intersection) => {
    return cities.find(c => c.id === (allIntersections.find(i => i.id === intersection.id)?.city_id))
  }

  if (error) {
    return (
      <div className="dashboard error">
        <div className="error-message">
          <h2>⚠️ Error</h2>
          <p>{error}</p>
          <button className="btn-retry" onClick={() => {
            setError(null)
            fetchAllData()
          }}>
            Retry
          </button>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="dashboard loading">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading traffic data...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div className="header-content">
          <h1>🗺️ Traffic Junction Selector</h1>
          <p>Select any road junction to start simulation</p>
        </div>
      </div>

      <div className="dashboard-body">
        <main className="map-section">
          {/* Map Visualization */}
          <div className="map-container">
            <svg className="map-svg" viewBox="0 0 800 600" preserveAspectRatio="xMidYMid meet">
              <defs>
                <linearGradient id="darkGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#1a1a2e" />
                  <stop offset="100%" stopColor="#16213e" />
                </linearGradient>
                <filter id="darkShadow">
                  <feDropShadow dx="0" dy="2" stdDeviation="4" floodOpacity="0.4" />
                </filter>
              </defs>

              {/* Background */}
              <rect width="800" height="600" fill="url(#darkGradient)" />

              {/* Grid lines */}
              <g stroke="#444" strokeWidth="1" opacity="0.5">
                {Array.from({ length: 5 }).map((_, i) => (
                  <React.Fragment key={`grid-${i}`}>
                    <line x1={40 + (i * 720) / 4} y1="40" x2={40 + (i * 720) / 4} y2="560" />
                    <line x1="40" y1={40 + (i * 520) / 4} x2="760" y2={40 + (i * 520) / 4} />
                  </React.Fragment>
                ))}
              </g>

              {/* Calculate bounds */}
              {allIntersections.length > 0 && (() => {
                const lats = allIntersections.map(i => i.latitude)
                const lons = allIntersections.map(i => i.longitude)
                const minLat = Math.min(...lats)
                const maxLat = Math.max(...lats)
                const minLon = Math.min(...lons)
                const maxLon = Math.max(...lons)
                const latRange = (maxLat - minLat) || 0.01
                const lonRange = (maxLon - minLon) || 0.01

                const toSvgCoords = (lat: number, lon: number) => {
                  const x = 40 + ((lon - minLon) / lonRange) * 720
                  const y = 560 - ((lat - minLat) / latRange) * 520
                  return { x, y }
                }

                return (
                  <>
                    {/* Connection lines */}
                    {allIntersections.map((intersection, idx) => {
                      if (idx < allIntersections.length - 1) {
                        const start = toSvgCoords(intersection.latitude, intersection.longitude)
                        const end = toSvgCoords(allIntersections[idx + 1].latitude, allIntersections[idx + 1].longitude)
                        return (
                          <line
                            key={`line-${idx}`}
                            x1={start.x}
                            y1={start.y}
                            x2={end.x}
                            y2={end.y}
                            stroke="#00d4ff"
                            strokeWidth="1.5"
                            opacity="0.3"
                          />
                        )
                      }
                      return null
                    })}

                    {/* Junction circles */}
                    {allIntersections.map(intersection => {
                      const coords = toSvgCoords(intersection.latitude, intersection.longitude)
                      const isSelected = selectedIntersection?.id === intersection.id
                      return (
                        <g key={`junction-${intersection.id}`}>
                          {isSelected && (
                            <circle
                              cx={coords.x}
                              cy={coords.y}
                              r="20"
                              fill="none"
                              stroke="#00ff88"
                              strokeWidth="2"
                              opacity="0.6"
                              className="pulse-ring"
                            />
                          )}
                          <circle
                            cx={coords.x}
                            cy={coords.y}
                            r={isSelected ? 9 : 6}
                            fill={isSelected ? '#00ff88' : '#00d4ff'}
                            stroke={isSelected ? '#ffffff' : '#00d4ff'}
                            strokeWidth={isSelected ? 2 : 1}
                            className="junction-circle"
                            style={{ cursor: 'pointer' }}
                            onClick={() => handleSelectIntersection(intersection)}
                            filter="url(#darkShadow)"
                          />
                        </g>
                      )
                    })}
                  </>
                )
              })()}
            </svg>
          </div>

          {/* Search and Info */}
          <div className="map-info">
            <div className="search-box">
              <input
                type="text"
                placeholder="🔍 Search junctions..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="search-input"
              />
              <span className="junction-count">{filteredIntersections.length} junctions</span>
            </div>
          </div>
        </main>

        <aside className="junctions-sidebar">
          <h3>Road Junctions</h3>
          
          <div className="junctions-scroll">
            {filteredIntersections.length > 0 ? (
              filteredIntersections.map(intersection => {
                const city = cities.find(c => c.id === intersection.city_id)
                const isSelected = selectedIntersection?.id === intersection.id
                return (
                  <div
                    key={intersection.id}
                    className={`junction-entry ${isSelected ? 'selected' : ''}`}
                    onClick={() => handleSelectIntersection(intersection)}
                  >
                    <div className="junction-entry-header">
                      <h4>{intersection.name}</h4>
                      <span className="lane-badge">{intersection.num_lanes}L</span>
                    </div>
                    <p className="junction-city">{city?.name || 'Unknown'}</p>
                    <p className="junction-coords">
                      📍 {intersection.latitude.toFixed(3)}, {intersection.longitude.toFixed(3)}
                    </p>
                  </div>
                )
              })
            ) : (
              <p className="no-results">No junctions found</p>
            )}
          </div>
        </aside>

        {selectedIntersection && (
          <div className="selection-panel">
            <div className="selected-info">
              <h4>Selected Junction</h4>
              <p className="junction-name">{selectedIntersection.name}</p>
              <div className="junction-details">
                <div className="detail-item">
                  <span className="label">City:</span>
                  <span className="value">{cities.find(c => c.id === selectedIntersection.city_id)?.name}</span>
                </div>
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
      </div>
    </div>
  )
}
