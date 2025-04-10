import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_PREFIX = "/api"
PROJECT_NAME = "Darwix AI API"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# HuggingFace Configuration
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN") or os.getenv("HF_API_KEY")

# File Upload Configuration
MAX_UPLOAD_SIZE = 25 * 1024 * 1024  # 25 MB
ALLOWED_AUDIO_TYPES = ["audio/mpeg", "audio/mp3", "audio/wav", "audio/ogg"]
UPLOAD_DIRECTORY = "uploads"

# Models Configuration
OPENAI_TRANSCRIPTION_MODEL = "whisper-1"
OPENAI_TITLE_MODEL = "gpt-4o-mini"
DIARIZATION_MODEL = "pyannote/speaker-diarization-3.1" 