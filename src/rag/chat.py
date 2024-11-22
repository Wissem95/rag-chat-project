from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage
from src.config import OLLAMA_CONFIG
import requests
import json
from typing import List, Dict, Optional
from datetime import datetime
from src.rag.conversation_store import ConversationStore
import uuid
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGChat:
    def __init__(self, vector_store):
        logger.info("Initialisation de RAGChat")
        self.vector_store = vector_store
        self.conversation_store = ConversationStore()
        self.conversation_id = str(uuid.uuid4())
        logger.info(f"Conversation ID créé: {self.conversation_id}")

    def get_context(self, query: str, k: int = 2) -> str:
        """Récupère le contexte pertinent pour la requête"""
        try:
            relevant_docs = self.vector_store.similarity_search(query, k=k)
            context_parts = []
            
            for doc in relevant_docs:
                metadata = doc.metadata
                source_info = f"Source: {metadata.get('filename', 'Inconnu')}"
                date_info = f"Date: {metadata.get('date_added', 'Inconnue')}"
                content = doc.page_content
                context_parts.append(f"{source_info}\n{date_info}\n\nContenu:\n{content}\n")
            
            return "\n---\n".join(context_parts)
        except Exception as e:
            print(f"Erreur lors de la recherche de contexte: {str(e)}")
            return ""

    def _build_prompt(self, query: str, context: str) -> str:
        """Construit le prompt avec l'historique"""
        conversation_context = "\n".join([
            f"{'Question' if msg['role'] == 'user' else 'Réponse'}: {msg['content']}"
            for msg in self.conversation_history[-2:]  # Utiliser les 2 derniers messages
        ])

        return f"""Tu es un assistant expert qui aide à comprendre des documents.

Instructions :
- Utilise UNIQUEMENT le contexte fourni pour répondre
- Sois précis et détaillé dans tes réponses
- Si une information n'est pas dans le contexte, dis-le clairement
- Cite des parties du texte pour appuyer tes réponses
- Prends en compte l'historique de la conversation pour plus de cohérence

Historique récent de la conversation :
{conversation_context}

Contexte des documents :
{context}

Question actuelle : {query}

Réponse détaillée :"""

    def save_history(self):
        """Sauvegarde l'historique de la conversation"""
        return self.conversation_store.save_conversation(
            self.conversation_id, 
            self.conversation_history
        )

    def load_history(self, conversation_id: str):
        """Charge l'historique d'une conversation"""
        self.conversation_id = conversation_id
        self.conversation_history = self.conversation_store.load_conversation(conversation_id)

    def list_conversations(self):
        """Liste toutes les conversations disponibles"""
        return self.conversation_store.list_conversations()

    def generate_response(self, query: str, conversation_id: Optional[str] = None) -> str:
        try:
            logger.info(f"Génération de réponse pour: {query}")
            
            # Utiliser le conversation_id fourni ou celui créé
            self.conversation_id = conversation_id or self.conversation_id
            logger.info(f"Utilisation du conversation_id: {self.conversation_id}")

            # Rechercher les documents pertinents
            logger.info("Recherche de documents pertinents")
            relevant_docs = self.vector_store.similarity_search(query)
            logger.info(f"Nombre de documents trouvés: {len(relevant_docs)}")

            # Générer la réponse avec le contexte
            logger.info("Génération de la réponse avec le contexte")
            response = self._generate_response_with_context(query, relevant_docs)
            logger.info(f"Réponse générée: {response[:100]}...")  # Log des 100 premiers caractères

            # Sauvegarder la conversation
            logger.info("Sauvegarde de la conversation")
            self.conversation_store.save_message(self.conversation_id, "user", query)
            self.conversation_store.save_message(self.conversation_id, "assistant", response)

            return response

        except Exception as e:
            logger.error(f"Erreur dans generate_response: {str(e)}", exc_info=True)
            raise Exception(f"Erreur lors de la génération de la réponse: {str(e)}")

    def _generate_response_with_context(self, query: str, relevant_docs: list) -> str:
        try:
            # Construire le contexte à partir des documents pertinents
            context = "\n".join([doc.page_content for doc in relevant_docs])
            logger.info(f"Contexte construit avec {len(relevant_docs)} documents")

            # Utiliser le modèle pour générer la réponse
            from src.llm.ollama_client import get_ollama_response
            response = get_ollama_response(query, context)
            
            return response

        except Exception as e:
            logger.error(f"Erreur dans _generate_response_with_context: {str(e)}", exc_info=True)
            raise
