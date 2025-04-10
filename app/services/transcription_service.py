from openai import OpenAI
from app.schemas.transcription import SpeakerSegment, TranscriptionResponse
from collections import Counter
from app.core.config import OPENAI_API_KEY, HUGGINGFACE_TOKEN, DIARIZATION_MODEL, OPENAI_TRANSCRIPTION_MODEL

# Conditionally import pyannote
try:
    from pyannote.audio import Pipeline
    PYANNOTE_AVAILABLE = True
except ImportError:
    PYANNOTE_AVAILABLE = False


class TranscriptionService:
    """Service for handling audio transcription with speaker diarization.
    
    This service provides:
    1. Audio transcription using OpenAI's Whisper model
    2. Speaker diarization using pyannote.audio
    3. Intelligent speaker labeling with conversation pattern detection
    """
    
    def __init__(self):
        """Initialize the transcription service with API keys and diarization pipeline."""
        self.openai_key = OPENAI_API_KEY
        self.hf_token = HUGGINGFACE_TOKEN
        self.diarization_pipeline = None
        
        # Initialize pyannote pipeline if available
        if PYANNOTE_AVAILABLE:
            try:
                self.diarization_pipeline = Pipeline.from_pretrained(
                    DIARIZATION_MODEL,
                    use_auth_token=self.hf_token
                )
            except Exception as e:
                print(f"Warning: Failed to initialize pyannote pipeline: {str(e)}")
    
    async def transcribe_audio_with_diarization(self, file_path: str) -> TranscriptionResponse:
        """Transcribe audio file with speaker diarization.
        
        Args:
            file_path: Path to the audio file to transcribe
            
        Returns:
            TranscriptionResponse object containing the transcription with speaker segments
        """
        client = OpenAI(api_key=self.openai_key)
        
        try:
            # First, get the transcription from Whisper
            with open(file_path, "rb") as audio_file:
                response = client.audio.transcriptions.create(
                    file=audio_file,
                    model=OPENAI_TRANSCRIPTION_MODEL,
                    response_format="verbose_json"
                )
            response_dict = response.model_dump()
            
            # If pyannote is available, use it for speaker diarization
            segments = []
            if self.diarization_pipeline:
                # Get speaker diarization
                diarization = self.diarization_pipeline(file_path)
                
                # Create a mapping of time ranges to speakers
                speaker_map = {}
                speaker_stats = {}
                
                # First pass: collect speaker statistics
                for turn, _, speaker in diarization.itertracks(yield_label=True):
                    if speaker not in speaker_stats:
                        speaker_stats[speaker] = {
                            "first_time": turn.start,
                            "total_time": 0
                        }
                    speaker_stats[speaker]["total_time"] += turn.end - turn.start
                    
                    # Add to speaker map with 100ms resolution
                    for t in range(int(turn.start * 100), int(turn.end * 100)):
                        speaker_map[t/100] = speaker
                
                # Match transcription segments with speaker labels
                temp_segments = []
                prev_speaker = None
                prev_text = ""
                
                for segment in response_dict.get("segments", []):
                    start = float(segment.get("start", 0))
                    end = float(segment.get("end", 0))
                    text = segment.get("text", "").strip()
                    
                    # Find speakers in this segment
                    speakers_in_segment = []
                    for t in range(int(start * 100), int(end * 100)):
                        if t/100 in speaker_map:
                            speakers_in_segment.append(speaker_map[t/100])
                    
                    if speakers_in_segment:
                        # Get most common speaker in this segment
                        speaker_counts = Counter(speakers_in_segment)
                        most_common = speaker_counts.most_common(1)[0]
                        speaker = most_common[0]
                        
                        # Handle special cases for speaker changes
                        if prev_text and prev_speaker:
                            # Check if previous segment ended with hesitation
                            ends_with_hesitation = (
                                "..." in prev_text or  # Has ellipsis
                                (  # Check for repeated words/phrases at the end
                                    len(prev_text.split()) >= 2 and
                                    prev_text.split()[-1] == prev_text.split()[-2]
                                )
                            )
                            
                            # Check if this segment completes the thought
                            is_completion = (
                                ends_with_hesitation and (
                                    # Current segment starts with the last word of previous segment
                                    text.lower().startswith(prev_text.split()[-1].lower()) or
                                    # Or current segment completes the interrupted thought
                                    len(text.split()) <= 4  # Short completion
                                )
                            )
                            
                            # If previous ended with hesitation and this completes it,
                            # use the other speaker
                            if is_completion:
                                # Find the other speaker
                                other_speakers = [s for s in speaker_stats.keys() if s != prev_speaker]
                                if other_speakers:
                                    speaker = other_speakers[0]
                    else:
                        speaker = prev_speaker if prev_speaker else list(speaker_stats.keys())[0]
                    
                    temp_segments.append({
                        "speaker": speaker,
                        "start": start,
                        "end": end,
                        "text": text
                    })
                    prev_speaker = speaker
                    prev_text = text
                
                # Normalize speaker labels based on first appearance
                sorted_speakers = sorted(
                    speaker_stats.items(),
                    key=lambda x: x[1]["first_time"]
                )
                
                speaker_mapping = {
                    speaker: f"SPEAKER_{idx+1}"
                    for idx, (speaker, _) in enumerate(sorted_speakers)
                }
                
                # Apply mapping to segments
                for segment in temp_segments:
                    segment["speaker"] = speaker_mapping[segment["speaker"]]
                
                # Convert to SpeakerSegment objects
                segments = [
                    SpeakerSegment(**segment)
                    for segment in temp_segments
                ]
            else:
                # Fallback to basic alternating speakers if pyannote is not available
                current_speaker_idx = 1
                for segment in response_dict.get("segments", []):
                    segments.append(
                        SpeakerSegment(
                            speaker=f"SPEAKER_{current_speaker_idx}",
                            start=float(segment.get("start", 0)),
                            end=float(segment.get("end", 0)),
                            text=segment.get("text", "").strip()
                        )
                    )
                    current_speaker_idx = 2 if current_speaker_idx == 1 else 1
            
            return TranscriptionResponse(
                segments=segments,
                full_transcript=response_dict.get("text", ""),
                language=response_dict.get("language", "en"),
                duration=segments[-1].end if segments else 0.0
            )
            
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            return TranscriptionResponse(
                segments=[SpeakerSegment(
                    speaker="ERROR",
                    start=0.0,
                    end=0.0,
                    text=f"Error transcribing audio: {str(e)}"
                )],
                full_transcript=f"Error transcribing audio: {str(e)}",
                language="en",
                duration=0.0
            )


# Create service instance
transcription_service = TranscriptionService() 
