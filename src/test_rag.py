import os
import ast
from rag.document_loader import DocumentLoader
from rag.embeddings import EmbeddingManager
from rag.vector_store import VectorStore
from rag.chat import RAGChat

def test_rag():
    try:
        # Créer plusieurs fichiers test
        test_files = {
            "doc1.txt": """
            Ceci est un document test pour le système RAG.
            Il contient plusieurs phrases pour tester le découpage.
            Nous allons voir comment le système gère ce contenu.
            """,
            "doc2.txt": """
            Le système RAG (Retrieval-Augmented Generation) est une approche moderne.
            Il combine la recherche d'information et la génération de texte.
            Cette approche permet d'obtenir des réponses plus précises.
            """
        }
        
        for filename, content in test_files.items():
            with open(filename, "w", encoding='utf-8') as f:
                f.write(content)

        # Initialiser les composants
        print("🔄 Initialisation des composants...")
        loader = DocumentLoader()
        embedding_manager = EmbeddingManager()
        vector_store = VectorStore(embedding_manager.get_embeddings())
        
        # Charger tous les documents
        print("📚 Chargement des documents...")
        all_documents = []
        for filename in test_files.keys():
            docs = loader.load_text(filename)
            all_documents.extend(docs)
            print(f"✅ Document {filename} découpé en {len(docs)} chunks")

        # Afficher les métadonnées enrichies
        print("\n📊 Métadonnées des documents :")
        for doc in all_documents:
            print(f"\n📄 Document: {doc.metadata['filename']}")
            print(f"📈 Statistiques:")
            stats = ast.literal_eval(doc.metadata['stats'])
            for key, value in stats.items():
                print(f"  - {key}: {value}")
            print(f"🏷️  Tags: {doc.metadata['tags']}")
            print(f"📊 Complexité:")
            complexity = ast.literal_eval(doc.metadata['complexity'])
            for key, value in complexity.items():
                print(f"  - {key}: {value}")

        # Ajouter à la base vectorielle
        print("\n💾 Ajout à la base vectorielle...")
        vector_store.add_documents(all_documents)
        print("✅ Documents ajoutés")

        # Tester le chat RAG avec sauvegarde
        print("\n🤖 Test du chat RAG avec sauvegarde")
        rag_chat = RAGChat(vector_store)
        
        # Afficher l'ID de conversation
        print(f"📝 ID de conversation: {rag_chat.conversation_id}")
        
        questions = [
            "Qu'est-ce que le système RAG ?",
            "Comment fonctionne-t-il ?",
            "Quels sont les avantages de cette approche ?",
            "Peux-tu me donner un exemple concret de son utilisation ?"
        ]
        
        for question in questions:
            print(f"\n❓ Question: {question}")
            response = rag_chat.generate_response(question)
            print(f"🤖 Réponse: {response}")
        
        # Sauvegarder et charger l'historique
        saved_path = rag_chat.save_history()
        print(f"\n💾 Conversation sauvegardée dans: {saved_path}")
        
        # Lister les conversations disponibles
        conversations = rag_chat.list_conversations()
        print(f"\n📚 Conversations disponibles: {conversations}")
        
        # Charger la conversation précédente
        new_chat = RAGChat(vector_store)
        new_chat.load_history(rag_chat.conversation_id)
        print(f"\n📖 Historique chargé: {len(new_chat.conversation_history)} messages")

        # Nettoyage
        for filename in test_files.keys():
            os.remove(filename)
        print("\n🧹 Nettoyage effectué")

    except Exception as e:
        print("❌ Erreur:", str(e))

if __name__ == "__main__":
    test_rag()
