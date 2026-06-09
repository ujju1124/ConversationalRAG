"""Router for conversational RAG API."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.schemas import ChatRequest, ChatResponse
from app.services.retrieval_service import retrieve_relevant_chunks
from app.services.memory_service import get_chat_history, save_conversation_turn
from app.services.llm_service import generate_rag_response
from app.services.booking_service import process_booking

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    db: Session = Depends(get_db)
) -> ChatResponse:
    """Conversational RAG endpoint with booking detection."""
    
    try:
        # Step 1: Retrieve relevant chunks from Pinecone
        context_chunks = retrieve_relevant_chunks(
            user_message=request.user_message,
            document_id=request.document_id,
            top_k=5
        )
        
        if not context_chunks:
            raise HTTPException(
                status_code=404, 
                detail=f"No relevant context found for document_id: {request.document_id}"
            )
        
        # Step 2: Fetch chat history from Redis
        chat_history = get_chat_history(request.session_id, max_messages=6)
        
        # Step 3: Generate RAG response using Groq
        assistant_response = generate_rag_response(
            context_chunks=context_chunks,
            chat_history=chat_history,
            user_message=request.user_message
        )
        
        # Step 4: Save conversation to Redis
        save_conversation_turn(
            session_id=request.session_id,
            user_message=request.user_message,
            assistant_response=assistant_response
        )
        
        # Step 5: Check for booking intent and extract information
        booking_data = process_booking(
            db=db,
            session_id=request.session_id,
            user_message=request.user_message,
            chat_history=chat_history
        )
        
        # Build response
        response = ChatResponse(
            response=assistant_response,
            session_id=request.session_id,
            booking=booking_data
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
