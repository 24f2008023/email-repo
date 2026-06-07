from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx, asyncio

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], expose_headers=["*"])

@app.api_route("/{path:path}", methods=["GET","POST","PUT","DELETE","OPTIONS"])
async def proxy(path: str, request: Request):
    body = await request.body()
    async with httpx.AsyncClient() as client:
        r = await client.request(
            method=request.method,
            url=f"http://localhost:11434/{path}",
            content=body,
            headers={"Content-Type": "application/json"}
        )
        return r.json()
    