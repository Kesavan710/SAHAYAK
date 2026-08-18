"""
Example usage of the Sahayak Agent

This script demonstrates how to:
1. Upload scheme documents
2. Create a vector store
3. Create the Sahayak agent with file search
"""

import os
from pathlib import Path
from agent import SahayakAgent, create_sahayak_agent


def example_full_setup():
    """
    Example: Complete setup from a directory of scheme documents.
    """
    # Path to directory containing scheme PDFs/JSONs
    schemes_directory = "/path/to/scheme/documents"
    
    # Create agent with all documents in directory
    manager, agent = create_sahayak_agent(
        schemes_dir=schemes_directory,
        version_label="v1"
    )
    
    print(f"Agent created successfully!")
    print(f"Agent ID: {agent.id}")
    print(f"Vector Store ID: {manager.vector_store.id}")
    
    return manager, agent


def example_step_by_step():
    """
    Example: Step-by-step setup with more control.
    """
    # Initialize manager
    manager = SahayakAgent()
    
    # Upload specific documents
    scheme_files = [
        "/path/to/pm-kisan.pdf",
        "/path/to/ayushman-bharat.pdf",
        "/path/to/pradhan-mantri-awas-yojana.pdf",
    ]
    
    file_ids = manager.upload_scheme_documents(scheme_files)
    print(f"Uploaded {len(file_ids)} documents")
    
    # Create vector store
    vector_store = manager.create_vector_store(file_ids)
    print(f"Created vector store: {vector_store.id}")
    
    # Create agent
    agent = manager.create_agent(version_label="v1")
    print(f"Created agent: {agent.id}")
    
    return manager, agent


def example_reuse_existing_vector_store():
    """
    Example: Create agent using an existing vector store.
    """
    manager = SahayakAgent()
    
    # If you already have a vector store ID
    existing_vector_store_id = "vs_xxxxxxxxxxxxx"
    
    agent = manager.create_agent(
        vector_store_id=existing_vector_store_id,
        version_label="v2"
    )
    
    print(f"Created agent with existing vector store")
    print(f"Agent ID: {agent.id}")
    
    return manager, agent


if __name__ == "__main__":
    # Choose one example:
    
    # Option 1: Full automated setup
    # manager, agent = example_full_setup()
    
    # Option 2: Step-by-step with control
    # manager, agent = example_step_by_step()
    
    # Option 3: Reuse existing vector store
    # manager, agent = example_reuse_existing_vector_store()
    
    print("\nExample usage script - uncomment the option you want to use")
