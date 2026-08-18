"""
Sahayak Agent Definition
Creates and configures the Azure AI Foundry agent with file search capabilities.
"""

import os
from typing import Optional, List
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from .prompts import SAHAYAK_SYSTEM_PROMPT
from .tool_definitions import get_function_tools
from .tool_definitions import get_function_tools


class SahayakAgent:
    """
    Sahayak Agent Manager
    Handles agent creation, vector store management, and scheme knowledge base.
    """
    
    def __init__(self):
        """Initialize the AI Project Client."""
        self.endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
        self.model = os.environ.get("FOUNDRY_MODEL_DEPLOYMENT")
        self.bing_connection_id = os.environ.get("BING_CONNECTION_ID")
        
        if not self.endpoint or not self.model:
            raise ValueError(
                "Missing required environment variables: "
                "FOUNDRY_PROJECT_ENDPOINT and/or FOUNDRY_MODEL_DEPLOYMENT"
            )
        
        self.project = AIProjectClient(
            endpoint=self.endpoint,
            credential=DefaultAzureCredential(),
        )
        
        self.agent = None
        self.vector_store = None
    
    def upload_scheme_documents(self, file_paths: list[str]) -> list[str]:
        """
        Upload scheme PDF/JSON documents to Azure AI.
        
        Args:
            file_paths: List of file paths to scheme documents
            
        Returns:
            List of file IDs for uploaded documents
        """
        file_ids = []
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"Warning: File not found: {file_path}")
                continue
            
            try:
                with open(file_path, 'rb') as f:
                    uploaded_file = self.project.agents.files.upload(
                        file=f,
                        purpose="assistants"
                    )
                    file_ids.append(uploaded_file.id)
                    print(f"Uploaded: {file_path} -> {uploaded_file.id}")
            except Exception as e:
                print(f"Error uploading {file_path}: {e}")
        
        return file_ids
    
    def create_vector_store(self, file_ids: list[str]):
        """
        Create a vector store for scheme knowledge base.
        
        Args:
            file_ids: List of uploaded file IDs
            
        Returns:
            VectorStore object
        """
        print(f"Creating vector store with {len(file_ids)} files...")
        
        self.vector_store = self.project.agents.vector_stores.create_and_poll(
            file_ids=file_ids,
            name="sahayak-schemes",
        )
        
        print(f"Vector store created: {self.vector_store.id}")
        return self.vector_store
    
    def create_agent(
        self,
        vector_store_id: Optional[str] = None,
        version_label: str = "v1",
        enable_bing_search: bool = True,
        enable_function_tools: bool = True,
    ):
        """
        Create the Sahayak agent with file search tool.
        
        Args:
            vector_store_id: Optional vector store ID. If None, uses self.vector_store
            version_label: Version label for the agent
            enable_bing_search: Whether to enable Bing grounding for live deadlines
            enable_function_tools: Whether to enable custom function tools
            
        Returns:
            Created agent object
        """
        # Determine vector store ID
        if vector_store_id is None:
            if self.vector_store is None:
                raise ValueError(
                    "No vector store available. Call create_vector_store first "
                    "or provide vector_store_id."
                )
            vector_store_id = self.vector_store.id
        
        # Build tools list
        tools = []
        
        # 1. File Search Tool (scheme knowledge base)
        file_search = FileSearchTool(
            vector_store_ids=[vector_store_id]
        )
        tools.extend(file_search.definitions)
        
        # 2. Bing Grounding Tool (live deadline search)
        if enable_bing_search and self.bing_connection_id:
            try:
                bing_tool = BingGroundingAgentTool(
                    bing_grounding=BingGroundingSearchToolParameters(
                        search_configurations=[
                            BingGroundingSearchConfiguration(
                                connection_id=self.bing_connection_id
                            )
                        ]
                    )
                )
                tools.extend(bing_tool.definitions)
                print("  ✓ Bing Search enabled for live deadline grounding")
            except Exception as e:
                print(f"  ⚠ Bing Search setup skipped: {e}")
                print("    (Continue with File Search only)")
        elif enable_bing_search:
            print("  ⚠ Bing Search disabled: BING_CONNECTION_ID not set")
        
        # 3. Function Tools (custom eligibility, documents, etc.)
        if enable_function_tools:
            function_tools = get_function_tools()
            tools.extend(function_tools)
            print(f"  ✓ Added {len(function_tools)} custom function tools")
        
        # Create agent with prompt definition
        print(f"Creating agent with model: {self.model}")
        
        self.agent = self.project.agents.create_version(
            agent_name="sahayak-agent",
            definition=PromptAgentDefinition(
                model=self.model,
                instructions=SAHAYAK_SYSTEM_PROMPT,
                tools=tools,
            ),
            version_label=version_label,
        )
        
        print(f"Agent created: {self.agent.id}")
        return self.agent
    
    def setup_from_directory(
        self,
        schemes_dir: str,
        version_label: str = "v1"
    ):
        """
        Complete setup: upload documents, create vector store, and create agent.
        
        Args:
            schemes_dir: Directory containing scheme PDF/JSON files
            version_label: Version label for the agent
            
        Returns:
            Created agent object
        """
        # Find all scheme documents
        import glob
        
        file_patterns = [
            os.path.join(schemes_dir, "*.pdf"),
            os.path.join(schemes_dir, "*.json"),
        ]
        
        file_paths = []
        for pattern in file_patterns:
            file_paths.extend(glob.glob(pattern))
        
        if not file_paths:
            raise ValueError(f"No scheme documents found in {schemes_dir}")
        
        print(f"Found {len(file_paths)} scheme documents")
        
        # Upload documents
        file_ids = self.upload_scheme_documents(file_paths)
        
        if not file_ids:
            raise ValueError("No files were successfully uploaded")
        
        # Create vector store
        self.create_vector_store(file_ids)
        
        # Create agent
        return self.create_agent(version_label=version_label)


# Convenience function for quick setup
def create_sahayak_agent(schemes_dir: str, version_label: str = "v1"):
    """
    Quick setup function to create Sahayak agent with scheme knowledge base.
    
    Args:
        schemes_dir: Directory containing scheme PDF/JSON files
        version_label: Version label for the agent
        
    Returns:
        Tuple of (SahayakAgent instance, created agent object)
    """
    manager = SahayakAgent()
    agent = manager.setup_from_directory(schemes_dir, version_label)
    return manager, agent


__all__ = ['SahayakAgent', 'create_sahayak_agent']
