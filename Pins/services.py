from fastapi import UploadFile
import aiofiles

async def upload_file(file: UploadFile):
    async with aiofiles.open(file.filename, "wb") as buffer:
        data = await file.read()
        await buffer.write(data)

def file_validator(file: UploadFile):
    if ("image" in file.content_type or "video" not in file.content_type) and file.size < 209715200:
        return True
    return False

