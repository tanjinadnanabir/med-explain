import io
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError


UPLOAD_DIR = Path("uploads")

ALLOWED_CONTENT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}

MAX_FILE_SIZE = 5 * 1024 * 1024

MIN_IMAGE_WIDTH = 64
MIN_IMAGE_HEIGHT = 64

MAX_IMAGE_WIDTH = 4096
MAX_IMAGE_HEIGHT = 4096


async def save_image(file: UploadFile) -> dict:
    # 1. Check MIME type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG, and WebP images are allowed.",
        )

    # 2. Read file
    content = await file.read()

    # 3. Check file size
    if len(content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is empty.",
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Image size must be 5 MB or less.",
        )

    # 4. Validate actual image content
    try:
        image = Image.open(io.BytesIO(content))

        image.verify()

    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is not a valid image.",
        )

    # 5. Re-open image after verify()
    try:
        image = Image.open(io.BytesIO(content))

        width, height = image.size

    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not read image dimensions.",
        )

    # 6. Validate dimensions
    if width < MIN_IMAGE_WIDTH or height < MIN_IMAGE_HEIGHT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Image dimensions must be at least "
                f"{MIN_IMAGE_WIDTH}x{MIN_IMAGE_HEIGHT} pixels."
            ),
        )

    if width > MAX_IMAGE_WIDTH or height > MAX_IMAGE_HEIGHT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Image dimensions must not exceed "
                f"{MAX_IMAGE_WIDTH}x{MAX_IMAGE_HEIGHT} pixels."
            ),
        )

    # 7. Create upload directory
    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # 8. Generate safe filename
    extension = ALLOWED_CONTENT_TYPES[file.content_type]

    filename = f"{uuid.uuid4()}{extension}"

    file_path = UPLOAD_DIR / filename

    # 9. Save file
    file_path.write_bytes(content)

    # 10. Return useful metadata
    return {
        "path": str(file_path),
        "filename": filename,
        "content_type": file.content_type,
        "size": len(content),
        "width": width,
        "height": height,
    }
    
def delete_image(image_path: str) -> None:
    file_path = Path(image_path)

    if file_path.exists() and file_path.is_file():
        file_path.unlink()