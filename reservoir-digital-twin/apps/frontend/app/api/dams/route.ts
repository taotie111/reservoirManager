import { NextResponse } from 'next/server'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export async function GET() {
  try {
    const res = await fetch(`${API_BASE}/dams`, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
    const data = await res.json()
    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch dams' },
      { status: 500 }
    )
  }
}
