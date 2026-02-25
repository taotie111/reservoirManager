import { NextResponse } from 'next/server'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const damId = searchParams.get('damId')
  const level = searchParams.get('level')
  const status = searchParams.get('status')
  
  let url = `${API_BASE}/alarms?`
  const params = new URLSearchParams()
  if (damId) params.append('damId', damId)
  if (level) params.append('level', level)
  if (status) params.append('status', status)
  
  try {
    const res = await fetch(`${url}${params.toString()}`, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
    const data = await res.json()
    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch alarms' },
      { status: 500 }
    )
  }
}
