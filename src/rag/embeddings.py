from langchain_ollama import OllamaEmbeddings
from src.config import OLLAMA_CONFIG

class EmbeddingManager:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            base_url=OLLAMA_CONFIG["base_url"],
            model=OLLAMA_CONFIG["model_name"]
        )

    def get_embeddings(self):
        return self.embeddings
