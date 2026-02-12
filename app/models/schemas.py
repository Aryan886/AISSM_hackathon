from pydantic import BaseModel, Field
from typing import Optional, List


class IssueRequest(BaseModel):
    """Request model for issue analysis"""
    
    issue_text: str = Field(..., min_length=10, description="Description of the civic issue")
    location: str = Field(..., min_length=2, description="Area/locality name")
    pincode: Optional[str] = Field(None, pattern=r"^\d{6}$", description="6-digit pincode")
    image_url: Optional[str] = Field(None, description="Optional image URL (for future vision processing)")
    #ngo_list: Optional[List[str]] = Field(None, description="List of NGOs to consider for recommendation")

    class Config:
        json_schema_extra = {
            "example": {
                "issue_text": "Water pipe burst near school, urgent help needed",
                "location": "Kothrud",
                "pincode": "411038",
                "image_url": "https://example.com/image.jpg"
            }
        }


class IssueResponse(BaseModel):
    """Response model for issue analysis"""
    
    category: str = Field(..., description="Classified issue category")
    severity: str = Field(..., description="Severity level (Low/Medium/High/Critical)")
    impact_score: float = Field(..., ge=0.0, le=10.0, description="Numerical impact score (0-10)")
    suggested_ngos: List[str] = Field(..., min_items=1, max_items=3, description="Top 3 recommended NGO names")
    reasoning: str = Field(..., description="AI-generated explanation for the recommendation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "category": "Water Infrastructure",
                "severity": "High",
                "impact_score": 8.7,
                "suggested_ngos": [
                    "CleanWater Foundation",
                    "Urban Relief NGO",
                    "CommunityAid Trust"
                ],
                "reasoning": "Public safety risk near school. Immediate response recommended."
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    fallback_used: bool = Field(False, description="Whether fallback logic was used")