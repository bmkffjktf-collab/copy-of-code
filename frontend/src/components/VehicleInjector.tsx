import React, { useState } from 'react'
import { vehiclesAPI } from '../utils/api'
import './VehicleInjector.css'

interface VehicleInjectorProps {
  intersectionId: number
  onVehicleAdded: () => void
}

const VEHICLE_TYPES = ['CAR', 'BUS', 'TRUCK', 'TWO_WHEELER', 'AUTO', 'AMBULANCE', 'FIRE_ENGINE', 'POLICE']
const LANES = [
  { id: 1, name: 'North' },
  { id: 2, name: 'South' },
  { id: 3, name: 'East' },
  { id: 4, name: 'West' },
]

export default function VehicleInjector({ intersectionId, onVehicleAdded }: VehicleInjectorProps) {
  const [selectedVehicle, setSelectedVehicle] = useState('CAR')
  const [selectedLane, setSelectedLane] = useState(1)
  const [isEmergency, setIsEmergency] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleInjectVehicle = async () => {
    try {
      setLoading(true)
      await vehiclesAPI.inject({
        vehicle_type: selectedVehicle,
        intersection_id: intersectionId,
        lane_id: selectedLane,
        is_emergency: isEmergency,
      })
      onVehicleAdded()
    } catch (error) {
      console.error('Error injecting vehicle:', error)
      alert('Failed to inject vehicle')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="vehicle-injector">
      <h3>Inject Vehicle</h3>

      <div className="form-group">
        <label>Vehicle Type</label>
        <select value={selectedVehicle} onChange={(e) => setSelectedVehicle(e.target.value)}>
          {VEHICLE_TYPES.map((type) => (
            <option key={type} value={type}>
              {type.replace('_', ' ')}
            </option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label>Lane</label>
        <select value={selectedLane} onChange={(e) => setSelectedLane(Number(e.target.value))}>
          {LANES.map((lane) => (
            <option key={lane.id} value={lane.id}>
              {lane.name}
            </option>
          ))}
        </select>
      </div>

      <div className="form-group checkbox">
        <input type="checkbox" id="emergency" checked={isEmergency} onChange={(e) => setIsEmergency(e.target.checked)} />
        <label htmlFor="emergency">Emergency Vehicle</label>
      </div>

      <button onClick={handleInjectVehicle} disabled={loading} className="btn-inject">
        {loading ? 'Injecting...' : '+ Add Vehicle'}
      </button>
    </div>
  )
}
