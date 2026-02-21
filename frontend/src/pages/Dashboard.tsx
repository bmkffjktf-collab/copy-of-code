import React, { useState, useEffect } from 'react'
import { citiesAPI, intersectionsAPI } from '../utils/api'
import { City, Intersection } from '../types'
import './Dashboard.css'

interface DashboardProps {
  onSelectIntersection: (intersectionId: number) => void
}

export default function Dashboard({ onSelectIntersection }: DashboardProps) {
  const [cities, setCities] = useState<City[]>([])
  const [selectedCity, setSelectedCity] = useState<City | null>(null)
  const [intersections, setIntersections] = useState<Intersection[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    console.log('Dashboard mounted, fetching cities...')
    fetchCities()
  }, [])

  const fetchCities = async () => {
    try {
      setError(null)
      setLoading(true)
      console.log('Fetching cities from API...')
      const response = await citiesAPI.getAll()
      console.log('Cities fetched successfully:', response.data)
      setCities(response.data)
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error)
      console.error('Error fetching cities:', errorMsg, error)
      setError(`Failed to fetch cities: ${errorMsg}`)
    } finally {
      setLoading(false)
    }
  }

  const handleSelectCity = async (city: City) => {
    setSelectedCity(city)
    try {
      setError(null)
      setLoading(true)
      console.log('Fetching intersections for city:', city.id)
      const response = await intersectionsAPI.getAll(city.id)
      console.log('Intersections fetched successfully:', response.data)
      setIntersections(response.data)
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error)
      console.error('Error fetching intersections:', errorMsg, error)
      setError(`Failed to fetch intersections: ${errorMsg}`)
    } finally {
      setLoading(false)
    }
  }

  if (error) {
    return (
      <div className="dashboard error">
        <div className="error-message">
          <h2>Error</h2>
          <p>{error}</p>
          <button onClick={() => {
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
      <div className="dashboard-container">
        <div className="cities-section">
          <h2>Indian Cities</h2>
          {loading && cities.length === 0 ? (
            <p>Loading cities...</p>
          ) : cities.length > 0 ? (
            <div className="cities-grid">
              {cities.map((city) => (
                <div
                  key={city.id}
                  className={`city-card ${selectedCity?.id === city.id ? 'selected' : ''}`}
                  onClick={() => handleSelectCity(city)}
                >
                  <h3>{city.name}</h3>
                  <p className="state">{city.state}</p>
                  <p className="population">{city.population}</p>
                </div>
              ))}
            </div>
          ) : (
            <p>No cities available</p>
          )}
        </div>

        {selectedCity && (
          <div className="intersections-section">
            <h2>Intersections in {selectedCity.name}</h2>
            <div className="intersections-grid">
              {loading ? (
                <p>Loading intersections...</p>
              ) : intersections.length > 0 ? (
                intersections.map((intersection) => (
                  <div key={intersection.id} className="intersection-card">
                    <h3>{intersection.name}</h3>
                    <p className="location">
                      {intersection.latitude.toFixed(4)}, {intersection.longitude.toFixed(4)}
                    </p>
                    <p className="lanes">Lanes: {intersection.num_lanes}</p>
                    {intersection.description && <p className="description">{intersection.description}</p>}
                    <button
                      className="btn-simulate"
                      onClick={() => onSelectIntersection(intersection.id)}
                    >
                      Start Simulation
                    </button>
                  </div>
                ))
              ) : (
                <p>No intersections found</p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
