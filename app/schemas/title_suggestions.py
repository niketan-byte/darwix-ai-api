from pydantic import BaseModel, Field
from typing import List


class TitleSuggestionRequest(BaseModel):
    """Model for requesting blog title suggestions."""
    
    content: str = Field(..., description="The blog post content to generate titles for", min_length=50)


class TitleSuggestionResponse(BaseModel):
    """Model for the response from the title suggestion API."""
    
    suggestions: List[str] = Field(..., description="List of suggested titles for the blog post")
    

class ErrorResponse(BaseModel):
    """Model for API error responses."""
    
    detail: str = Field(..., description="Error message detailing what went wrong") 