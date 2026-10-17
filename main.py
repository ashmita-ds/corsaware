
import os
import time
import uuid

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-3f5quo.example.com"
EMAIL = os.getenv("STUDENT_EMAIL", "25ds1000059@ds.study.iitm.ac.in")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_required_headers(request: Request, call_next):
    start = time.perf_counter()
    request_id = str(uuid.uuid4())

    try:
        response = await call_next(request)
    except Exception:
        raise

    elapsed = time.perf_counter() - start
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"
    return response

@app.get("/stats")
async def stats(values: str = Query(..., description="Comma-separated integers")):
    try:
        numbers = [int(value.strip()) for value in values.split(",")]
        if not numbers or any(value == "" for value in values.split(",")):
            raise ValueError
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="values must be a comma-separated list of integers",
        )

    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": sum(numbers) / len(numbers),
    }
