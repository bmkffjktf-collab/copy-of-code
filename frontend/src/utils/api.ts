import axios from 'axios'
import { City, Intersection, Vehicle, SimulationMetrics } from '../types'

// Determine API base URL
const getApiBaseUrl = (): string => {
  // First check for explicit configuration from config.js
  if (typeof window !== 'undefined' && (window as any).API_CONFIG?.apiUrl) {
    const baseUrl = (window as any).API_CONFIG.apiUrl;
    if (baseUrl) {
      return baseUrl;
    }
  }

  // For development with proxying (localhost:5173 with Vite dev server)
  // use relative path which proxy will handle
  if (window.location.hostname === 'localhost' && window.location.port === '5173') {
    return '';
  }

  // For development accessing directly
  if (window.location.hostname === 'localhost') {
    return 'http://localhost:8000';
  }

  // For production, use relative path (assumes reverse proxy)
  return '';
};

const API_BASE_URL = getApiBaseUrl()
const API_PREFIX = '/api'

console.log('🔌 API Configuration:', {
  baseURL: API_BASE_URL,
  prefix: API_PREFIX,
  fullURL: API_BASE_URL + API_PREFIX,
  hostname: window.location.hostname,
  port: window.location.port,
});

const api = axios.create({
  baseURL: API_BASE_URL + API_PREFIX,
})

// Cities API
export const citiesAPI = {
  getAll: () => api.get<City[]>('/cities'),
  getById: (id: number) => api.get<City>(`/cities/${id}`),
  create: (data: Partial<City>) => api.post<City>('/cities', data),
  update: (id: number, data: Partial<City>) => api.put<City>(`/cities/${id}`, data),
  delete: (id: number) => api.delete(`/cities/${id}`),
}

// Intersections API
export const intersectionsAPI = {
  getAll: (cityId?: number) => api.get<Intersection[]>('/intersections', { params: { city_id: cityId } }),
  getById: (id: number) => api.get<Intersection>(`/intersections/${id}`),
  create: (data: Partial<Intersection>) => api.post<Intersection>('/intersections', data),
  update: (id: number, data: Partial<Intersection>) => api.put<Intersection>(`/intersections/${id}`, data),
  delete: (id: number) => api.delete(`/intersections/${id}`),
}

// Vehicles API
export const vehiclesAPI = {
  getAll: (intersectionId?: number) => api.get<Vehicle[]>('/vehicles', { params: { intersection_id: intersectionId } }),
  getById: (id: number) => api.get<Vehicle>(`/vehicles/${id}`),
  inject: (data: { vehicle_type: string; intersection_id: number; lane_id: number; is_emergency?: boolean }) =>
    api.post<Vehicle>('/vehicles/inject', data),
}

// Simulation API
export const simulationAPI = {
  start: (intersectionId: number, duration: number = 300, speedFactor: number = 1.0) =>
    api.post('/simulation/start', { intersection_id: intersectionId, duration, speed_factor: speedFactor }),
  stop: (intersectionId: number) => api.post(`/simulation/stop/${intersectionId}`),
  optimize: (intersectionId: number) => api.post(`/simulation/optimize/${intersectionId}`),
  getMetrics: (intersectionId: number) => api.get<SimulationMetrics>(`/simulation/metrics/${intersectionId}`),
  step: (intersectionId: number, dt?: number) => api.post(`/simulation/step/${intersectionId}`, { dt }),
}

export default api
