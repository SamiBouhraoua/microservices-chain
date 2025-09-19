from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

app = FastAPI()

class Trace(BaseModel):
    service: str
    language: str
    info: dict
    timestamp: float

class Payload(BaseModel):
    message: str
    trace: list[Trace]

@app.post("/stepC")
async def step_c(payload: Payload):
    try:
        # Transformation : ajouter longueur
        length = len(payload.message)
        transformed = f"{payload.message} | len={length} | service-c"

        # Ajouter trace (✅ objet Trace plutôt qu'un dict)
        payload.trace.append(Trace(
            service="service-c",
            language="Python",
            info={"appended_len": length},
            timestamp=time.time()
        ))

        # Retourner le message final + la trace
        return {"message": transformed, "trace": [t.model_dump() for t in payload.trace]}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

@app.get("/ping")
def ping():
    return {"status": "C up"}
