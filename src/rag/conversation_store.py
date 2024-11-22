import json
import os
from datetime import datetime
import uuid
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class Conversation:
    def __init__(self, id: str = None, messages: List[Dict] = None):
        self.id = id or str(uuid.uuid4())
        self.messages = messages or []
        self.timestamp = datetime.now().isoformat()

    def add_message(self, role: str, content: str):
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)

    def to_dict(self):
        return {
            "id": self.id,
            "messages": self.messages,
            "timestamp": self.timestamp,
            "title": self.messages[0]["content"][:50] if self.messages else "Nouvelle conversation",
            "messageCount": len(self.messages)
        }

class ConversationStore:
    def __init__(self, storage_dir: str = "conversations"):
        self.storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

    def get_or_create_conversation(self, conversation_id: Optional[str] = None) -> Conversation:
        if conversation_id:
            conversation_data = self.load_conversation(conversation_id)
            if conversation_data:
                return Conversation(id=conversation_id, messages=conversation_data)
        return Conversation()

    def save_conversation(self, conversation: Conversation) -> None:
        try:
            file_path = os.path.join(self.storage_dir, f"{conversation.id}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(conversation.messages, f, ensure_ascii=False, indent=2)
            logger.info(f"Conversation {conversation.id} sauvegardée")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de la conversation: {str(e)}")
            raise

    def load_conversation(self, conversation_id: str) -> List[Dict]:
        try:
            file_path = os.path.join(self.storage_dir, f"{conversation_id}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la conversation: {str(e)}")
            return []

    def list_conversations(self) -> List[Dict]:
        try:
            conversations = []
            for filename in os.listdir(self.storage_dir):
                if filename.endswith('.json'):
                    conversation_id = filename.replace('.json', '')
                    messages = self.load_conversation(conversation_id)
                    conv = Conversation(id=conversation_id, messages=messages)
                    conversations.append(conv.to_dict())
            return sorted(conversations, key=lambda x: x['timestamp'], reverse=True)
        except Exception as e:
            logger.error(f"Erreur lors du listage des conversations: {str(e)}")
            return []

    def delete_conversation(self, conversation_id: str) -> None:
        try:
            file_path = os.path.join(self.storage_dir, f"{conversation_id}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Conversation {conversation_id} supprimée")
            else:
                raise FileNotFoundError(f"Conversation {conversation_id} non trouvée")
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de la conversation: {str(e)}")
            raise
