import React from 'react'
import { notFound } from 'next/navigation'

export default function ReservoirDetail({ params }: { params: { id: string } }) {
  const { id } = params
  if (!id) return notFound()
  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-2">水库详情 - {id}</h2>
      <div className="bg-white rounded p-4">时序图和详解在这里占位</div>
    </div>
  )
}
