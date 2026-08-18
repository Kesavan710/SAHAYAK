"""
API Test Script
Tests all Sahayak API endpoints with example data.
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


def print_response(title: str, response: requests.Response):
    """Pretty print API response"""
    print("\n" + "=" * 60)
    print(f"{title}")
    print("=" * 60)
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)


def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response.status_code == 200


def test_chat():
    """Test chat endpoint"""
    data = {
        "message": "What is PM-KISAN scheme? Who is eligible?",
        "user_id": "test_user_001"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/chat", json=data)
    print_response("Chat - PM-KISAN Query", response)
    
    if response.status_code == 200:
        result = response.json()
        return result.get("conversation_id")
    return None


def test_profile():
    """Test profile creation"""
    profile_data = {
        "full_name": "Rajesh Kumar",
        "father_name": "Suresh Kumar",
        "date_of_birth": "1985-05-15",
        "age": 39,
        "gender": "Male",
        "mobile": "9876543210",
        "email": "rajesh.kumar@example.com",
        "address": "123, Main Street, Village Rampur",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "pincode": "221001",
        "aadhaar": "123456789012",
        "bank_account_number": "1234567890",
        "bank_ifsc": "SBIN0001234",
        "annual_family_income": 120000,
        "caste_category": "OBC",
        "occupation": "Farmer",
        "is_bpl": False,
        "has_ration_card": True,
        "is_farmer": True,
        "land_holding_acres": 2.5
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/profile",
        json=profile_data,
        params={"user_id": "test_user_001"}
    )
    print_response("Profile Creation", response)
    return response.status_code == 200


def test_eligibility():
    """Test eligibility check"""
    data = {
        "scheme_id": "pm-kisan",
        "user_profile": {
            "full_name": "Rajesh Kumar",
            "age": 39,
            "gender": "Male",
            "mobile": "9876543210",
            "address": "Village Rampur",
            "district": "Varanasi",
            "state": "Uttar Pradesh",
            "pincode": "221001",
            "annual_family_income": 120000,
            "caste_category": "General",
            "is_farmer": True,
            "land_holding_acres": 2.5
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/eligibility/check", json=data)
    print_response("Eligibility Check - PM-KISAN", response)
    return response.status_code == 200


def test_documents():
    """Test documents endpoint"""
    response = requests.get(f"{BASE_URL}/api/v1/schemes/pm-kisan/documents")
    print_response("Required Documents - PM-KISAN", response)
    return response.status_code == 200


def test_application():
    """Test application package generation"""
    data = {
        "scheme_id": "pm-kisan",
        "output_format": "both",
        "user_profile": {
            "full_name": "Rajesh Kumar",
            "father_name": "Suresh Kumar",
            "mother_name": "Geeta Devi",
            "date_of_birth": "1985-05-15",
            "age": 39,
            "gender": "Male",
            "mobile": "9876543210",
            "email": "rajesh.kumar@example.com",
            "address": "123, Main Street, Village Rampur",
            "district": "Varanasi",
            "state": "Uttar Pradesh",
            "pincode": "221001",
            "aadhaar": "123456789012",
            "bank_account_number": "1234567890",
            "bank_ifsc": "SBIN0001234",
            "annual_family_income": 120000,
            "caste_category": "OBC",
            "occupation": "Farmer",
            "is_bpl": False,
            "has_ration_card": True,
            "is_farmer": True,
            "land_holding_acres": 2.5
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/application/package", json=data)
    print_response("Application Package Generation", response)
    return response.status_code == 200


def test_status():
    """Test status check"""
    data = {
        "scheme_id": "pm-kisan",
        "application_id": "PM-KISAN-2024-12345",
        "mobile_or_aadhaar": "9876543210"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/status/check", json=data)
    print_response("Application Status Check", response)
    return response.status_code == 200


def test_conversation_flow():
    """Test multi-turn conversation"""
    print("\n" + "=" * 60)
    print("Testing Multi-Turn Conversation Flow")
    print("=" * 60)
    
    # Turn 1: Initial query
    response1 = requests.post(
        f"{BASE_URL}/api/v1/chat",
        json={
            "message": "I am a farmer from Uttar Pradesh. What schemes can I apply for?",
            "user_id": "test_user_002"
        }
    )
    print_response("Turn 1: Initial Query", response1)
    
    if response1.status_code != 200:
        return False
    
    conv_id = response1.json().get("conversation_id")
    
    # Turn 2: Follow-up question
    response2 = requests.post(
        f"{BASE_URL}/api/v1/chat",
        json={
            "message": "Tell me more about PM-KISAN. Am I eligible if my income is 1.5 lakh per year?",
            "conversation_id": conv_id
        }
    )
    print_response("Turn 2: Follow-up", response2)
    
    # Turn 3: Application help
    response3 = requests.post(
        f"{BASE_URL}/api/v1/chat",
        json={
            "message": "How do I apply? What documents do I need?",
            "conversation_id": conv_id
        }
    )
    print_response("Turn 3: Application Help", response3)
    
    return response3.status_code == 200


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Sahayak API Test Suite")
    print("=" * 60)
    print(f"Testing against: {BASE_URL}")
    print("\nMake sure the server is running: python main.py")
    input("\nPress Enter to start tests...")
    
    results = {}
    
    # Run tests
    print("\n🧪 Running API tests...\n")
    
    results["Health Check"] = test_health()
    results["Chat"] = test_chat()
    results["Profile"] = test_profile()
    results["Eligibility"] = test_eligibility()
    results["Documents"] = test_documents()
    results["Application"] = test_application()
    results["Status"] = test_status()
    results["Conversation Flow"] = test_conversation_flow()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")


if __name__ == "__main__":
    main()
