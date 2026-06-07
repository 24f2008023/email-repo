from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json, os

app = FastAPI()

@app.middleware("http")
async def add_cors(request: Request, call_next):
    if request.method == "OPTIONS":
        return JSONResponse(
            content={},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            }
        )
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

data_path = os.path.join(os.path.dirname(__file__), '..', 'data.json')
with open(data_path) as f:
    data = json.load(f)

class LatencyRequest(BaseModel):
    regions: list
    threshold_ms: float

@app.post("/api/latency")
def latency(req: LatencyRequest):
    result = []
    for region in req.regions:
        rows = [r for r in data if r["region"] == region]
        latencies = sorted([r["latency_ms"] for r in rows])
        uptimes = [r["uptime_pct"] for r in rows]
        n = len(latencies)
        p95_index = int(round(0.95 * n)) - 1
        result.append({
            "region": region,
            "avg_latency": round(sum(latencies)/n, 2),
            "p95_latency": round(latencies[p95_index], 2),
            "avg_uptime": round(sum(uptimes)/len(uptimes), 2),
            "breaches": sum(1 for l in latencies if l > req.threshold_ms)
        })
    return result

handler = app