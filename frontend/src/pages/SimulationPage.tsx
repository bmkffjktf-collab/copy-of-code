import React, { useState, useEffect } from 'react'
import { intersectionsAPI, vehiclesAPI, simulationAPI } from '../utils/api'
import { Intersection, Vehicle, SimulationMetrics } from '../types'
import TrafficMap from '../components/TrafficMap'
import VehicleInjector from '../components/VehicleInjector'
import LiveDashboard from '../components/LiveDashboard'
import './SimulationPage.css'

interface SimulationPageProps {
  intersectionId: number
  onBack: () => void
}

export default function SimulationPage({ intersectionId, onBack }: SimulationPageProps) {
  const [intersection, setIntersection] = useState<Intersection | null>(null)
  const [vehicles, setVehicles] = useState<Vehicle[]>([])
  const [metrics, setMetrics] = useState<SimulationMetrics | null>(null)
  const [isRunning, setIsRunning] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchIntersection()
  }, [intersectionId])

  useEffect(() => {
    let interval: NodeJS.Timeout

    if (isRunning) {
      interval = setInterval(() => {
        fetchVehicles()
        fetchMetrics()
      }, 500)
    }

    return () => clearInterval(interval)
  }, [isRunning, intersectionId])

  const fetchIntersection = async () => {
    try {
      const response = await intersectionsAPI.getById(intersectionId)
      setIntersection(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching intersection:', error)
      setLoading(false)
    }
  }

  const fetchVehicles = async () => {
    try {
      const response = await vehiclesAPI.getAll(intersectionId)
      setVehicles(response.data)
    } catch (error) {
      console.error('Error fetching vehicles:', error)
    }
  }

  const fetchMetrics = async () => {
    try {
      const response = await simulationAPI.getMetrics(intersectionId)
      setMetrics(response.data)
    } catch (error) {
      console.error('Error fetching metrics:', error)
    }
  }

  const handleStartSimulation = async () => {
    try {
      await simulationAPI.start(intersectionId)
      setIsRunning(true)
      fetchVehicles()
      fetchMetrics()
    } catch (error) {
      console.error('Error starting simulation:', error)
    }
  }

  const handleStopSimulation = async () => {
    try {
      await simulationAPI.stop(intersectionId)
      setIsRunning(false)
    } catch (error) {
      console.error('Error stopping simulation:', error)
    }
  }

  const handleOptimizeSignals = async () => {
    try {
      await simulationAPI.optimize(intersectionId)
    } catch (error) {
      console.error('Error optimizing signals:', error)
    }
  }

  if (loading) {
    return <div className="simulation-page"><p>Loading...</p></div>
  }

  if (!intersection) {
    return <div className="simulation-page"><p>Intersection not found</p></div>
  }

  return (
    <div className="simulation-page">
      <div className="simulation-header">
        <h1>{intersection.name}</h1>
        <button onClick={onBack} className="btn-back">
          ← Back
        </button>
      </div>

      <div className="simulation-container">
        <div className="left-panel">
          <TrafficMap intersection={intersection} vehicles={vehicles} />
          <VehicleInjector intersectionId={intersectionId} onVehicleAdded={fetchVehicles} />
        </div>

        <div className="right-panel">
          <div className="controls">
            {!isRunning ? (
              <button onClick={handleStartSimulation} className="btn-start">
                ▶ Start Simulation
              </button>
            ) : (
              <button onClick={handleStopSimulation} className="btn-stop">
                ⏹ Stop Simulation
              </button>
            )}
            <button onClick={handleOptimizeSignals} className="btn-optimize">
              ⚙ Optimize Signals
            </button>
          </div>

          <LiveDashboard intersection={intersection} metrics={metrics} vehicles={vehicles} isRunning={isRunning} />
        </div>
      </div>
    </div>
  )
}
