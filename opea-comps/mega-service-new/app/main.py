from fastapi import FastAPI
from .telemetry import setup_telemetry
from .gptsovits import router as gptsovits_router

app = FastAPI(title="GPT-SoVITS Service")

# Set up telemetry
setup_telemetry(app)

# Include routers
app.include_router(gptsovits_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 