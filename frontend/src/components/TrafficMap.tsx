import React, { useEffect, useRef } from 'react'
import mapboxgl from 'mapbox-gl'
import { Intersection, Vehicle } from '../types'
import './TrafficMap.css'

interface TrafficMapProps {
  intersection: Intersection
  vehicles: Vehicle[]
}

export default function TrafficMap({ intersection, vehicles }: TrafficMapProps) {
  const mapContainer = useRef<HTMLDivElement>(null)
  const map = useRef<mapboxgl.Map | null>(null)

  useEffect(() => {
    if (!mapContainer.current) return

    // Create a simple canvas-based map visualization
    const canvas = document.createElement('canvas')
    canvas.width = mapContainer.current.clientWidth
    canvas.height = mapContainer.current.clientHeight

    mapContainer.current.innerHTML = ''
    mapContainer.current.appendChild(canvas)

    draw(canvas.getContext('2d')!, intersection, vehicles)

    window.addEventListener('resize', () => {
      canvas.width = mapContainer.current!.clientWidth
      canvas.height = mapContainer.current!.clientHeight
      draw(canvas.getContext('2d')!, intersection, vehicles)
    })
  }, [intersection, vehicles])

  const draw = (ctx: CanvasRenderingContext2D, intersection: Intersection, vehicles: Vehicle[]) => {
    const width = ctx.canvas.width
    const height = ctx.canvas.height

    // Clear canvas
    ctx.fillStyle = '#f0f0f0'
    ctx.fillRect(0, 0, width, height)

    // Draw intersection
    const centerX = width / 2
    const centerY = height / 2
    const roadSize = 100

    // Draw roads
    ctx.fillStyle = '#333333'
    ctx.fillRect(0, centerY - 20, width, 40) // Horizontal road
    ctx.fillRect(centerX - 20, 0, 40, height) // Vertical road

    // Draw intersection
    ctx.fillStyle = '#666666'
    ctx.fillRect(centerX - 20, centerY - 20, 40, 40)

    // Draw lane markers
    ctx.strokeStyle = '#ffff00'
    ctx.lineWidth = 2
    ctx.setLineDash([10, 10])

    // Horizontal lines
    ctx.beginPath()
    ctx.moveTo(0, centerY - 10)
    ctx.lineTo(width, centerY - 10)
    ctx.stroke()

    ctx.beginPath()
    ctx.moveTo(0, centerY + 10)
    ctx.lineTo(width, centerY + 10)
    ctx.stroke()

    // Vertical lines
    ctx.beginPath()
    ctx.moveTo(centerX - 10, 0)
    ctx.lineTo(centerX - 10, height)
    ctx.stroke()

    ctx.beginPath()
    ctx.moveTo(centerX + 10, 0)
    ctx.lineTo(centerX + 10, height)
    ctx.stroke()

    ctx.setLineDash([])

    // Draw intersection name
    ctx.fillStyle = '#000'
    ctx.font = '14px Arial'
    ctx.textAlign = 'center'
    ctx.fillText(intersection.name, centerX, 30)

    // Draw vehicles
    vehicles.forEach((vehicle) => {
      const vehicleX = Math.random() * width
      const vehicleY = Math.random() * height

      if (vehicle.is_emergency) {
        ctx.fillStyle = '#ff4444'
      } else if (vehicle.state === 'STOPPED') {
        ctx.fillStyle = '#ffaa00'
      } else if (vehicle.state === 'MOVING') {
        ctx.fillStyle = '#44aa44'
      } else {
        ctx.fillStyle = '#4444ff'
      }

      ctx.fillRect(vehicleX - 10, vehicleY - 8, 20, 16)

      // Draw vehicle label
      ctx.fillStyle = '#fff'
      ctx.font = 'bold 10px Arial'
      ctx.textAlign = 'center'
      ctx.fillText(vehicle.vehicle_type[0], vehicleX, vehicleY + 5)
    })

    // Draw legend
    ctx.font = '12px Arial'
    ctx.textAlign = 'left'
    const legendX = 20
    const legendY = height - 120

    ctx.fillStyle = '#000'
    ctx.fillText('Legend:', legendX, legendY)

    ctx.fillStyle = '#44aa44'
    ctx.fillRect(legendX, legendY + 10, 15, 15)
    ctx.fillStyle = '#000'
    ctx.fillText('Moving', legendX + 20, legendY + 22)

    ctx.fillStyle = '#ffaa00'
    ctx.fillRect(legendX, legendY + 35, 15, 15)
    ctx.fillStyle = '#000'
    ctx.fillText('Stopped', legendX + 20, legendY + 47)

    ctx.fillStyle = '#4444ff'
    ctx.fillRect(legendX, legendY + 60, 15, 15)
    ctx.fillStyle = '#000'
    ctx.fillText('Waiting', legendX + 20, legendY + 72)

    ctx.fillStyle = '#ff4444'
    ctx.fillRect(legendX, legendY + 85, 15, 15)
    ctx.fillStyle = '#000'
    ctx.fillText('Emergency', legendX + 20, legendY + 97)
  }

  return (
    <div className="traffic-map-container">
      <div ref={mapContainer} className="traffic-map" />
    </div>
  )
}
