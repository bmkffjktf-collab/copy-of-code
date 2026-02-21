import React from 'react'
import { Intersection, Vehicle, SimulationMetrics } from '../types'
import './LiveDashboard.css'

interface LiveDashboardProps {
  intersection: Intersection
  metrics: SimulationMetrics | null
  vehicles: Vehicle[]
  isRunning: boolean
}

export default function LiveDashboard({ intersection, metrics, vehicles, isRunning }: LiveDashboardProps) {
  const getMetricColor = (value: number, max: number = 100) => {
    if (value < 30) return '#28a745'
    if (value < 60) return '#ffc107'
    return '#dc3545'
  }

  return (
    <div className="live-dashboard">
      <h3>Live Metrics & Analytics</h3>

      <div className="status-bar">
        <div className={`status-indicator ${isRunning ? 'running' : 'stopped'}`}></div>
        <span>{isRunning ? 'Simulation Running' : 'Simulation Stopped'}</span>
      </div>

      {metrics ? (
        <>
          <div className="metrics-grid">
            <div className="metric-card">
              <div className="metric-label">Total Vehicles</div>
              <div className="metric-value">{metrics.total_vehicles}</div>
              <div className="metric-subtext">Active in intersection</div>
            </div>

            <div className="metric-card">
              <div className="metric-label">Exited Vehicles</div>
              <div className="metric-value">{metrics.vehicles_exited}</div>
              <div className="metric-subtext">Left intersection</div>
            </div>

            <div className="metric-card">
              <div className="metric-label">Avg Wait Time</div>
              <div className="metric-value">{metrics.avg_waiting_time.toFixed(1)}s</div>
              <div className="metric-subtext">Per vehicle</div>
            </div>

            <div className="metric-card">
              <div className="metric-label">Vehicles/Min</div>
              <div className="metric-value">{metrics.vehicles_per_minute.toFixed(1)}</div>
              <div className="metric-subtext">Throughput</div>
            </div>
          </div>

          <div className="congestion-section">
            <div className="congestion-label">Congestion Level</div>
            <div className="congestion-bar">
              <div
                className="congestion-fill"
                style={{
                  width: `${metrics.congestion_score}%`,
                  backgroundColor: getMetricColor(metrics.congestion_score),
                }}
              ></div>
            </div>
            <div className="congestion-value">{metrics.congestion_score.toFixed(1)}%</div>
          </div>

          <div className="simulation-time">
            <div className="label">Simulation Time</div>
            <div className="value">{metrics.simulation_time.toFixed(1)}s</div>
          </div>

          <div className="vehicles-section">
            <div className="section-title">Active Vehicles</div>
            <div className="vehicles-list">
              {vehicles.length > 0 ? (
                <div className="vehicle-summary">
                  <p>
                    <strong>{vehicles.filter((v) => v.state === 'MOVING').length}</strong> Moving
                  </p>
                  <p>
                    <strong>{vehicles.filter((v) => v.state === 'STOPPED').length}</strong> Stopped
                  </p>
                  <p>
                    <strong>{vehicles.filter((v) => v.state === 'WAITING').length}</strong> Waiting
                  </p>
                  <p>
                    <strong>{vehicles.filter((v) => v.is_emergency).length}</strong> Emergency
                  </p>
                </div>
              ) : (
                <p className="no-vehicles">No active vehicles</p>
              )}
            </div>
          </div>
        </>
      ) : (
        <p className="no-metrics">No metrics available</p>
      )}
    </div>
  )
}
