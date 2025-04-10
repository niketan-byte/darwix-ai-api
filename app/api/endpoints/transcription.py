import os
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.services.transcription_service import transcription_service
from app.schemas.transcription import TranscriptionResponse
from app.core.config import ALLOWED_AUDIO_TYPES, MAX_UPLOAD_SIZE, UPLOAD_DIRECTORY
from app.utils.file_utils import save_upload_file, remove_file

# Create router
router = APIRouter()

# Ensure upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@router.post(
    "/transcribe", 
    response_model=TranscriptionResponse, 
    summary="Transcribe audio with speaker diarization",
    status_code=status.HTTP_200_OK,
)
async def transcribe_audio(
    file: UploadFile = File(...),
):
    """
    Transcribe an audio file with speaker diarization.
    
    - **file**: The audio file to transcribe (mp3, wav, ogg formats supported)
    
    Returns a JSON with:
    - Full transcript
    - Speaker segments with timestamps
    - Detected language
    - Audio duration
    """
    # Validate file type
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format. Supported formats: {', '.join(ALLOWED_AUDIO_TYPES)}"
        )
    
    # Check file size
    file_size = 0
    for chunk in file.file:
        file_size += len(chunk)
        if file_size > MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Maximum size: {MAX_UPLOAD_SIZE / 1024 / 1024} MB"
            )
    
    # Reset file cursor
    await file.seek(0)
    
    temp_file_path = None
    try:
        # Save the uploaded file
        temp_file_path = await save_upload_file(file)
        
        # Call the transcription service
        result = await transcription_service.transcribe_audio_with_diarization(str(temp_file_path))
        
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing audio: {str(e)}"
        )
    
    finally:
        # Clean up the temporary file
        if temp_file_path:
            remove_file(temp_file_path) 