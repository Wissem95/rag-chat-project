from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from typing import List
import logging
import os
import pickle

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, embeddings):
        self.embeddings = embeddings
        self.vector_store = None
        self.storage_path = "data/vector_store.pkl"
        self._load_or_create_store()

    def _load_or_create_store(self):
        """Charge le vector store existant ou en crée un nouveau"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'rb') as f:
                    self.vector_store = pickle.load(f)
                logger.info("Vector store chargé depuis le fichier")
                return
            except Exception as e:
                logger.error(f"Erreur lors du chargement du vector store: {e}")
        
        self.vector_store = None

    def _save_store(self):
        """Sauvegarde le vector store sur le disque"""
        if self.vector_store:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, 'wb') as f:
                pickle.dump(self.vector_store, f)
            logger.info("Vector store sauvegardé")

    def has_documents(self) -> bool:
        return self.vector_store is not None

    def add_documents(self, texts: List[str]):
        try:
            documents = [
                Document(
                    page_content=text,
                    metadata={"source": f"doc_{i}"}
                ) 
                for i, text in enumerate(texts)
            ]

            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(documents, self.embeddings)
            else:
                self.vector_store.add_documents(documents)
            
            self._save_store()  # Sauvegarder après l'ajout
            logger.info(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise

    def similarity_search(self, query: str, k: int = 4):
        if self.vector_store is None:
            logger.warning("Vector store is empty")
            return []
        
        try:
            return self.vector_store.similarity_search(query, k=k)
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            return []
