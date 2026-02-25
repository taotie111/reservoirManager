import React from 'react'
import Link from 'next/link'

export default function Dashboard() {
  return (
    <div className="main">
      <h1 className="page-title">数据看板</h1>
      
      <div className="stats-grid">
        <div className="stat-card animate-in animate-delay-1">
          <div className="stat-label">在线大坝</div>
          <div className="stat-value">12</div>
          <div className="stat-change positive">↑ 2 近一月</div>
        </div>
        <div className="stat-card animate-in animate-delay-2">
          <div className="stat-label">监测点位</div>
          <div className="stat-value">248</div>
          <div className="stat-change positive">↑ 15 近一月</div>
        </div>
        <div className="stat-card animate-in animate-delay-3">
          <div className="stat-label">告警数量</div>
          <div className="stat-value">3</div>
          <div className="stat-change negative">↓ 5 近一月</div>
        </div>
        <div className="stat-card animate-in animate-delay-4">
          <div className="stat-label">在线率</div>
          <div className="stat-value">98.5%</div>
          <div className="stat-change positive">↑ 1.2%</div>
        </div>
      </div>

      <div className="grid-3">
        <div className="card animate-in" style={{ gridColumn: 'span 2' }}>
          <div className="card-title">
            📍 3D 地图视图
            <span className="card-badge badge-success">在线</span>
          </div>
          <div className="card-content">
            <div style={{ 
              height: '300px', 
              background: 'linear-gradient(135deg, #f0f4ff 0%, #e0e7ff 100%)',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#6b7280',
              fontSize: '14px'
            }}>
              [3D 地图占位 - CGCS2000 坐标系]
            </div>
          </div>
        </div>

        <div className="card animate-in animate-delay-1">
          <div className="card-title">
            🔔 实时告警
          </div>
          <div className="card-content">
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div style={{ padding: '10px', background: 'rgba(225, 29, 72, 0.08)', borderRadius: '6px', borderLeft: '3px solid #e11d48' }}>
                <div style={{ fontWeight: 600, fontSize: '13px' }}>水位超限告警</div>
                <div style={{ fontSize: '12px', color: '#6b7280', marginTop: '4px' }}>示例坝体A - 10:32</div>
              </div>
              <div style={{ padding: '10px', background: 'rgba(245, 158, 11, 0.08)', borderRadius: '6px', borderLeft: '3px solid #f59e0b' }}>
                <div style={{ fontWeight: 600, fontSize: '13px' }}>渗流异常</div>
                <div style={{ fontSize: '12px', color: '#6b7280', marginTop: '4px' }}>示例坝体B - 09:15</div>
              </div>
              <div style={{ padding: '10px', background: 'rgba(20, 184, 166, 0.08)', borderRadius: '6px', borderLeft: '3px solid #14b8a6' }}>
                <div style={{ fontWeight: 600, fontSize: '13px' }}>设备维护提醒</div>
                <div style={{ fontSize: '12px', color: '#6b7280', marginTop: '4px' }}>示例坝体C - 昨天</div>
              </div>
            </div>
            <div className="card-actions">
              <Link href="/alerts" className="card-link">查看全部 →</Link>
            </div>
          </div>
        </div>

        <div className="card animate-in animate-delay-2" style={{ gridColumn: 'span 2' }}>
          <div className="card-title">
            📈 监测趋势
          </div>
          <div className="card-content">
            <div style={{ 
              height: '200px', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center',
              color: '#6b7280',
              fontSize: '14px'
            }}>
              [时序数据图表占位]
            </div>
          </div>
        </div>

        <div className="card animate-in animate-delay-3">
          <div className="card-title">
            📋 快速操作
          </div>
          <div className="card-content">
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <Link href="/dams" style={{ padding: '10px 12px', background: 'rgba(37, 99, 235, 0.08)', borderRadius: '6px', color: '#2563eb', textDecoration: 'none', fontSize: '14px' }}>
                + 添加新水库
              </Link>
              <Link href="/alerts" style={{ padding: '10px 12px', background: 'rgba(37, 99, 235, 0.08)', borderRadius: '6px', color: '#2563eb', textDecoration: 'none', fontSize: '14px' }}>
                查看待处理告警
              </Link>
              <Link href="/forecasts" style={{ padding: '10px 12px', background: 'rgba(37, 99, 235, 0.08)', borderRadius: '6px', color: '#2563eb', textDecoration: 'none', fontSize: '14px' }}>
                生成预测报告
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
