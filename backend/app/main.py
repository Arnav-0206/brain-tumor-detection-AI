from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import prediction, metrics

app = FastAPI(
    title="NeuroScan AI - Brain Tumor Detection API",
    description="AI-powered brain tumor detection with explainable AI",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(prediction.router)
app.include_router(metrics.router, prefix="/api", tags=["metrics"])


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "NeuroScan AI - Brain Tumor Detection API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "predict": "/api/predict",
            "gradcam": "/api/gradcam"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}
