"use client";
import React, { useEffect, useState } from 'react'
import Link from 'next/link'
import { useParams } from 'next/navigation'

type LocationPoint = {
  type: string
  coordinates: [number, number]
}

type Dam = {
  damId: string
  name: string
  location?: LocationPoint
  type?: string
  status?: string
  designParameters?: any
  createdAt?: string
  updatedAt?: string
}

type MonitoringPoint = {
  pointId: string
  damId: string
  name: string
  location?: LocationPoint
  pointType?: string
  status?: string
  lastValue?: number
  unit?: string
}

export default function DamDetailPage() {
  const params = useParams()
  const damId = params.damId as string
  
  const [dam, setDam] = useState<Dam | null>(null)
  const [monitoringPoints, setMonitoringPoints] = useState<MonitoringPoint[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetch(`/api/dams/${damId}`).then(r => r.json()),
      fetch(`/api/monitoring-points?damId=${damId}`).then(r => r.json())
    ])
      .then(([damData, pointsData]) => {
        setDam(damData)
        setMonitoringPoints(pointsData)
        setLoading(false)
      })
      .catch(() => {
        setLoading(false)
      })
  }, [damId])

  const formatLocation = (loc?: LocationPoint) => {
    if (!loc?.coordinates) return '—'
    const [lon, lat] = loc.coordinates
    return `${lon.toFixed(4)}°, ${lat.toFixed(4)}°`
  }

  const getStatusBadge = (status?: string) => {
    const statusMap: Record<string, string> = {
      'normal': 'badge-success',
      'active': 'badge-success',
      'maintenance': 'badge-warning',
      'warning': 'badge-warning',
      'error': 'badge-error',
      'critical': 'badge-error',
    }
    return statusMap[status || ''] || 'badge-success'
  }

  if (loading) {
    return (
      <div className="main">
        <h1 className="page-title">加载中...</h1>
      </div>
    )
  }

  if (!dam) {
    return (
      <div className="main">
        <h1 className="page-title">水库详情</h1>
        <p>未找到该水库信息</p>
        <Link href="/dams" className="card-link">← 返回水库列表</Link>
      </div>
    )
  }

  return (
    <div className="main">
      <div style={{ marginBottom: '20px' }}>
        <Link href="/dams" className="card-link">← 返回水库列表</Link>
      </div>
      
      <h1 className="page-title">{dam.name}</h1>
      
      <div className="stats-grid">
        <div className="stat-card animate-in animate-delay-1">
          <div className="stat-label">状态</div>
          <div className="stat-value">
            <span className={`card-badge ${getStatusBadge(dam.status)}`}>
              {dam.status || '正常'}
            </span>
          </div>
        </div>
        <div className="stat-card animate-in animate-delay-2">
          <div className="stat-label">类型</div>
          <div className="stat-value">{dam.type || '—'}</div>
        </div>
        <div className="stat-card animate-in animate-delay-3">
          <div className="stat-label">监测点数量</div>
          <div className="stat-value">{monitoringPoints.length}</div>
        </div>
        <div className="stat-card animate-in animate-delay-4">
          <div className="stat-label">坐标</div>
          <div className="stat-value" style={{ fontSize: '18px' }}>
            {formatLocation(dam.location)}
          </div>
        </div>
      </div>

      <h2 className="page-title" style={{ marginTop: '32px' }}>监测点列表</h2>
      
      {monitoringPoints.length > 0 ? (
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>监测点名称</th>
                <th>类型</th>
                <th>当前值</th>
                <th>单位</th>
                <th>状态</th>
              </tr>
            </thead>
            <tbody>
              {monitoringPoints.map((point) => (
                <tr key={point.pointId}>
                  <td>{point.name}</td>
                  <td>{point.pointType || '—'}</td>
                  <td>{point.lastValue ?? '—'}</td>
                  <td>{point.unit || '—'}</td>
                  <td>
                    <span className={`card-badge ${getStatusBadge(point.status)}`}>
                      {point.status || 'active'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="card">
          <div className="card-content">暂无监测点数据</div>
        </div>
      )}
    </div>
  )
}
