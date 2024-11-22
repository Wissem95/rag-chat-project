from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import logging
from src.rag.conversation_store import ConversationStore
from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain.chains import ConversationalRetrievalChain
from src.rag.document_loader import DocumentLoader
from src.rag.vector_store import VectorStore

router = APIRouter()
logger = logging.getLogger(__name__)

# Créer les embeddings
embeddings = OllamaEmbeddings(
    model="llama2",
    base_url="http://localhost:11434"
)

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    use_rag: bool = False
    temperature: float = 0.7
    documents: List[str] = []

@router.post("/chat/")
async def chat(request: ChatRequest):
    try:
        llm = OllamaLLM(
            model="llama2",
            base_url="http://localhost:11434",
            temperature=0.3
        )

        if request.use_rag and request.documents:
            document_loader = DocumentLoader()
            documents = await document_loader.load_documents(request.documents)
            
            if not documents:
                return {"response": "Aucun document valide n'a été trouvé."}

            # Extraction du contenu avec plus de détails
            document_contents = []
            for doc in documents:
                content = doc.page_content.strip()
                if content:
                    document_contents.append(content)

            context = "\n\n".join(document_contents)
            
            enhanced_prompt = f"""Tu es un assistant précis et direct.

Document analysé : {request.documents[0]}
Contenu du document :
{context}

Question : {request.message}

Instructions :
1. Décris exactement ce qu'est ce fichier (type, nom, contenu principal)
2. Résume brièvement les informations principales qu'il contient
3. Si tu ne peux pas lire certaines parties, indique-le clairement

Réponds en français de manière concise et structurée."""

            response = await llm.ainvoke(enhanced_prompt)
            return {"response": response}
        else:
            response = await llm.ainvoke(request.message)
            return {"response": response}

    except Exception as e:
        logger.error(f"Erreur lors du chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    try:
        conversation_store = ConversationStore()
        conversation = conversation_store.load_conversation(conversation_id)
        return conversation
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Conversation not found: {str(e)}")

@router.get("/conversations")
async def list_conversations():
    try:
        conversation_store = ConversationStore()
        conversations = conversation_store.list_conversations()
        return {"conversations": conversations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    try:
        conversation_store = ConversationStore()
        conversation_store.delete_conversation(conversation_id)
        return {"message": f"Conversation {conversation_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error deleting conversation: {str(e)}")
