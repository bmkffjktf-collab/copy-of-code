export interface City {
  id: number
  name: string
  state: string
  latitude: number
  longitude: number
  description?: string
  population?: string
}

export interface Lane {
  id: number
  name: string
  direction: 'NORTH' | 'SOUTH' | 'EAST' | 'WEST'
  capacity: number
  length: number
  width: number
  vehicle_count?: number
  congestion_score?: number
}

export interface Signal {
  id: number
  name: string
  state: 'GREEN' | 'YELLOW' | 'RED'
  remaining_time: number
  green_duration: number
  is_optimized: boolean
}

export interface Vehicle {
  id: number
  vehicle_id: string
  vehicle_type: string
  position: number
  speed: number
  state: 'WAITING' | 'MOVING' | 'STOPPED' | 'EXITED'
  is_emergency: boolean
  waiting_time: number
}

export interface Intersection {
  id: number
  name: string
  city_id: number
  latitude: number
  longitude: number
  num_lanes: number
  description?: string
}

export interface SimulationMetrics {
  simulation_time: number
  total_vehicles: number
  vehicles_exited: number
  avg_waiting_time: number
  congestion_score: number
  vehicles_per_minute: number
}
