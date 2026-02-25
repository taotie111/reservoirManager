import React from 'react'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import './styles/ui.css'
import './globals.css'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <head />
      <body style={{ minHeight: '100%' }}>
        <div className="app-shell">
          <Sidebar />
          <div className="content-shell">
            <Header />
            <main className="main container">{children}</main>
          </div>
        </div>
      </body>
    </html>
  )
}
