from openai import OpenAI
from typing import List
from app.core.config import OPENAI_API_KEY, OPENAI_TITLE_MODEL

class TitleSuggestionService:
    """Service for generating blog title suggestions using AI.
    
    This service leverages OpenAI's language models to generate engaging
    and conversion-optimized title suggestions for blog content.
    """
    
    def __init__(self):
        """Initialize title suggestion service."""
        self.api_key = OPENAI_API_KEY
    
    async def generate_title_suggestions(self, content: str) -> List[str]:
        """Generate engaging title suggestions for a blog post.
        
        Args:
            content: The blog post content to generate titles for
            
        Returns:
            A list of 3 suggested titles
        
        Raises:
            Exception: If the API call fails
        """
        client = OpenAI(api_key=self.api_key)
        
        try:
            completion = client.chat.completions.create(
                model=OPENAI_TITLE_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert copywriter who creates viral blog titles. Create exactly 3 engaging titles. Return each title on a new line without quotes or numbering. Example format:\nFirst Amazing Title Here\nSecond Amazing Title Here\nThird Amazing Title Here"
                    },
                    {
                        "role": "user",
                        "content": f"Create 3 amazing titles for this blog post:\n\nContent: {content[:1000]}"
                    }
                ]
            )
            
            # Split by newlines and clean up any extra whitespace
            titles = [line.strip() for line in completion.choices[0].message.content.strip().split('\n') if line.strip()]
            return titles
            
        except Exception as e:
            print(f"Error generating title suggestions: {str(e)}")
            return ["Error generating title suggestions"]


# Create the service instance that endpoints will import
title_service = TitleSuggestionService()
