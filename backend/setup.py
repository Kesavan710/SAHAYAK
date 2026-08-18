"""
Sahayak Backend Setup Script
Run this to validate setup and create the agent.
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))


def check_environment():
    """Check if environment variables are set"""
    print("=" * 60)
    print("Checking Environment Variables")
    print("=" * 60)
    
    required = {
        "FOUNDRY_PROJECT_ENDPOINT": "Azure AI Foundry endpoint",
        "FOUNDRY_MODEL_DEPLOYMENT": "Model deployment name"
    }
    
    optional = {
        "BING_CONNECTION_ID": "Bing Search connection (optional)"
    }
    
    missing = []
    
    for var, desc in required.items():
        value = os.environ.get(var)
        if value:
            print(f"✓ {var}: {value}")
        else:
            print(f"✗ {var}: NOT SET - {desc}")
            missing.append(var)
    
    for var, desc in optional.items():
        value = os.environ.get(var)
        if value and value != "your-bing-connection-id-here":
            print(f"✓ {var}: {value}")
        else:
            print(f"⚠ {var}: NOT SET - {desc}")
    
    print()
    
    if missing:
        print(f"❌ Missing required variables: {', '.join(missing)}")
        print("Please set them in your .env file")
        return False
    
    print("✅ All required environment variables are set")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    print("=" * 60)
    print("Checking Dependencies")
    print("=" * 60)
    
    packages = {
        "fastapi": "FastAPI web framework",
        "uvicorn": "ASGI server",
        "pydantic": "Data validation",
        "azure.ai.projects": "Azure AI Projects SDK",
        "azure.identity": "Azure authentication",
    }
    
    missing = []
    
    for package, desc in packages.items():
        try:
            __import__(package.replace("-", "_"))
            print(f"✓ {package}: installed")
        except ImportError:
            print(f"✗ {package}: NOT INSTALLED - {desc}")
            missing.append(package)
    
    print()
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True


def create_agent_interactive():
    """Interactive agent creation"""
    print("=" * 60)
    print("Agent Creation")
    print("=" * 60)
    
    schemes_dir = input("\nEnter path to scheme documents directory (or 'skip'): ").strip()
    
    if schemes_dir.lower() == 'skip':
        print("\n⚠ Skipping agent creation")
        print("You can create the agent later using foundry/example_usage.py")
        return True
    
    if not os.path.isdir(schemes_dir):
        print(f"❌ Directory not found: {schemes_dir}")
        return False
    
    print(f"\n📁 Using scheme directory: {schemes_dir}")
    
    # Import and create agent
    try:
        from foundry import create_sahayak_agent
        
        print("\n🚀 Creating Sahayak agent...")
        print("This may take a few minutes...")
        
        manager, agent = create_sahayak_agent(schemes_dir, version_label="v1")
        
        print("\n✅ Agent created successfully!")
        print(f"   Agent ID: {agent.id}")
        print(f"   Vector Store ID: {manager.vector_store.id}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error creating agent: {e}")
        return False


def main():
    """Main setup flow"""
    print("\n" + "=" * 60)
    print("Sahayak Backend Setup")
    print("=" * 60 + "\n")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check environment
    if not check_environment():
        print("\n❌ Setup failed: Environment variables missing")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Setup failed: Dependencies missing")
        sys.exit(1)
    
    # Azure authentication check
    print("=" * 60)
    print("Azure Authentication")
    print("=" * 60)
    print("\nEnsure you are authenticated with Azure:")
    print("  Run: az login")
    input("\nPress Enter when authenticated...")
    
    # Create agent (optional)
    print("\n" + "=" * 60)
    print("Agent Creation (Optional)")
    print("=" * 60)
    print("\nYou can create the agent now or skip and do it later.")
    print("Required: A directory containing scheme PDF/JSON documents")
    
    create_now = input("\nCreate agent now? (y/n): ").strip().lower()
    
    if create_now == 'y':
        if not create_agent_interactive():
            print("\n⚠ Agent creation failed, but you can retry later")
    
    # Summary
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. If you skipped agent creation, run: python foundry/example_usage.py")
    print("2. Start the API server: python main.py")
    print("3. Access API docs: http://localhost:8000/docs")
    print("4. Test the chat endpoint with a POST request")
    print("\n✅ You're ready to build with Sahayak!")


if __name__ == "__main__":
    main()
