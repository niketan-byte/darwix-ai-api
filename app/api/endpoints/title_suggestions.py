from fastapi import APIRouter, HTTPException, status

from app.services.title_service import title_service
from app.schemas.title_suggestions import TitleSuggestionRequest, TitleSuggestionResponse

# Create router
router = APIRouter()


@router.post(
    "/title-suggestions", 
    response_model=TitleSuggestionResponse, 
    summary="Generate blog post title suggestions",
    status_code=status.HTTP_200_OK,
)
async def generate_title_suggestions(
    request: TitleSuggestionRequest,
):
    """
    Generate AI-powered title suggestions for a blog post.
    
    - **content**: The content of the blog post
    
    Returns a JSON with:
    - A list of 3 suggested titles
    """
    try:
        if len(request.content) < 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Blog content is too short. Please provide at least 50 characters."
            )
            
        # Call the title suggestion service
        titles = await title_service.generate_title_suggestions(request.content)
        
        # Return the suggestions
        return TitleSuggestionResponse(suggestions=titles)
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating title suggestions: {str(e)}"
        ) 