from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import logging
from src.rag.conversation_store import ConversationStore
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import ConversationalRetrievalChain

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    use_rag: bool = False
    temperature: float = 0.7
    documents: List[str] = []

@router.post("/chat/")
async def chat(request: ChatRequest):
    try:
        # Initialiser Ollama
        llm = Ollama(
            model="llama2",
            base_url="http://localhost:11434",
            temperature=request.temperature
        )

        # Créer ou récupérer la conversation
        conversation_store = ConversationStore()
        conversation = conversation_store.get_or_create_conversation(request.conversation_id)
        
        # Formater l'historique pour le contexte
        chat_history = "\n".join([
            f"{'Assistant' if msg['role'] == 'assistant' else 'Human'}: {msg['content']}"
            for msg in conversation.messages
        ])
        
        # Préparer le prompt avec l'historique
        full_prompt = f"{chat_history}\nHuman: {request.message}\nAssistant:"

        if request.use_rag and request.documents:
            # Utiliser RAG seulement si demandé et documents fournis
            embeddings = OllamaEmbeddings(
                model="llama2",
                base_url="http://localhost:11434"
            )
            
            from src.rag.vector_store import VectorStore
            vector_store = VectorStore(embeddings)
            vector_store.add_documents(request.documents)
            
            chat_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=vector_store.vector_store.as_retriever(),
                return_source_documents=True
            )
            
            response = await chat_chain.ainvoke({
                "question": request.message,
                "chat_history": conversation.messages
            })
            answer = response.content
        else:
            # Sans RAG - utilisation directe du LLM avec historique
            response = await llm.ainvoke(full_prompt)
            answer = response

        # Mettre à jour la conversation
        conversation.add_message("user", request.message)
        conversation.add_message("assistant", answer)
        conversation_store.save_conversation(conversation)

        return {
            "response": answer,
            "conversation_id": conversation.id,
            "rag_used": request.use_rag
        }

    except Exception as e:
        logger.error(f"Erreur lors du chat: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

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
