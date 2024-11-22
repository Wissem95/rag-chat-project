import os
from rag.document_loader import DocumentLoader
from rag.embeddings import EmbeddingManager
from rag.vector_store import VectorStore

def test_rag():
    try:
        # Créer un fichier test
        test_content = """
        Ceci est un document test pour le système RAG.
        Il contient plusieurs phrases pour tester le découpage.
        Nous allons voir comment le système gère ce contenu.
        """
        with open("test_doc.txt", "w") as f:
            f.write(test_content)

        # Initialiser les composants
        print("🔄 Initialisation des composants...")
        loader = DocumentLoader()
        embedding_manager = EmbeddingManager()
        vector_store = VectorStore(embedding_manager.get_embeddings())

        # Charger et découper le document
        print("📚 Chargement du document...")
        documents = loader.load_text("test_doc.txt")
        print(f"✅ Document découpé en {len(documents)} chunks")

        # Ajouter à la base vectorielle
        print("\n💾 Ajout à la base vectorielle...")
        vector_store.add_documents(documents)
        print("✅ Documents ajoutés")

        # Tester la recherche
        query = "Comment le système gère le contenu ?"
        print(f"\n🔍 Test de recherche pour: '{query}'")
        results = vector_store.similarity_search(query)
        print("\n📄 Résultats:")
        for doc in results:
            print(f"- {doc.page_content}")

        # Nettoyage
        os.remove("test_doc.txt")
        print("\n🧹 Nettoyage effectué")

    except Exception as e:
        print("❌ Erreur:", str(e))

if __name__ == "__main__":
    test_rag()
