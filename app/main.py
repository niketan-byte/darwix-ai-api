from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.endpoints import transcription, title_suggestions
from app.core.config import API_PREFIX, PROJECT_NAME, DEBUG

app = FastAPI(
    title=PROJECT_NAME,
    description="API for audio transcription with diarization and blog title suggestions",
    version="1.0.0",
    debug=DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, this should be restricted
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transcription.router, prefix=API_PREFIX, tags=["Transcription"])
app.include_router(title_suggestions.router, prefix=API_PREFIX, tags=["Title Suggestions"])

# Error handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)},
    )

@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": f"Welcome to {PROJECT_NAME}. See /docs for API documentation."} 