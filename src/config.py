import os
from pathlib import Path
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Chemin de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuration Cloud Storage (MinIO)
MINIO_CONFIG = {
    "endpoint": os.getenv("MINIO_ENDPOINT", "localhost:9000"),
    "access_key": os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
    "secret_key": os.getenv("MINIO_SECRET_KEY", "minioadmin"),
    "bucket_name": os.getenv("MINIO_BUCKET_NAME", "rag-documents"),
    "secure": False  # Mettre à True pour HTTPS
}

# Configuration Ollama
OLLAMA_CONFIG = {
    "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    "model_name": os.getenv("MODEL_NAME", "mistral")
}

# Configuration Vector Store
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./data/vector_store")

# Configuration RAG
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Paramètres LLM par défaut
DEFAULT_LLM_PARAMS = {
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 512
}
