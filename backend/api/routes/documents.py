from fastapi import APIRouter, File, UploadFile

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)) -> dict:
    return {
        "uploaded": True,
        "filename": file.filename,
        "message": "Document received for processing",
    }
