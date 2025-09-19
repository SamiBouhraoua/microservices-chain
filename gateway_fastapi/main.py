from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import time

app = FastAPI()

class Payload(BaseModel):
    message: str
    trace: list = []

@app.post("/api/chain")
async def chain(payload: Payload):
    try:
        data = {
            "message": payload.message,
            "trace": []
        }

        async with httpx.AsyncClient(timeout=5.0) as client:
            res = await client.post("http://127.0.0.1:9001/stepA", json=data)
            res.raise_for_status()
            result = res.json()

        result["trace"].append({
            "service": "gateway",
            "language": "Python (FastAPI)",
            "info": {"final": True},
            "timestamp": time.time()
        })

        return result
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Gateway error: {str(e)}")

@app.get("/ping")
def ping():
    return {"status": "gateway up"}
