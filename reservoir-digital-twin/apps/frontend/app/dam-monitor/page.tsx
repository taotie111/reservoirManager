import React from 'react'

export default function DamMonitor() {
  return (
    <div className="main">
      <h1 className="page-title">大坝监测</h1>

      <div className="grid-3">
        <div className="card animate-in">
          <div className="card-title">
            🌡️ 环境监测
            <span className="card-badge badge-success">正常</span>
          </div>
          <div className="card-content">
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: '#6b7280' }}>气温</span>
                <span style={{ fontSize: '20px', fontWeight: 600 }}>23.5°C</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: '#6b7280' }}>水温</span>
                <span style={{ fontSize: '20px', fontWeight: 600 }}>18.2°C</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: '#6b7280' }}>气压</span>
                <span style={{ fontSize: '20px', fontWeight: 600 }}>101.3 kPa</span>
              </div>
            </div>
          </div>
        </div>

        <div className="card animate-in animate-delay-1">
          <div className="card-title">
            💧 水位监测
            <span className="card-badge badge-warning">偏高</span>
          </div>
          <div className="card-content">
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: '#6b7280' }}>库水位</span>
                <span style={{ fontSize: '20px', fontWeight: 600, color: '#f59e0b' }}>185.2m</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: '#6b7280' }}>警戒水位</span>
                <span style={{ fontSize: '20px', fontWeight: 600 }}>180.0m</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: '#6b7280' }}>汛限水位</span>
                <span style={{ fontSize: '20px', fontWeight: 600 }}>175.0m</span>
              </div>
            </div>
          </div>
        </div>

        <div className="card animate-in animate-delay-2">
          <div className="card-title">
            📊 渗流监测
            <span className="card-badge badge-success">正常</span>
          </div>
          <div className="card-content">
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: '#6b7280' }}>渗流量</span>
                <span style={{ fontSize: '20px', fontWeight: 600 }}>12.5 L/s</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: '#6b7280' }}">渗流速率</span>
                <span style={{ fontSize: '20px', fontWeight: 600 }}>0.8 mm/d</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: '#6b7280' }}">渗压水位</span>
                <span style={{ fontSize: '20px', fontWeight: 600 }}>82.3m</span>
              </div>
            </div>
          </div>
        </div>

        <div className="card animate-in animate-delay-3" style={{ gridColumn: 'span 2' }}>
          <div className="card-title">
            📈 实时曲线
          </div>
          <div className="card-content">
            <div style={{ 
              height: '200px', 
              background: 'linear-gradient(135deg, #f0f4ff 0%, #e0e7ff 100%)',
              borderRadius: '8px',
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

        <div className="card animate-in animate-delay-4">
          <div className="card-title">
            📋 传感器状态
          </div>
          <div className="card-content">
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px', background: '#f0fdf4', borderRadius: '6px' }}>
                <span>在线</span>
                <span style={{ fontWeight: 600, color: '#14b8a6' }}>156</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px', background: '#fef3c7', borderRadius: '6px' }}>
                <span>离线</span>
                <span style={{ fontWeight: 600, color: '#f59e0b' }}>3</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '8px', background: '#fee2e2', borderRadius: '6px' }}>
                <span>告警</span>
                <span style={{ fontWeight: 600, color: '#e11d48' }}>2</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
