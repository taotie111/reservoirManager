import React from 'react'
import Link from 'next/link'

export default function Forecasts() {
  const predictions = [
    { id: 1, model: '水位预测模型 v2.1', dam: '示例坝体A', accuracy: '92.5%', lastRun: '2024-01-15 08:00', status: '运行中' },
    { id: 2, model: '渗流趋势模型 v1.8', dam: '示例坝体B', accuracy: '88.3%', lastRun: '2024-01-15 06:00', status: '运行中' },
    { id: 3, model: '位移沉降预测 v1.5', dam: '示例坝体A', accuracy: '85.7%', lastRun: '2024-01-14 22:00', status: '已完成' },
    { id: 4, model: '洪峰预警模型 v3.0', dam: '全流域', accuracy: '94.2%', lastRun: '2024-01-15 10:00', status: '运行中' },
  ]

  return (
    <div className="main">
      <h1 className="page-title">预测分析</h1>

      <div className="stats-grid">
        <div className="stat-card animate-in animate-delay-1">
          <div className="stat-label">运行模型</div>
          <div className="stat-value">4</div>
        </div>
        <div className="stat-card animate-in animate-delay-2">
          <div className="stat-label">平均准确率</div>
          <div className="stat-value">90.2%</div>
          <div className="stat-change positive">↑ 2.3%</div>
        </div>
        <div className="stat-card animate-in animate-delay-3">
          <div className="stat-label">今日预测</div>
          <div className="stat-value">156</div>
        </div>
        <div className="stat-card animate-in animate-delay-4">
          <div className="stat-label">预警次数</div>
          <div className="stat-value">8</div>
          <div className="stat-change negative">↑ 3</div>
        </div>
      </div>

      <div className="grid-3">
        <div className="card animate-in" style={{ gridColumn: 'span 2' }}>
          <div className="card-title">
            📈 预测趋势图
          </div>
          <div className="card-content">
            <div style={{ 
              height: '280px', 
              background: 'linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%)',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#0f766e',
              fontSize: '14px'
            }}>
              [未来7天水位预测趋势图占位]
            </div>
          </div>
        </div>

        <div className="card animate-in animate-delay-1">
          <div className="card-title">
            🎯 模型列表
          </div>
          <div className="card-content">
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {predictions.slice(0, 3).map((p) => (
                <div key={p.id} style={{ padding: '12px', background: '#f6f7fb', borderRadius: '8px' }}>
                  <div style={{ fontWeight: 600, fontSize: '13px' }}>{p.model}</div>
                  <div style={{ fontSize: '12px', color: '#6b7280', marginTop: '4px' }}>
                    准确率: {p.accuracy}
                  </div>
                </div>
              ))}
            </div>
            <div className="card-actions">
              <Link href="#" className="card-link">查看全部 →</Link>
            </div>
          </div>
        </div>

        <div className="table-container animate-in animate-delay-2" style={{ gridColumn: 'span 3' }}>
          <table className="table">
            <thead>
              <tr>
                <th>模型名称</th>
                <th>适用水库</th>
                <th>准确率</th>
                <th>最后运行</th>
                <th>状态</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              {predictions.map((p) => (
                <tr key={p.id}>
                  <td style={{ fontWeight: 500 }}>{p.model}</td>
                  <td>{p.dam}</td>
                  <td>{p.accuracy}</td>
                  <td style={{ color: '#6b7280' }}>{p.lastRun}</td>
                  <td>
                    <span className={`card-badge ${p.status === '运行中' ? 'badge-success' : 'badge-warning'}`}>
                      {p.status}
                    </span>
                  </td>
                  <td>
                    <Link href="#" className="card-link">详情</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
