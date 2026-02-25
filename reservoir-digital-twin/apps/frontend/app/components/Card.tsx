import React from 'react'

type CardProps = {
  title?: string
  children: React.ReactNode
}

export default function Card({ title, children }: CardProps) {
  return (
    <section className="card" aria-label={title ?? 'card'}>
      {title && <div className="card-title">{title}</div>}
      {children}
    </section>
  )
}
