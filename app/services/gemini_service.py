"""
Gemini Service - AI-powered issue classification and NGO recommendation

Uses Google's Gemini API to analyze civic issues and suggest relevant NGOs
"""

from google import genai
import json
from typing import Optional
from app.config.settings import settings
from app.models.schemas import IssueResponse
from app.services.ngo_data import format_ngos_for_prompt
from app.services.fallback_service import classify_issue_fallback
from app.utils.logger import logger


class GeminiService:
    """Service class for Gemini API interactions"""
    
    def __init__(self):
        """Initialize Gemini API with configuration"""
        try:
            self.client = genai.Client(api_key=settings.gemini_api_key)
            self.model = "gemini-2.5-flash"
            logger.info("Gemini API initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini API: {str(e)}")
            self.client = None
            self.model = None
    
    def analyze_issue(
        self, 
        issue_text: str, 
        location: str, 
        pincode: str,
        image_url: Optional[str] = None
    ) -> IssueResponse:
        """
        Analyze civic issue using Gemini API
        
        Args:
            issue_text: Description of the issue
            location: Area/locality
            pincode: 6-digit pincode
            image_url: Optional image URL (not used yet)
        
        Returns:
            IssueResponse with classification and NGO suggestions
        """
        # If Gemini is not initialized, use fallback
        if self.client is None or self.model is None:
            logger.warning("Gemini API not available, using fallback")
            return classify_issue_fallback(issue_text, location)
        
        try:
            # Generate prompt for Gemini
            prompt = self._create_prompt(issue_text, location, pincode)
            
            logger.info(f"Sending request to Gemini API for issue in {location}")
            
            # Call Gemini API
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            # Parse and validate response
            result = self._parse_gemini_response(response.text)
            
            logger.info(f"Successfully received response from Gemini: category={result.category}")
            
            return result
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}, falling back to keyword classification")
            return classify_issue_fallback(issue_text, location)
    
    def _create_prompt(self, issue_text: str, location: str, pincode: str) -> str:
        """
        Create structured prompt for Gemini API
        
        Args:
            issue_text: Issue description
            location: Location name
            pincode: Pincode
        
        Returns:
            Formatted prompt string
        """
        ngo_list = format_ngos_for_prompt()
        
        prompt = f"""You are an AI assistant for a civic issue routing system. Your task is to analyze civic issues and recommend the most suitable NGOs.

{ngo_list}

**Issue Details:**
- Description: {issue_text}
- Location: {location}
- Pincode: {pincode}

**Your Task:**
1. Classify the issue into ONE category (Water, Waste, Roads, Electricity, Women Safety, Animal Rescue, Healthcare, Environment, Infrastructure, or General)
2. Assign a severity level: Low, Medium, High, or Critical
3. Provide an impact score from 0.0 to 10.0 (where 10.0 is most severe)
4. Select the TOP 3 most relevant NGOs from the list above ONLY by their exact names
5. Provide clear reasoning for your recommendations

**CRITICAL RULES:**
- You MUST select NGOs ONLY from the provided list above
- Return EXACTLY 3 NGO names (no more, no less)
- Use the EXACT names as listed (do not modify)
- Consider both the issue category and the NGO's operating area
- Prioritize NGOs that operate in "All Pune" or the specific area mentioned

**Response Format:**
Return your response as a valid JSON object with this exact structure:
{{
    "category": "category name",
    "severity": "Low/Medium/High/Critical",
    "impact_score": numeric value between 0.0 and 10.0,
    "suggested_ngos": ["NGO Name 1", "NGO Name 2", "NGO Name 3"],
    "reasoning": "explanation of your analysis and recommendations"
}}

Return ONLY the JSON object, no additional text before or after.
"""
        return prompt
    
    def _parse_gemini_response(self, response_text: str) -> IssueResponse:
        """
        Parse and validate Gemini API response
        
        Args:
            response_text: Raw response from Gemini
        
        Returns:
            Validated IssueResponse object
        
        Raises:
            ValueError: If response cannot be parsed
        """
        try:
            # Remove markdown code blocks if present
            cleaned_text = response_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            
            cleaned_text = cleaned_text.strip()
            
            # Parse JSON
            data = json.loads(cleaned_text)
            
            # Validate required fields
            required_fields = ["category", "severity", "impact_score", "suggested_ngos", "reasoning"]
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Ensure we have exactly 3 NGOs (or at least 1)
            if not isinstance(data["suggested_ngos"], list) or len(data["suggested_ngos"]) == 0:
                raise ValueError("Invalid NGO list")
            
            # Limit to top 3
            data["suggested_ngos"] = data["suggested_ngos"][:3]
            
            # Create and validate response using Pydantic
            return IssueResponse(**data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            raise ValueError(f"Invalid JSON response from Gemini: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to validate response: {str(e)}")
            raise ValueError(f"Invalid response structure: {str(e)}")


# Global service instance
gemini_service = GeminiService()
