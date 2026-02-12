"""
Main FastAPI Application
AI-Powered NGO Civic Issue Routing System
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.models.schemas import IssueRequest, IssueResponse, ErrorResponse
from app.services import gemini_service
from app.utils.logger import logger
from app.config import settings

# Initialize FastAPI app
app = FastAPI(
    title="Civic Issue Routing API",
    description="AI-powered system for routing civic issues to relevant NGOs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration - adjust origins for your Node.js server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Replace with your Node.js server URL in production
    allow_credentials=True,
    allow_methods=["*"], #POST, GET, etc.
    allow_headers=["*"], #Content-Type, Authorization, etc.
)


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check"""
    return {
        "status": "online",
        "message": "Civic Issue Routing API is running",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "gemini_configured": settings.gemini_api_key != "your_gemini_api_key_here"
    }


@app.post(
    "/analyze-issue",
    response_model=IssueResponse,
    status_code=status.HTTP_200_OK,
    tags=["Issue Analysis"],
    summary="Analyze civic issue and recommend NGOs",
    responses={
        200: {
            "description": "Successfully analyzed issue",
            "model": IssueResponse
        },
        400: {
            "description": "Invalid request data",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    }
)

async def analyze_issue(request: IssueRequest):
    """
    Analyze a civic issue and recommend top 3 relevant NGOs
    
    This endpoint:
    1. Receives issue details from Node.js
    2. Uses Gemini API to classify and analyze the issue
    3. Recommends top 3 NGOs from the predefined list
    4. Falls back to keyword-based classification if Gemini fails
    
    Args:
        request: IssueRequest containing issue_text, location, pincode, and optional image_url
    
    Returns:
        IssueResponse with category, severity, impact_score, suggested_ngos, and reasoning
    
    Raises:
        HTTPException: If request validation fails or processing error occurs
    """
    try:
        logger.info(f"Received issue analysis request for location: {request.location}")
        
        # Call Gemini service to analyze issue
        result = gemini_service.analyze_issue(
            issue_text=request.issue_text,
            location=request.location,
            pincode=request.pincode,
            image_url=request.image_url
        )
        
        logger.info(
            f"Issue analyzed successfully: category={result.category}, "
            f"severity={result.severity}, NGOs={len(result.suggested_ngos)}"
        )
        
        return result
        
    except ValueError as e:
        # Validation or parsing errors
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        # Unexpected errors
        logger.error(f"Unexpected error during issue analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the request"
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "detail": None,
            "fallback_used": False
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.environment == "development" else None,
            "fallback_used": False
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {settings.host}:{settings.port}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development"
    )