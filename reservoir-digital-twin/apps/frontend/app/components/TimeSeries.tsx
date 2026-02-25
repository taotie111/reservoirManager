import React from 'react'
import TimeSeriesChart from './TimeSeriesChart'

export default function TimeSeries({ data }: { data: Array<{ t: string; v: number }> }) {
  // simple container with a lightweight sparkline chart
  const chartData = data.map((d) => ({ t: d.t, v: d.v }))
  return (
    <div className="time-series-chart" aria-label="time-series-chart" style={{ padding: 8 }}>
      <TimeSeriesChart data={chartData} />
    </div>
  )
}
