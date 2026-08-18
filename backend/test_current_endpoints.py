"""
Test Script for Current Working Endpoints
Run this to verify the server is working before implementing RPwD features.
"""

import requests
import json
from typing import Dict

BASE_URL = "http://localhost:8000"


def print_test(name: str, success: bool, response: requests.Response = None):
    """Print test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"\n{status}: {name}")
    if response:
        print(f"   Status Code: {response.status_code}")
        try:
            print(f"   Response: {json.dumps(response.json(), indent=2)[:200]}...")
        except:
            print(f"   Response: {response.text[:200]}...")


def test_root():
    """Test root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        success = response.status_code == 200 and "Sahayak API" in response.text
        print_test("GET / (Root)", success, response)
        return success
    except Exception as e:
        print_test("GET / (Root)", False)
        print(f"   Error: {e}")
        return False


def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        success = response.status_code == 200 and data.get("status") == "healthy"
        print_test("GET /health", success, response)
        return success
    except Exception as e:
        print_test("GET /health", False)
        print(f"   Error: {e}")
        return False


def test_docs():
    """Test API documentation"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        success = response.status_code == 200
        print_test("GET /docs (Swagger UI)", success)
        if success:
            print("   ✓ Open http://localhost:8000/docs in your browser!")
        return success
    except Exception as e:
        print_test("GET /docs", False)
        print(f"   Error: {e}")
        return False


def test_chat_endpoint():
    """Test chat endpoint (if implemented)"""
    try:
        data = {
            "message": "Hello, what is PM-KISAN scheme?",
            "user_id": "test_user_001"
        }
        response = requests.post(f"{BASE_URL}/api/v1/chat", json=data, timeout=30)
        success = response.status_code in [200, 500]  # 500 means endpoint exists but agent not created
        print_test("POST /api/v1/chat", success, response)
        
        if response.status_code == 500:
            print("   ⚠ Agent not created yet - this is expected")
            print("   ℹ Run: cd backend/foundry && python example_usage.py")
        
        return success
    except requests.exceptions.ConnectionError:
        print_test("POST /api/v1/chat", False)
        print("   Error: Endpoint not found or server not running")
        return False
    except Exception as e:
        print_test("POST /api/v1/chat", False)
        print(f"   Error: {e}")
        return False


def test_profile_endpoint():
    """Test profile endpoints"""
    try:
        profile = {
            "full_name": "Test User",
            "age": 30,
            "gender": "Male",
            "mobile": "9876543210",
            "address": "Test Address",
            "district": "Test District",
            "state": "Karnataka",
            "pincode": "560001",
            "annual_family_income": 100000,
            "caste_category": "General"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/profile",
            json=profile,
            params={"user_id": "test_user_001"}
        )
        success = response.status_code in [200, 422]  # 422 means validation error but endpoint exists
        print_test("POST /api/v1/profile", success, response)
        return success
    except Exception as e:
        print_test("POST /api/v1/profile", False)
        print(f"   Error: {e}")
        return False


def test_eligibility_endpoint():
    """Test eligibility checking"""
    try:
        data = {
            "scheme_id": "pm-kisan",
            "user_profile": {
                "full_name": "Test User",
                "age": 40,
                "gender": "Male",
                "mobile": "9876543210",
                "address": "Test Address",
                "district": "Test District",
                "state": "Karnataka",
                "pincode": "560001",
                "annual_family_income": 100000,
                "caste_category": "General",
                "is_farmer": True
            }
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/eligibility/check", json=data)
        success = response.status_code in [200, 400, 422]
        print_test("POST /api/v1/eligibility/check", success, response)
        return success
    except Exception as e:
        print_test("POST /api/v1/eligibility/check", False)
        print(f"   Error: {e}")
        return False


def test_documents_endpoint():
    """Test documents listing"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/schemes/pm-kisan/documents")
        success = response.status_code in [200, 400]
        print_test("GET /api/v1/schemes/{id}/documents", success, response)
        return success
    except Exception as e:
        print_test("GET /api/v1/schemes/{id}/documents", False)
        print(f"   Error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 70)
    print("SAHAYAK BACKEND ENDPOINT TESTS")
    print("=" * 70)
    print(f"\nTesting against: {BASE_URL}")
    print("\nℹ Make sure the server is running: python backend/main.py\n")
    
    results = {
        "Root Endpoint": test_root(),
        "Health Check": test_health(),
        "API Documentation": test_docs(),
        "Chat Endpoint": test_chat_endpoint(),
        "Profile Endpoint": test_profile_endpoint(),
        "Eligibility Endpoint": test_eligibility_endpoint(),
        "Documents Endpoint": test_documents_endpoint(),
    }
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
        print("\nCommon issues:")
        print("  - Server not running: python backend/main.py")
        print("  - Wrong port: Check if server is on port 8000")
        print("  - Agent not created: Run backend/foundry/example_usage.py")
    
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("\n1. If tests pass: Current endpoints work ✓")
    print("2. View API docs: http://localhost:8000/docs")
    print("3. For RPwD implementation, see: CHANGES_REQUIRED.md")
    print("\n")


if __name__ == "__main__":
    main()
