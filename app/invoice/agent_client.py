import httpx
from fastapi import HTTPException
from app.settings import get_settings

settings = get_settings()

async def query_invoice_agent(text: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.invoice_agent_url, json={"text": text})
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Agent unreachable: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Agent error: {e.response.text}")
