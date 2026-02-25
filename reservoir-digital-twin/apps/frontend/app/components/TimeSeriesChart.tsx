"use client";
import React from 'react'

type Point = { t: string; v: number }
export default function TimeSeriesChart({ data }: { data: Point[] }) {
  const w = 360
  const h = 120
  // simple sparkline path
  const max = Math.max(...data.map((d) => d.v), 1)
  const min = Math.min(...data.map((d) => d.v), 0)
  const range = max - min || 1
  const step = w / Math.max(1, data.length - 1)
  const points = data.map((d, i) => {
    const x = i * step
    const y = h - ((d.v - min) / range) * h
    return `${x},${y}`
  }).join(' ')
  return (
    <svg viewBox={`0 0 ${w} ${h}`} width="100%" height={h} aria-label="time-series-chart">
      <polyline fill="none" stroke="#2563eb" strokeWidth={2} points={points} />
    </svg>
  )
}
