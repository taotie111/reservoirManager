"use client";
import React, { useEffect, useState } from 'react'

function applyTheme(theme: 'light' | 'dark') {
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('rt-theme', theme)
}

export default function ThemeToggle() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light')

  useEffect(() => {
    const saved = (localStorage.getItem('rt-theme') as 'light' | 'dark') || 'light'
    setTheme(saved)
    applyTheme(saved)
  }, [])

  const toggle = () => {
    const next = theme === 'light' ? 'dark' : 'light'
    setTheme(next)
    applyTheme(next)
  }

  return (
    <button aria-label="切换主题" onClick={toggle} className="theme-toggle">
      {theme === 'dark' ? '🌞' : '🌜'}
    </button>
  )
}
