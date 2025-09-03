#!/usr/bin/env python3
"""
Simple test script to demonstrate the quotation service functionality.
Run this after starting the service to test the API endpoints.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint."""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to service. Make sure it's running on localhost:8000")
        return False
    return True

def test_root_endpoint():
    """Test the root endpoint."""
    print("\n🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            data = response.json()
            print(f"   Service: {data['message']}")
            print(f"   Status: {data['status']}")
            print(f"   Version: {data['version']}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing root endpoint: {e}")
    return True

def test_quotation_creation():
    """Test quotation creation with the example from the task."""
    print("\n🔍 Testing quotation creation...")
    
    # Test data from the task requirements
    test_data = {
        "client": {
            "name": "Gulf Eng.",
            "contact": "omar@client.com",
            "lang": "en"
        },
        "currency": "SAR",
        "items": [
            {
                "sku": "ALR-SL-90W",
                "qty": 120,
                "unit_cost": 240.0,
                "margin_pct": 22
            },
            {
                "sku": "ALR-OBL-12V",
                "qty": 40,
                "unit_cost": 95.5,
                "margin_pct": 18
            }
        ],
        "delivery_terms": "DAP Dammam, 4 weeks",
        "notes": "Client asked for spec compliance with Tarsheed."
    }
    
    try:
        response = requests.post(f"{BASE_URL}/quote", json=test_data)
        if response.status_code == 200:
            print("✅ Quotation created successfully")
            quotation = response.json()
            
            print(f"   Quotation ID: {quotation['quotation_id']}")
            print(f"   Client: {quotation['client']['name']}")
            print(f"   Currency: {quotation['currency']}")
            print(f"   Total Items: {len(quotation['items'])}")
            
            # Verify calculations
            print("\n   📊 Pricing Details:")
            for item in quotation['items']:
                print(f"     {item['sku']}: {item['qty']} × {quotation['currency']} {item['unit_price']:.2f} = {quotation['currency']} {item['line_total']:.2f}")
            
            print(f"\n   💰 Grand Total: {quotation['currency']} {quotation['grand_total']:.2f}")
            
            # Show email draft preview
            email_draft = quotation['email_draft']
            print(f"\n   📧 Email Draft Preview:")
            print(f"     {email_draft[:100]}...")
            
        else:
            print(f"❌ Quotation creation failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error creating quotation: {e}")
    
    return True

def test_arabic_quotation():
    """Test quotation creation with Arabic language."""
    print("\n🔍 Testing Arabic quotation...")
    
    test_data = {
        "client": {
            "name": "شركة الخليج الهندسية",
            "contact": "omar@client.com",
            "lang": "ar"
        },
        "currency": "SAR",
        "items": [
            {
                "sku": "ALR-SL-90W",
                "qty": 100,
                "unit_cost": 240.0,
                "margin_pct": 20
            }
        ],
        "delivery_terms": "DAP الرياض، 3 أسابيع",
        "notes": "مطلوب توافق مع معايير ترشيد"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/quote", json=test_data)
        if response.status_code == 200:
            print("✅ Arabic quotation created successfully")
            quotation = response.json()
            print(f"   Language: {quotation['client']['lang']}")
            print(f"   Total: {quotation['currency']} {quotation['grand_total']:.2f}")
        else:
            print(f"❌ Arabic quotation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error creating Arabic quotation: {e}")
    
    return True

def test_error_handling():
    """Test error handling with invalid data."""
    print("\n🔍 Testing error handling...")
    
    # Test with invalid data (missing required fields)
    invalid_data = {
        "client": {
            "name": "Test Company"
            # Missing contact and lang
        },
        "currency": "USD",
        "items": []
    }
    
    try:
        response = requests.post(f"{BASE_URL}/quote", json=invalid_data)
        if response.status_code == 422:
            print("✅ Validation error handled correctly")
            print(f"   Status: {response.status_code}")
        else:
            print(f"❌ Expected validation error, got: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing validation: {e}")
    
    return True

def main():
    """Run all tests."""
    print("🚀 Starting Quotation Service Tests")
    print("=" * 50)
    
    # Wait a moment for service to be ready
    print("⏳ Waiting for service to be ready...")
    time.sleep(2)
    
    # Run tests
    tests = [
        test_health_check,
        test_root_endpoint,
        test_quotation_creation,
        test_arabic_quotation,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Service is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the service logs for details.")
    
    print("\n💡 Next steps:")
    print("   1. Visit http://localhost:8000/docs for interactive API documentation")
    print("   2. Use the /quote endpoint to create more quotations")
    print("   3. Check the service logs for any errors")

if __name__ == "__main__":
    main()
