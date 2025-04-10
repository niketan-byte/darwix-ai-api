import os
import shutil
from fastapi import UploadFile
from pathlib import Path
from typing import Optional

from app.core.config import UPLOAD_DIRECTORY


async def save_upload_file(upload_file: UploadFile, destination: Optional[Path] = None) -> Path:
    """
    Save an uploaded file to disk.
    
    Args:
        upload_file: The FastAPI UploadFile object
        destination: Optional destination path, if not provided uses the default upload directory
        
    Returns:
        Path to the saved file
    """
    if destination is None:
        os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
        destination = Path(UPLOAD_DIRECTORY) / upload_file.filename
    
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return destination


def remove_file(file_path: Path) -> None:
    """
    Remove a file from disk if it exists.
    
    Args:
        file_path: Path to the file to remove
    """
    if file_path.exists():
        os.remove(file_path) 