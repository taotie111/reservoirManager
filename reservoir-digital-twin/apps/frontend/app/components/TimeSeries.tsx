import React from 'react'
import * as echarts from 'echarts'

export default function TimeSeriesChart({ data }: { data: Array<{ t: string; v: number }> }) {
  // Simple placeholder chart using a div; actual chart would be rendered with ECharts
  return (
    <div style={{ height: 260, background: '#fff' }} aria-label="time-series-chart">
      Time series chart placeholder
    </div>
  )
}
