import requests
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_ollama_response(query: str, context: str = "") -> str:
    try:
        logger.info("Envoi de la requête à Ollama")
        
        # Construire le prompt avec le contexte
        prompt = f"""Contexte: {context}

Question: {query}

Réponse:"""

        # Appel à l'API Ollama
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'mistral',
                'prompt': prompt,
                'stream': False
            }
        )
        
        logger.info("Réponse reçue d'Ollama")
        response_json = response.json()
        
        if 'response' in response_json:
            return response_json['response']
        else:
            logger.error(f"Réponse Ollama invalide: {response_json}")
            return "Désolé, je n'ai pas pu générer une réponse cohérente."

    except Exception as e:
        logger.error(f"Erreur lors de l'appel à Ollama: {str(e)}", exc_info=True)
        raise Exception(f"Erreur lors de l'appel à Ollama: {str(e)}")
