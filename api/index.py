from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json, os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=False)

data_path = os.path.join(os.path.dirname(__file__), '..', 'data.json')
with open(data_path) as f:
    data = json.load(f)

class LatencyRequest(BaseModel):
    regions: list
    threshold_ms: float

@app.options("/api/latency")
def options():
    return JSONResponse(content={}, headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST", "Access-Control-Allow-Headers": "*"})

@app.post("/api/latency")
def latency(req: LatencyRequest):
    result = []
    for region in req.regions:
        rows = [r for r in data if r["region"] == region]
        latencies = [r["latency_ms"] for r in rows]
        uptimes = [r["uptime_pct"] for r in rows]
        result.append({
            "region": region,
            "avg_latency": round(sum(latencies)/len(latencies), 2),
            "p95_latency": round(sorted(latencies)[int(len(latencies)*0.95)], 2),
            "avg_uptime": round(sum(uptimes)/len(uptimes), 2),
            "breaches": sum(1 for l in latencies if l > req.threshold_ms)
        })
    return JSONResponse(content=result, headers={"Access-Control-Allow-Origin": "*"})