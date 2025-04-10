from pydantic import BaseModel, Field
from typing import List, Optional


class SpeakerSegment(BaseModel):
    """Model representing a segment of speech by a speaker."""
    
    speaker: str = Field(..., description="Identifier for the speaker (e.g., 'SPEAKER_1')")
    start: float = Field(..., description="Start time of the segment in seconds")
    end: float = Field(..., description="End time of the segment in seconds")
    text: str = Field(..., description="Transcribed text for this segment")


class TranscriptionResponse(BaseModel):
    """Model for the response from the transcription API."""
    
    segments: List[SpeakerSegment] = Field(..., description="List of transcribed segments with speaker information")
    full_transcript: str = Field(..., description="Complete transcript with all segments combined")
    language: Optional[str] = Field(None, description="Detected language of the audio")
    duration: float = Field(..., description="Duration of the audio in seconds") 