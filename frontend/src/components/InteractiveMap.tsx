import React, { useState, useEffect } from 'react'
import { City, Intersection } from '../types'
import { intersectionsAPI } from '../utils/api'
import './InteractiveMap.css'

interface InteractiveMapProps {
  city: City
  onSelectIntersection: (intersection: Intersection) => void
  selectedIntersection?: Intersection | null
}

export default function InteractiveMap({ city, onSelectIntersection, selectedIntersection }: InteractiveMapProps) {
  const [intersections, setIntersections] = useState<Intersection[]>([])
  const [loading, setLoading] = useState(true)
  const [hoveredId, setHoveredId] = useState<number | null>(null)

  useEffect(() => {
    fetchIntersections()
  }, [city.id])

  const fetchIntersections = async () => {
    try {
      setLoading(true)
      const response = await intersectionsAPI.getAll(city.id)
      setIntersections(response.data)
    } catch (error) {
      console.error('Error fetching intersections:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="interactive-map loading">Loading intersections...</div>
  }

  // Calculate bounds for the map
  const lats = intersections.map(i => i.latitude)
  const lons = intersections.map(i => i.longitude)
  const minLat = Math.min(...lats)
  const maxLat = Math.max(...lats)
  const minLon = Math.min(...lons)
  const maxLon = Math.max(...lons)
  const latRange = maxLat - minLat || 0.01
  const lonRange = maxLon - minLon || 0.01

  // SVG dimensions
  const WIDTH = 800
  const HEIGHT = 600
  const PADDING = 40

  // Convert lat/lon to SVG coordinates
  const toSvgCoords = (lat: number, lon: number) => {
    const x = PADDING + ((lon - minLon) / lonRange) * (WIDTH - 2 * PADDING)
    const y = HEIGHT - PADDING - ((lat - minLat) / latRange) * (HEIGHT - 2 * PADDING)
    return { x, y }
  }

  return (
    <div className="interactive-map">
      <div className="map-container">
        <svg className="map-svg" width={WIDTH} height={HEIGHT} viewBox={`0 0 ${WIDTH} ${HEIGHT}`}>
          {/* Background */}
          <defs>
            <linearGradient id="mapGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#f9f9fb" />
              <stop offset="100%" stopColor="#ffffff" />
            </linearGradient>
            <filter id="shadow">
              <feDropShadow dx="0" dy="2" stdDeviation="4" floodOpacity="0.15" />
            </filter>
          </defs>

          <rect width={WIDTH} height={HEIGHT} fill="url(#mapGradient)" />

          {/* Grid lines */}
          <g stroke="#e5e5e7" strokeWidth="1" opacity="0.3">
            {Array.from({ length: 5 }).map((_, i) => (
              <React.Fragment key={`grid-${i}`}>
                <line
                  x1={PADDING + (i * (WIDTH - 2 * PADDING)) / 4}
                  y1={PADDING}
                  x2={PADDING + (i * (WIDTH - 2 * PADDING)) / 4}
                  y2={HEIGHT - PADDING}
                />
                <line
                  x1={PADDING}
                  y1={PADDING + (i * (HEIGHT - 2 * PADDING)) / 4}
                  x2={WIDTH - PADDING}
                  y2={PADDING + (i * (HEIGHT - 2 * PADDING)) / 4}
                />
              </React.Fragment>
            ))}
          </g>

          {/* Axis labels */}
          <text x={WIDTH / 2} y={HEIGHT - 10} textAnchor="middle" fontSize="12" fill="#86868b">
            Longitude
          </text>
          <text x="15" y={HEIGHT / 2} textAnchor="middle" fontSize="12" fill="#86868b" transform={`rotate(-90 15 ${HEIGHT / 2})`}>
            Latitude
          </text>

          {/* Intersections - connections */}
          {intersections.map((intersection, idx) => {
            if (idx < intersections.length - 1) {
              const start = toSvgCoords(intersection.latitude, intersection.longitude)
              const end = toSvgCoords(intersections[idx + 1].latitude, intersections[idx + 1].longitude)
              return (
                <line
                  key={`line-${idx}`}
                  x1={start.x}
                  y1={start.y}
                  x2={end.x}
                  y2={end.y}
                  stroke="#0071e3"
                  strokeWidth="2"
                  opacity="0.2"
                />
              )
            }
            return null
          })}

          {/* Intersections - circles */}
          {intersections.map(intersection => {
            const coords = toSvgCoords(intersection.latitude, intersection.longitude)
            const isSelected = selectedIntersection?.id === intersection.id
            const isHovered = hoveredId === intersection.id

            return (
              <g key={`junction-${intersection.id}`}>
                {/* Outer glow effect */}
                {isSelected && (
                  <circle
                    cx={coords.x}
                    cy={coords.y}
                    r="16"
                    fill="none"
                    stroke="#0071e3"
                    strokeWidth="2"
                    opacity="0.3"
                    className="glow-circle"
                  />
                )}

                {/* Main circle */}
                <circle
                  cx={coords.x}
                  cy={coords.y}
                  r={isSelected ? 8 : isHovered ? 7 : 6}
                  fill={isSelected ? '#0071e3' : isHovered ? '#0071e3' : '#f5f5f7'}
                  stroke={isSelected ? '#ffffff' : '#0071e3'}
                  strokeWidth={isSelected ? 3 : 2}
                  className={`junction-circle ${isSelected ? 'selected' : ''} ${isHovered ? 'hovered' : ''}`}
                  style={{ cursor: 'pointer' }}
                  onClick={() => onSelectIntersection(intersection)}
                  onMouseEnter={() => setHoveredId(intersection.id)}
                  onMouseLeave={() => setHoveredId(null)}
                  filter="url(#shadow)"
                />
              </g>
            )
          })}
        </svg>

        {/* Legend */}
        <div className="map-legend">
          <div className="legend-item">
            <div className="legend-icon" style={{ backgroundColor: '#0071e3' }}></div>
            <span>Traffic Junction</span>
          </div>
          <div className="legend-item">
            <div className="legend-icon" style={{ backgroundColor: '#34c759' }}></div>
            <span>Selected</span>
          </div>
        </div>
      </div>

      {/* Intersections list */}
      <div className="intersections-list">
        <h3>Road Junctions in {city.name}</h3>
        <div className="junctions-grid">
          {intersections.map(intersection => (
            <div
              key={intersection.id}
              className={`junction-card ${selectedIntersection?.id === intersection.id ? 'selected' : ''}`}
              onClick={() => onSelectIntersection(intersection)}
              onMouseEnter={() => setHoveredId(intersection.id)}
              onMouseLeave={() => setHoveredId(null)}
            >
              <div className="junction-card-header">
                <h4>{intersection.name}</h4>
                <div className="junction-badge">{intersection.num_lanes} lanes</div>
              </div>
              <div className="junction-card-coords">
                <small>📍 {intersection.latitude.toFixed(4)}, {intersection.longitude.toFixed(4)}</small>
              </div>
              <button className="select-btn">Select</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
