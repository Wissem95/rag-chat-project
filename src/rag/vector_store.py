from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from typing import List
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, embeddings):
        self.embeddings = embeddings
        self.vector_store = None

    def add_documents(self, documents: List[Document]) -> None:
        try:
            # Vérifier et nettoyer les documents
            valid_documents = []
            for doc in documents:
                if hasattr(doc, 'page_content') and isinstance(doc.page_content, str) and doc.page_content.strip():
                    valid_documents.append(Document(
                        page_content=doc.page_content,
                        metadata=doc.metadata if hasattr(doc, 'metadata') else {}
                    ))
            
            if not valid_documents:
                logger.warning("No valid documents to add to vector store")
                return

            # Créer ou mettre à jour le vector store
            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(valid_documents, self.embeddings)
            else:
                self.vector_store.add_documents(valid_documents)
                
            logger.info(f"Added {len(valid_documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise
