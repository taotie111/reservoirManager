import React from 'react'

export default function Dashboard() {
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-3">Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div className="bg-white rounded shadow p-4">地图区域占位</div>
        <div className="bg-white rounded shadow p-4">指标卡片占位</div>
        <div className="bg-white rounded shadow p-4">告警流占位</div>
      </div>
    </div>
  )
}
