"""
Chat Router - Main conversational interface
"""

from fastapi import APIRouter, HTTPException
from models.chat import ChatRequest, ChatResponse, ToolCall
from foundry.runner import get_runner

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint for conversational interaction.
    Handles multi-turn conversations with automatic tool calling.
    
    The agent can call tools like check_eligibility, get_required_documents, etc.
    as needed during the conversation.
    """
    try:
        # Get runner instance
        runner = get_runner()
        
        # Get or create conversation
        if request.conversation_id:
            conversation_id = request.conversation_id
        elif request.user_id:
            conversation_id = runner.get_or_create_conversation(request.user_id)
        else:
            # Create anonymous conversation
            conversation_id = runner.create_conversation()
        
        # Run conversation turn
        result = runner.run_turn(conversation_id, request.message)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("message", "Error processing chat request")
            )
        
        # Format tool calls for response
        tool_calls = [
            ToolCall(
                tool=tc["tool"],
                arguments=tc["arguments"],
                result=tc["result"]
            )
            for tc in result.get("tool_calls", [])
        ]
        
        return ChatResponse(
            success=True,
            response=result["response"],
            conversation_id=result["conversation_id"],
            tool_calls=tool_calls,
            iterations=result.get("iterations", 0)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat error: {str(e)}"
        )


@router.post("/chat/new")
async def new_conversation(user_id: str = None):
    """
    Create a new conversation session.
    Returns the conversation_id to use in subsequent chat calls.
    """
    try:
        runner = get_runner()
        conversation_id = runner.create_conversation(user_id)
        
        return {
            "success": True,
            "conversation_id": conversation_id,
            "user_id": user_id,
            "message": "New conversation created successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating conversation: {str(e)}"
        )


__all__ = ['router']
