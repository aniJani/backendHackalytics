import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "uploaded_files"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


async def save_file(file: UploadFile) -> str:
    file_extension = os.path.splitext(file.filename)[1]
    file_id = str(uuid.uuid4())
    file_name = f"{file_id}{file_extension}"
    file_location = os.path.join(UPLOAD_DIR, file_name)

    content = await file.read()
    with open(file_location, "wb") as buffer:
        buffer.write(content)

    return file_location
