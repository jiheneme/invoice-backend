import httpx
from fastapi import HTTPException
from app.settings import get_settings

settings = get_settings()

async def query_invoice_mcp_server(text: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.invoice_mcp_server_url, json={"input": text})
            response.raise_for_status()
            print(response.json)
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code = 503, detail = f"MCP Server unreachable: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code = e.response.status_code, detail = f"MCP Server error: {e.response.text}")
