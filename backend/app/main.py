from fastapi import FastAPI

from app.api.v1.router import api_router

app = FastAPI(
    title="Enterprise Intelligence Platform",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Enterprise Intelligence Platform API is running!"
    }
