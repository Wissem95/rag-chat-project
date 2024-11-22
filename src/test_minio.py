import os
import sys

# Ajout du chemin src au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.cloud_storage.cloud_client import CloudStorageClient

def test_minio():
    try:
        client = CloudStorageClient()
        print("✅ Connexion à MinIO réussie")
        
        # Créer un fichier test
        test_content = "Ceci est un fichier test pour MinIO!"
        with open("test_file.txt", "w") as f:
            f.write(test_content)
        
        # Upload du fichier
        print("\n📤 Upload du fichier test...")
        client.upload_file("test_file.txt")
        print("✅ Upload réussi")
        
        # Liste des fichiers
        print("\n📋 Fichiers dans le bucket:")
        files = client.list_files()
        print(files)
        
        # Download du fichier
        print("\n📥 Download du fichier...")
        client.download_file("test_file.txt", "downloaded_test.txt")
        print("✅ Download réussi")
        
        # Vérification du contenu
        with open("downloaded_test.txt", "r") as f:
            downloaded_content = f.read()
        print("\n📄 Contenu du fichier téléchargé:")
        print(downloaded_content)
        
        # Nettoyage
        os.remove("test_file.txt")
        os.remove("downloaded_test.txt")
        print("\n🧹 Nettoyage effectué")
        
    except Exception as e:
        print("❌ Erreur:", str(e))

if __name__ == "__main__":
    test_minio()
