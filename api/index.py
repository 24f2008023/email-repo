from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json, os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open(os.path.join(os.path.dirname(__file__), '..', 'data.json')) as f:
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
