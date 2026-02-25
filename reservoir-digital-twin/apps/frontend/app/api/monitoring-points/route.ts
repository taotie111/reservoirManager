import { NextResponse } from 'next/server'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const damId = searchParams.get('damId')
  
  let url = `${API_BASE}/monitoring-points`
  if (damId) {
    url = `${API_BASE}/dams/${damId}/monitoring-points`
  }
  
  try {
    const res = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
    const data = await res.json()
    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch monitoring points' },
      { status: 500 }
    )
  }
}
