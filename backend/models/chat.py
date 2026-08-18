"""
Chat Request/Response Models
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    
    message: str = Field(..., min_length=1, max_length=2000, description="User's message")
    user_id: Optional[str] = Field(None, description="User identifier for session management")
    conversation_id: Optional[str] = Field(None, description="Existing conversation ID for continuation")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "What is PM-KISAN scheme?",
                "user_id": "user_12345"
            }
        }


class ToolCall(BaseModel):
    """Information about a tool that was called"""
    
    tool: str
    arguments: Dict[str, Any]
    result: Dict[str, Any]


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    
    success: bool
    response: str = Field(..., description="Assistant's response text")
    conversation_id: str = Field(..., description="Conversation ID for future turns")
    tool_calls: List[ToolCall] = Field(default_factory=list, description="Tools called during this turn")
    iterations: int = Field(default=0, description="Number of tool execution iterations")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "response": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi) is a central sector scheme that provides income support to all landholding farmers' families...",
                "conversation_id": "conv_abc123",
                "tool_calls": [],
                "iterations": 0
            }
        }


__all__ = ['ChatRequest', 'ChatResponse', 'ToolCall']
