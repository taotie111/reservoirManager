"use client";
import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const NavItem = ({ href, label, icon }: { href: string; label: string; icon: string }) => {
  const pathname = usePathname() || '/'
  const isActive = pathname.startsWith(href)
  
  return (
    <Link href={href} className={`nav-item ${isActive ? 'active' : ''}`}>
      <span className="nav-icon">{icon}</span>
      {label}
    </Link>
  )
}

export default function Sidebar() {
  return (
    <aside className="sidebar" aria-label="导航菜单">
      <div className="sidebar-brand">
        <div className="sidebar-logo" />
        <div className="sidebar-brand-text">
          <span className="sidebar-brand-title">水库大坝安全监测</span>
          <span className="sidebar-brand-subtitle">数字孪生平台</span>
        </div>
      </div>
      <nav className="sidebar-nav" aria-label="导航列表">
        <NavItem href="/dams" label="水库大坝" icon="🏔️" />
        <NavItem href="/dashboard" label="数据看板" icon="📊" />
        <NavItem href="/alerts" label="告警中心" icon="🔔" />
        <NavItem href="/forecasts" label="预测分析" icon="📈" />
        <NavItem href="/admin" label="系统管理" icon="⚙️" />
      </nav>
    </aside>
  )
}
