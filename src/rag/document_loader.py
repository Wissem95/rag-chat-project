import os
from minio import Minio
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
import io
import logging
from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader, PDFPlumberLoader
from langchain.schema import Document
import shutil
from fastapi import UploadFile
from pypdf import PdfReader
import pdfplumber

logger = logging.getLogger(__name__)

class MinioStorage:
    def __init__(self):
        self.client = Minio(
            "localhost:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            secure=False
        )
        self.bucket_name = "documents"
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Bucket '{self.bucket_name}' created")
        except Exception as e:
            logger.error(f"Error with bucket: {str(e)}")
            raise

    async def get_documents(self) -> List[dict]:
        try:
            documents = []
            objects = self.client.list_objects(self.bucket_name)
            
            for obj in objects:
                try:
                    data = self.client.get_object(
                        self.bucket_name,
                        obj.object_name
                    )
                    content = data.read().decode('utf-8')
                    documents.append({
                        'name': obj.object_name,
                        'content': content
                    })
                except Exception as e:
                    logger.error(f"Error reading {obj.object_name}: {str(e)}")
                finally:
                    if 'data' in locals():
                        data.close()
                        data.release_conn()
            
            return documents
        except Exception as e:
            logger.error(f"Error fetching documents: {str(e)}")
            return []

    def upload_document(self, file_name: str, content: str) -> bool:
        try:
            content_bytes = content.encode('utf-8')
            content_stream = io.BytesIO(content_bytes)
            self.client.put_object(
                self.bucket_name,
                file_name,
                content_stream,
                len(content_bytes),
                content_type='text/plain'
            )
            logger.info(f"Uploaded {file_name}")
            return True
        except Exception as e:
            logger.error(f"Upload error: {str(e)}")
            return False

class DocumentLoader:
    def __init__(self):
        self.storage = os.path.join(os.getcwd(), "documents")
        os.makedirs(self.storage, exist_ok=True)

    async def upload_document(self, file: UploadFile) -> dict:
        """Upload un document et retourne ses informations"""
        try:
            file_path = os.path.join(self.storage, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            return {
                "name": file.filename,
                "size": os.path.getsize(file_path)
            }
        except Exception as e:
            print(f"Error uploading {file.filename}: {str(e)}")
            raise e

    async def list_documents(self) -> List[dict]:
        """Liste tous les documents disponibles"""
        try:
            documents = []
            for filename in os.listdir(self.storage):
                if filename.lower().endswith(('.txt', '.pdf', '.doc', '.docx')):
                    file_path = os.path.join(self.storage, filename)
                    documents.append({
                        "name": filename,
                        "size": os.path.getsize(file_path)
                    })
            return documents
        except Exception as e:
            print(f"Error listing documents: {str(e)}")
            raise e

    async def load_documents(self, filenames: List[str]) -> List[Document]:
        documents = []
        for filename in filenames:
            file_path = os.path.join(self.storage, filename)
            logger.info(f"Tentative de lecture du fichier: {file_path}")
            
            if not os.path.exists(file_path):
                logger.warning(f"Fichier non trouvé: {file_path}")
                continue

            try:
                if filename.lower().endswith('.pdf'):
                    # Essayer avec pdfplumber
                    with pdfplumber.open(file_path) as pdf:
                        text = ""
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                        
                        if text.strip():
                            logger.info(f"Contenu extrait du PDF: {text[:100]}...")  # Log des premiers caractères
                            documents.append(Document(
                                page_content=text,
                                metadata={
                                    "source": filename,
                                    "type": "pdf"
                                }
                            ))
                            logger.info(f"PDF chargé avec succès: {filename}")
                        else:
                            # Si pdfplumber échoue, essayer PyPDFLoader
                            logger.info("Tentative avec PyPDFLoader...")
                            loader = PyPDFLoader(file_path)
                            pdf_docs = loader.load()
                            if pdf_docs:
                                documents.extend(pdf_docs)
                                logger.info(f"PDF chargé avec PyPDFLoader: {filename}")
                            else:
                                logger.warning(f"PDF illisible avec les deux méthodes: {filename}")
                
            except Exception as e:
                logger.error(f"Erreur lors du chargement de {filename}: {str(e)}")
                logger.exception(e)  # Log complet de l'erreur

        logger.info(f"Nombre total de documents chargés: {len(documents)}")
        return documents
