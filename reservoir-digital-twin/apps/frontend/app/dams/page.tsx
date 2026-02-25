"use client";
import React, { useEffect, useState } from 'react'
import Link from 'next/link'

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
  createdAt?: string
  updatedAt?: string
}

export default function DamsPage() {
  const [dams, setDams] = useState<Dam[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/dams')
      .then((r) => r.json())
      .then((data) => {
        setDams(data as Dam[])
        setLoading(false)
      })
      .catch(() => {
        setDams([
          {
            damId: 'dam-001',
            name: '示例坝体A',
            location: { type: 'Point', coordinates: [102.0, 30.0] },
            type: '水库',
            status: '正常',
          },
          {
            damId: 'dam-002',
            name: '示例坝体B',
            location: { type: 'Point', coordinates: [103.5, 31.2] },
            type: '水库',
            status: '运行中',
          },
          {
            damId: 'dam-003',
            name: '示例坝体C',
            location: { type: 'Point', coordinates: [104.2, 32.5] },
            type: '水库',
            status: '维护中',
          },
        ])
        setLoading(false)
      })
  }, [])

  const formatLocation = (loc?: LocationPoint) => {
    if (!loc?.coordinates) return '—'
    const [lon, lat] = loc.coordinates
    return `${lon.toFixed(4)}°, ${lat.toFixed(4)}°`
  }

  const getStatusBadge = (status?: string) => {
    const statusMap: Record<string, string> = {
      '正常': 'badge-success',
      '运行中': 'badge-success',
      '维护中': 'badge-warning',
      '异常': 'badge-error',
    }
    return statusMap[status || ''] || 'badge-success'
  }

  if (loading) {
    return (
      <div className="main">
        <h1 className="page-title">水库大坝</h1>
        <div className="grid-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="card animate-in">
              <div className="card-title">加载中...</div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="main">
      <h1 className="page-title">水库大坝</h1>
      
      <div className="stats-grid">
        <div className="stat-card animate-in animate-delay-1">
          <div className="stat-label">水库总数</div>
          <div className="stat-value">{dams.length}</div>
        </div>
        <div className="stat-card animate-in animate-delay-2">
          <div className="stat-label">正常运行</div>
          <div className="stat-value">{dams.filter(d => d.status === '正常' || d.status === '运行中').length}</div>
        </div>
        <div className="stat-card animate-in animate-delay-3">
          <div className="stat-label">监测点位</div>
          <div className="stat-value">24</div>
        </div>
        <div className="stat-card animate-in animate-delay-4">
          <div className="stat-label">在线传感器</div>
          <div className="stat-value">156</div>
        </div>
      </div>

      <div className="grid-3">
        {dams.map((d, index) => (
          <div key={d.damId} className={`card animate-in animate-delay-${(index % 4) + 1}`}>
            <div className="card-title">
              {d.name}
              <span className={`card-badge ${getStatusBadge(d.status)}`}>
                {d.status || '正常'}
              </span>
            </div>
            <div className="card-content">
              <div className="card-row">
                <span className="card-label">坝体编号</span>
                <span className="card-value">{d.damId}</span>
              </div>
              <div className="card-row">
                <span className="card-label">地理位置</span>
                <span className="card-value">{formatLocation(d.location)}</span>
              </div>
              <div className="card-row">
                <span className="card-label">水库类型</span>
                <span className="card-value">{d.type || '—'}</span>
              </div>
              <div className="card-row">
                <span className="card-label">坐标系统</span>
                <span className="card-value">CGCS2000</span>
              </div>
            </div>
            <div className="card-actions">
              <Link href={`/dams/${d.damId}`} className="card-link">
                查看详情 →
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
