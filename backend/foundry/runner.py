"""
Sahayak Agent Runner
Handles conversation turns and tool execution loop.
"""

import json
import os
from typing import Dict, Any, List, Optional
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Import tool dispatch from tools module
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from tools import TOOL_DISPATCH


class SahayakRunner:
    """
    Manages conversation turns and tool execution for Sahayak agent.
    Implements the standard Responses API function-calling pattern.
    """
    
    def __init__(self):
        """Initialize the runner with OpenAI client."""
        self.endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
        
        if not self.endpoint:
            raise ValueError("Missing FOUNDRY_PROJECT_ENDPOINT environment variable")
        
        self.project = AIProjectClient(
            endpoint=self.endpoint,
            credential=DefaultAzureCredential(),
        )
        
        self.openai_client = self.project.get_openai_client()
        
        # In-memory conversation storage (for hackathon)
        # In production, use Redis or database
        self.conversations: Dict[str, str] = {}
    
    def create_conversation(self, user_id: str = None) -> str:
        """
        Create a new conversation for multi-turn state.
        
        Args:
            user_id: Optional user identifier
            
        Returns:
            Conversation ID
        """
        try:
            conversation = self.openai_client.conversations.create(items=[])
            conversation_id = conversation.id
            
            # Store mapping (in production, store in database)
            if user_id:
                self.conversations[user_id] = conversation_id
            
            print(f"Created conversation: {conversation_id}")
            return conversation_id
            
        except Exception as e:
            print(f"Error creating conversation: {e}")
            raise
    
    def get_conversation(self, user_id: str) -> Optional[str]:
        """Get existing conversation ID for a user."""
        return self.conversations.get(user_id)
    
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool function locally.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
        try:
            if tool_name not in TOOL_DISPATCH:
                return {
                    "error": f"Unknown tool: {tool_name}",
                    "available_tools": list(TOOL_DISPATCH.keys())
                }
            
            # Execute the tool function
            tool_function = TOOL_DISPATCH[tool_name]
            result = tool_function(**arguments)
            
            print(f"Executed tool: {tool_name}")
            return result
            
        except Exception as e:
            print(f"Error executing tool {tool_name}: {e}")
            return {
                "error": str(e),
                "tool_name": tool_name,
                "message": "Tool execution failed. Please check arguments and try again."
            }
    
    def run_turn(
        self,
        conversation_id: str,
        user_text: str,
        max_iterations: int = 10
    ) -> Dict[str, Any]:
        """
        Execute one conversation turn with tool execution loop.
        
        Args:
            conversation_id: The conversation ID
            user_text: User's message
            max_iterations: Max number of tool call iterations (prevents infinite loops)
            
        Returns:
            Dictionary with assistant response and metadata
        """
        try:
            # Send user message
            response = self.openai_client.responses.create(
                conversation=conversation_id,
                input=[{"role": "user", "content": user_text}],
                extra_body={
                    "agent": {
                        "name": "sahayak-agent",
                        "type": "agent_reference"
                    }
                },
            )
            
            iteration = 0
            tool_calls_made = []
            
            # Tool execution loop
            while iteration < max_iterations:
                # Check if response contains function calls
                has_function_calls = False
                if response.output:
                    for item in response.output:
                        if hasattr(item, 'type') and item.type == "function_call":
                            has_function_calls = True
                            break
                
                if not has_function_calls:
                    break
                
                # Execute all function calls in this response
                outputs = []
                for item in response.output:
                    if hasattr(item, 'type') and item.type == "function_call":
                        # Parse arguments
                        try:
                            arguments = json.loads(item.arguments)
                        except json.JSONDecodeError:
                            arguments = {}
                        
                        # Execute tool
                        print(f"Executing tool: {item.name} with args: {arguments}")
                        result = self.execute_tool(item.name, arguments)
                        
                        # Track tool call
                        tool_calls_made.append({
                            "tool": item.name,
                            "arguments": arguments,
                            "result": result
                        })
                        
                        # Prepare output for next turn
                        outputs.append({
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": json.dumps(result)
                        })
                
                # Send tool results back to agent
                response = self.openai_client.responses.create(
                    conversation=conversation_id,
                    input=outputs
                )
                
                iteration += 1
            
            # Extract final text response
            final_text = ""
            if response.output:
                for item in response.output:
                    if hasattr(item, 'type') and item.type == "text":
                        final_text += item.content
            
            return {
                "success": True,
                "conversation_id": conversation_id,
                "response": final_text,
                "tool_calls": tool_calls_made,
                "iterations": iteration,
                "response_metadata": {
                    "model": response.model if hasattr(response, 'model') else None,
                    "usage": response.usage if hasattr(response, 'usage') else None,
                }
            }
            
        except Exception as e:
            print(f"Error in run_turn: {e}")
            return {
                "success": False,
                "error": str(e),
                "conversation_id": conversation_id,
                "message": "Error processing request. Please try again."
            }
    
    def get_or_create_conversation(self, user_id: str) -> str:
        """Get existing conversation or create new one for a user."""
        conversation_id = self.get_conversation(user_id)
        if not conversation_id:
            conversation_id = self.create_conversation(user_id)
        return conversation_id


# Global runner instance (for FastAPI)
_runner_instance = None


def get_runner() -> SahayakRunner:
    """Get or create the global runner instance."""
    global _runner_instance
    if _runner_instance is None:
        _runner_instance = SahayakRunner()
    return _runner_instance


__all__ = ['SahayakRunner', 'get_runner']
