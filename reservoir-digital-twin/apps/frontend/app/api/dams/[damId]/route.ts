import { NextResponse } from 'next/server'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export async function GET(
  request: Request,
  { params }: { params: Promise<{ damId: string }> }
) {
  try {
    const { damId } = await params
    const res = await fetch(`${API_BASE}/dams/${damId}`, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    if (!res.ok) {
      return NextResponse.json(
        { error: 'Dam not found' },
        { status: res.status }
      )
    }
    
    const data = await res.json()
    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch dam' },
      { status: 500 }
    )
  }
}
