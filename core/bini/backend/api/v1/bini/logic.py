import os
from backend.settings import Config
from backend.utils.logger import Logfire
from fastapi import APIRouter, HTTPException


log = Logfire(name='bini-helper-functions')

router = APIRouter(prefix=f"/api/{Config.API_VERSION}/bini", tags=["bini"])

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}

MAX_FILE_SIZE = 100 * 1024 * 1024

TEXT_ALLOWED_EXTENSIONS = {".txt", ".json", ".csv"}


def validate_image_file(filename: str, size: int) -> str:
    """
    Validate an uploaded image file and return its extension.
    """
    if not filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    return file_ext


def validate_text_file(filename: str, size: int) -> str:
    if not filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    ext = os.path.splitext(filename)[1].lower()
    if ext not in TEXT_ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(TEXT_ALLOWED_EXTENSIONS))
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {allowed}")
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    return ext


def decode_text_bytes(data: bytes) -> str:
    # Try UTF-8 first, then common fallbacks; never crash.
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        for enc in ("utf-16", "latin-1"):
            try:
                return data.decode(enc)
            except UnicodeDecodeError:
                continue
    # Fallback with replacement characters
    return data.decode("utf-8", errors="replace")
