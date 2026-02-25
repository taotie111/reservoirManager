"use client";
import React, { useEffect, useState } from 'react'
import Link from 'next/link'

type Alarm = {
  alarmId: string
  damId?: string
  pointId?: string
  level: string
  message: string
  createdAt: string
  status: string
}

export default function AlertsPage() {
  const [alarms, setAlarms] = useState<Alarm[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/alarms')
      .then(r => r.json())
      .then(data => {
        setAlarms(data)
        setLoading(false)
      })
      .catch(() => {
        setLoading(false)
      })
  }, [])

  const activeAlarms = alarms.filter(a => a.status === 'active')
  const acknowledgedAlarms = alarms.filter(a => a.status === 'acknowledged')

  const getLevelBadge = (level: string) => {
    const map: Record<string, string> = {
      critical: 'badge-error',
      warning: 'badge-warning',
      info: 'badge-success',
    }
    return map[level] || 'badge-success'
  }

  const getLevelText = (level: string) => {
    const map: Record<string, string> = {
      critical: '紧急',
      warning: '警告',
      info: '提示',
    }
    return map[level] || level
  }

  const formatTime = (timeStr: string) => {
    const date = new Date(timeStr)
    return date.toLocaleString('zh-CN', { 
      month: 'short', 
      day: 'numeric', 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  if (loading) {
    return (
      <div className="main">
        <h1 className="page-title">告警中心</h1>
        <div className="card">加载中...</div>
      </div>
    )
  }

  return (
    <div className="main">
      <h1 className="page-title">告警中心</h1>

      <div className="stats-grid">
        <div className="stat-card animate-in animate-delay-1">
          <div className="stat-label">待处理</div>
          <div className="stat-value" style={{ color: '#e11d48' }}>{activeAlarms.length}</div>
        </div>
        <div className="stat-card animate-in animate-delay-2">
          <div className="stat-label">处理中</div>
          <div className="stat-value" style={{ color: '#f59e0b' }}>{acknowledgedAlarms.length}</div>
        </div>
        <div className="stat-card animate-in animate-delay-3">
          <div className="stat-label">告警总数</div>
          <div className="stat-value">{alarms.length}</div>
        </div>
        <div className="stat-card animate-in animate-delay-4">
          <div className="stat-label">已解决</div>
          <div className="stat-value" style={{ color: '#14b8a6' }}>{alarms.filter(a => a.status === 'resolved').length}</div>
        </div>
      </div>

      <div className="table-container animate-in">
        <table className="table">
          <thead>
            <tr>
              <th>级别</th>
              <th>告警消息</th>
              <th>时间</th>
              <th>状态</th>
            </tr>
          </thead>
          <tbody>
            {alarms.length > 0 ? (
              alarms.map((alarm) => (
                <tr key={alarm.alarmId}>
                  <td>
                    <span className={`card-badge ${getLevelBadge(alarm.level)}`}>
                      {getLevelText(alarm.level)}
                    </span>
                  </td>
                  <td>
                    <div style={{ fontWeight: 500 }}>{alarm.message}</div>
                  </td>
                  <td style={{ color: '#6b7280' }}>{formatTime(alarm.createdAt)}</td>
                  <td>
                    <span className={`card-badge ${alarm.status === 'active' ? 'badge-error' : alarm.status === 'acknowledged' ? 'badge-warning' : 'badge-success'}`}>
                      {alarm.status === 'active' ? '待处理' : alarm.status === 'acknowledged' ? '处理中' : '已解决'}
                    </span>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={4} style={{ textAlign: 'center', padding: '40px', color: '#6b7280' }}>
                  暂无告警数据
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
