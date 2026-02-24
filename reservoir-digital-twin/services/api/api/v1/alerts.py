from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio

router = APIRouter()

@router.get("/alerts/stream")
async def stream_alerts():
    async def event_generator():
        i = 0
        while True:
            i += 1
            yield f"data: {{\"alert\": \"sample-{i}\"}}\n\n"
            await asyncio.sleep(3)
    return StreamingResponse(event_generator(), media_type="text/event-stream")
