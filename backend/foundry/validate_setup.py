"""
Validation script to verify Sahayak agent setup
Run this to check if everything is configured correctly.
"""

import os
import sys
from pathlib import Path


def check_environment_variables():
    """Check if required environment variables are set."""
    print("Checking environment variables...")
    
    required_vars = [
        "FOUNDRY_PROJECT_ENDPOINT",
        "FOUNDRY_MODEL_DEPLOYMENT"
    ]
    
    missing = []
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"  ✓ {var}: {value}")
        else:
            print(f"  ✗ {var}: NOT SET")
            missing.append(var)
    
    if missing:
        print(f"\n❌ Missing environment variables: {', '.join(missing)}")
        print("Please set them in your .env file or environment.")
        return False
    
    print("✓ All environment variables are set\n")
    return True


def check_imports():
    """Check if required packages are installed."""
    print("Checking required packages...")
    
    packages = {
        "azure.identity": "azure-identity",
        "azure.ai.projects": "azure-ai-projects",
    }
    
    missing = []
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package}: NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    
    print("✓ All required packages are installed\n")
    return True


def check_azure_authentication():
    """Check if Azure authentication is working."""
    print("Checking Azure authentication...")
    
    try:
        from azure.identity import DefaultAzureCredential
        
        credential = DefaultAzureCredential()
        # Try to get a token (this will fail if not authenticated)
        token = credential.get_token("https://cognitiveservices.azure.com/.default")
        
        print("  ✓ Azure authentication successful")
        print(f"  Token expires: {token.expires_on}")
        print("✓ Azure authentication is working\n")
        return True
        
    except Exception as e:
        print(f"  ✗ Authentication failed: {e}")
        print("\n❌ Azure authentication failed")
        print("Please run: az login")
        return False


def check_project_structure():
    """Check if the project structure is correct."""
    print("Checking project structure...")
    
    required_files = [
        "prompts.py",
        "agent.py",
        "__init__.py",
    ]
    
    current_dir = Path(__file__).parent
    missing = []
    
    for file in required_files:
        file_path = current_dir / file
        if file_path.exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file}: NOT FOUND")
            missing.append(file)
    
    if missing:
        print(f"\n❌ Missing files: {', '.join(missing)}")
        return False
    
    print("✓ Project structure is correct\n")
    return True


def validate_system_prompt():
    """Validate that the system prompt contains required rules."""
    print("Validating system prompt...")
    
    try:
        from prompts import SAHAYAK_SYSTEM_PROMPT
        
        required_rules = [
            "NEVER INVENT",
            "CITE SOURCES",
            "NEVER CLAIM TO SUBMIT",
            "ASK ONE QUESTION",
        ]
        
        missing = []
        for rule in required_rules:
            if rule.lower() in SAHAYAK_SYSTEM_PROMPT.lower():
                print(f"  ✓ Rule present: {rule}")
            else:
                print(f"  ✗ Rule missing: {rule}")
                missing.append(rule)
        
        if missing:
            print(f"\n⚠️  Some rules may be missing from system prompt")
            return False
        
        print("✓ System prompt contains all required rules\n")
        return True
        
    except Exception as e:
        print(f"  ✗ Error loading prompt: {e}")
        return False


def main():
    """Run all validation checks."""
    print("=" * 60)
    print("Sahayak Agent Setup Validation")
    print("=" * 60 + "\n")
    
    checks = [
        ("Project Structure", check_project_structure),
        ("Environment Variables", check_environment_variables),
        ("Required Packages", check_imports),
        ("System Prompt", validate_system_prompt),
        ("Azure Authentication", check_azure_authentication),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            results.append(check_func())
        except Exception as e:
            print(f"❌ Error during {name} check: {e}\n")
            results.append(False)
    
    print("=" * 60)
    print("Validation Summary")
    print("=" * 60)
    
    for (name, _), result in zip(checks, results):
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print()
    
    if all(results):
        print("✓ All checks passed! You're ready to create the Sahayak agent.")
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
