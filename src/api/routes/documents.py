from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import shutil
from src.rag.document_loader import DocumentLoader

router = APIRouter()
document_loader = DocumentLoader()

ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.doc', '.docx'}

@router.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    try:
        uploaded_files = []
        for file in files:
            result = await document_loader.upload_document(file)
            uploaded_files.append(result)
        return {"uploaded": uploaded_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_documents():
    try:
        documents = await document_loader.list_documents()
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test-connection")
async def test_minio_connection():
    try:
        loader = DocumentLoader()
        # Tente de créer le bucket si nécessaire
        loader.storage._ensure_bucket_exists()
        return {"status": "success", "message": "MinIO connection successful"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"MinIO connection failed: {str(e)}"
        )
