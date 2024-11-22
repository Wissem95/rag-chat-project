import os
from minio import Minio
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
import io
import logging

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
        self.storage = MinioStorage()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    async def load_documents_from_storage(self) -> List[str]:
        documents = await self.storage.get_documents()
        split_docs = []
        for doc in documents:
            splits = self.text_splitter.split_text(doc['content'])
            split_docs.extend(splits)
        return split_docs

    def upload_document(self, file_name: str, content: str) -> bool:
        return self.storage.upload_document(file_name, content)
