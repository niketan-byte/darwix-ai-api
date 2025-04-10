# Darwix AI API

This project implements an AI-powered API providing two key features:

1. **Audio Transcription with Diarization**: Transcribes audio files and identifies different speakers in the conversation.
2. **AI Title Suggestions for Blog Posts**: Generates title suggestions for blog content using AI.

## Features

### Audio Transcription with Diarization

- **High-Quality Transcription**: Uses OpenAI's Whisper model for accurate transcription
- **Multilingual Support**: Handles 100+ languages with high accuracy
- **Advanced Speaker Diarization**: Implements Pyannote Audio to accurately identify speakers
- **Intelligent Speaker Labeling**: Uses conversation pattern detection to correctly handle hesitations, interruptions, and completions
- **Structured Output**: Returns transcription with speaker labels, timestamps, and full transcript
- **Fallback Mechanism**: Gracefully falls back to basic diarization algorithm if advanced diarization is unavailable

### Blog Post Title Suggestions

- **Smart Title Generation**: Uses GPT models to generate contextually relevant title suggestions
- **Multiple Options**: Provides 3 unique title suggestions for each blog post
- **Language-Agnostic**: Works with content in multiple languages

## Project Structure

```
darwix/
├── app/
│   ├── api/                 # API endpoints
│   │   └── endpoints/       # Route handlers for each feature
│   │       ├── transcription.py
│   │       └── title_suggestions.py
│   ├── core/                # Core configuration
│   │   └── config.py        # Environment variable configuration
│   ├── schemas/             # Pydantic models for API requests/responses
│   │   ├── transcription.py
│   │   └── title_suggestions.py
│   ├── services/            # Business logic implementation
│   │   ├── transcription_service.py
│   │   └── title_service.py
│   ├── utils/               # Utility functions
│   │   └── file_utils.py    # File handling utilities
│   ├── __init__.py
│   └── main.py              # FastAPI application setup
├── uploads/                 # Directory for temporary file uploads
├── .env                     # Environment variables (not in git repository)
├── .env.example             # Example environment variable file
├── .gitignore               # Git ignore file
├── README.md                # This file
└── requirements.txt         # Project dependencies
```

## Installation

### Prerequisites

- Python 3.9+
- OpenAI API key
- HuggingFace API key with access to Pyannote Audio models

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/darwix-ai-api.git
   cd darwix-ai-api
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Using venv
   python -m venv venv
   
   # Activate on Linux/macOS
   source venv/bin/activate
   
   # Activate on Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # Or using uv for faster installation
   uv pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   # Copy example file
   cp .env.example .env
   
   # Edit .env file with your API keys
   # Replace with actual keys
   OPENAI_API_KEY=your-openai-api-key
   HUGGINGFACE_TOKEN=your-huggingface-token
   ```

## Running the Application

Start the FastAPI application with uvicorn:

```bash
# Run with reload for development
uvicorn app.main:app --reload

# Run for production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- Base URL: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative Documentation: `http://localhost:8000/redoc`

## API Endpoints

### 1. Audio Transcription with Diarization

**Endpoint**: `POST /api/transcribe`

**Request**:
- Form data with an audio file (`file`)
- Supported formats: mp3, wav, ogg
- Maximum file size: 25MB

**Response**:
```json
{
  "segments": [
    {
      "speaker": "SPEAKER_1",
      "start": 0.0,
      "end": 2.5,
      "text": "Hello, how are you today?"
    },
    {
      "speaker": "SPEAKER_2",
      "start": 3.0,
      "end": 5.5,
      "text": "I'm doing well, thank you for asking."
    },
    {
      "speaker": "SPEAKER_2",
      "start": 5.5,
      "end": 6.5,
      "text": "And how are you..."
    },
    {
      "speaker": "SPEAKER_1",
      "start": 6.5,
      "end": 8.0,
      "text": "Doing very well, thanks!"
    }
  ],
  "full_transcript": "Hello, how are you today? I'm doing well, thank you for asking. And how are you... Doing very well, thanks!",
  "language": "en",
  "duration": 8.0
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/transcribe" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/audio.mp3"
```

### 2. Blog Post Title Suggestions

**Endpoint**: `POST /api/title-suggestions`

**Request**:
```json
{
  "content": "This is a blog post about artificial intelligence and its impact on modern society. The post discusses various applications of AI in healthcare, transportation, and education..."
}
```

**Response**:
```json
{
  "suggestions": [
    "The Revolutionary Impact of AI on Healthcare, Transportation, and Education",
    "AI in the Modern World: Transforming Our Society",
    "How Artificial Intelligence is Reshaping Our Future"
  ]
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/title-suggestions" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"content": "This is a blog post about artificial intelligence and its impact on modern society. The post discusses various applications of AI in healthcare, transportation, and education..."}'
```

## Testing

The API can be tested in several ways:

1. **Using the Swagger UI**: Navigate to `http://localhost:8000/docs` and use the interactive documentation.
2. **Using cURL commands**: Examples are provided above.
3. **Using API testing tools**: Tools like Postman or Insomnia can be used to test the API endpoints.

For the transcription feature, the best results are obtained with:
- Clear audio quality
- 2-4 speakers
- Natural conversation patterns

## Implementation Details

### Audio Transcription

The transcription feature intelligently combines:

1. **OpenAI's Whisper Model**: For high-quality speech recognition
2. **Pyannote Audio**: For state-of-the-art speaker diarization
3. **Conversation Pattern Detection**: To improve speaker labeling by analyzing:
   - Hesitations and repetitions
   - Interruptions and completions
   - Temporal patterns and speaker continuity

### Title Suggestions

The title suggestion feature uses:

1. **OpenAI's GPT Models**: To analyze content and generate creative titles
2. **Customized Prompting**: To ensure titles are engaging and relevant
3. **Multiple Options**: To give content creators choices for their headlines

## Error Handling

The API includes comprehensive error handling for:

- Invalid file formats
- File size limits
- Content length requirements
- API authentication issues
- Processing errors

## Future Improvements

- Database integration for storing transcription history
- Fine-tuned models for specific domains
- User authentication and API key management
- Advanced language-specific optimizations
- Caching for improved performance
