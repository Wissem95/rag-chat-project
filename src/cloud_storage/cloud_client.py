import os
import sys
from minio import Minio
from minio.error import S3Error
from typing import List, Optional
import io

# Ajout du chemin src au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.config import MINIO_CONFIG

class CloudStorageClient:
    def __init__(self):
        self.client = Minio(
            endpoint=MINIO_CONFIG["endpoint"],
            access_key=MINIO_CONFIG["access_key"],
            secret_key=MINIO_CONFIG["secret_key"],
            secure=MINIO_CONFIG["secure"]
        )
        self.bucket_name = MINIO_CONFIG["bucket_name"]
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Vérifie si le bucket existe, le crée si nécessaire."""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            raise Exception(f"Erreur lors de la création du bucket: {str(e)}")

    def upload_file(self, file_path: str, object_name: Optional[str] = None) -> str:
        """Upload un fichier vers le stockage cloud."""
        if object_name is None:
            object_name = file_path.split("/")[-1]
        
        try:
            self.client.fput_object(
                self.bucket_name, object_name, file_path
            )
            return object_name
        except S3Error as e:
            raise Exception(f"Erreur lors de l'upload: {str(e)}")

    def download_file(self, object_name: str, file_path: str) -> None:
        """Télécharge un fichier du stockage cloud."""
        try:
            self.client.fget_object(
                self.bucket_name, object_name, file_path
            )
        except S3Error as e:
            raise Exception(f"Erreur lors du téléchargement: {str(e)}")

    def list_files(self) -> List[str]:
        """Liste tous les fichiers dans le bucket."""
        try:
            objects = self.client.list_objects(self.bucket_name)
            return [obj.object_name for obj in objects]
        except S3Error as e:
            raise Exception(f"Erreur lors de la liste des fichiers: {str(e)}")
