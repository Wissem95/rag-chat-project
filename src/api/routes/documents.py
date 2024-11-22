from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
from src.rag.document_loader import DocumentLoader
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    try:
        loader = DocumentLoader()
        results = []
        
        for file in files:
            try:
                content = await file.read()
                # Essayons de détecter l'encodage ou utiliser 'latin-1' comme fallback
                try:
                    content_str = content.decode('utf-8')
                except UnicodeDecodeError:
                    content_str = content.decode('latin-1')
                
                success = loader.upload_document(file.filename, content_str)
                
                results.append({
                    "filename": file.filename,
                    "success": success
                })
                
            except Exception as e:
                logger.error(f"Error processing file {file.filename}: {str(e)}")
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "error": str(e)
                })
        
        return {
            "message": "Upload process completed",
            "results": results
        }
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_documents():
    try:
        loader = DocumentLoader()
        documents = await loader.storage.get_documents()
        return {
            "documents": [
                {
                    "name": doc["name"],
                    "size": len(doc["content"])
                }
                for doc in documents
            ]
        }
    except Exception as e:
        logger.error(f"List error: {str(e)}")
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
