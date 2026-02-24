import React from 'react'

export default function AlertsList({ items }: { items: Array<any> }) {
  return (
    <ul className="list-disc pl-5">
      {items.map((it, idx) => (
        <li key={idx}>{JSON.stringify(it)}</li>
      ))}
    </ul>
  )
}
