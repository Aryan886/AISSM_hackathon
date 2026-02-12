"""
Fallback Service - Keyword-based classification when Gemini API fails

This ensures the system remains operational even without AI
"""

from typing import Dict, List
from app.models.schemas import IssueResponse
from app.utils.logger import logger


# Keyword mappings for category classification
CATEGORY_KEYWORDS = {
    "Water": ["water", "pipe", "leak", "drain", "sewage", "tap", "plumbing", "overflow"],
    "Waste": ["garbage", "waste", "trash", "dump", "litter", "disposal", "dustbin", "cleanliness"],
    "Roads": ["road", "pothole", "street", "highway", "pavement", "footpath", "traffic"],
    "Electricity": ["light", "electric", "power", "streetlight", "pole", "wire", "blackout", "outage"],
    "Women Safety": ["women", "harassment", "safety", "assault", "security", "lighting"],
    "Animal Rescue": ["dog", "cat", "animal", "stray", "injured", "rescue", "wildlife"],
    "Healthcare": ["health", "medical", "hospital", "clinic", "disease", "sanitation"],
    "Environment": ["tree", "pollution", "air", "noise", "green", "park", "forest", "environmental"],
    "Infrastructure": ["building", "construction", "illegal", "encroachment", "bridge", "structure"],
}

# Severity keywords
HIGH_SEVERITY_KEYWORDS = ["urgent", "emergency", "critical", "dangerous", "immediate", "serious", "severe"]
MEDIUM_SEVERITY_KEYWORDS = ["concern", "issue", "problem", "needs attention", "repair"]


def classify_issue_fallback(issue_text: str, location: str) -> IssueResponse:
    """
    Fallback classification using keyword matching
    
    Args:
        issue_text: The issue description
        location: Location of the issue
    
    Returns:
        IssueResponse with fallback classification
    """
    logger.info("Using fallback keyword-based classification")
    
    issue_lower = issue_text.lower()
    
    # Determine category
    category = "General"
    max_matches = 0
    
    for cat, keywords in CATEGORY_KEYWORDS.items():
        matches = sum(1 for keyword in keywords if keyword in issue_lower)
        if matches > max_matches:
            max_matches = matches
            category = cat
    
    # Determine severity
    severity = "Medium"
    impact_score = 5.0
    
    high_severity_count = sum(1 for keyword in HIGH_SEVERITY_KEYWORDS if keyword in issue_lower)
    
    if high_severity_count >= 1:
        severity = "High"
        impact_score = 7.5
    elif any(keyword in issue_lower for keyword in MEDIUM_SEVERITY_KEYWORDS):
        severity = "Medium"
        impact_score = 5.0
    else:
        severity = "Low"
        impact_score = 3.0
    
    # Get NGO suggestions based on category
    suggested_ngos = get_ngos_by_category_fallback(category)
    
    reasoning = (
        f"Issue classified as {category} based on keyword analysis. "
        f"Severity assessed as {severity} based on urgency indicators in the description. "
        f"Recommended NGOs specialize in {category} and operate in the area."
    )
    
    return IssueResponse(
        category=category,
        severity=severity,
        impact_score=impact_score,
        suggested_ngos=suggested_ngos,
        reasoning=reasoning
    )


def get_ngos_by_category_fallback(category: str) -> List[str]:
    """
    Get NGOs matching the category (fallback logic)
    
    Args:
        category: Classified category
    
    Returns:
        List of up to 3 NGO names
    """
    # Import here to avoid circular dependency
    from app.services.ngo_data import get_ngo_list
    
    ngos = get_ngo_list()
    
    # Filter NGOs by category
    matching_ngos = [
        ngo["name"] for ngo in ngos 
        if ngo["category"].lower() == category.lower()
    ]
    
    # If no exact match, try general NGOs
    if not matching_ngos:
        matching_ngos = [
            ngo["name"] for ngo in ngos 
            if ngo["category"].lower() == "general" or ngo["area"].lower() == "all pune"
        ]
    
    # Return top 3
    return matching_ngos[:3] if matching_ngos else ["CommunityAid Trust", "Urban Relief NGO", "GreenCity NGO"]