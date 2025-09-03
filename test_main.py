import pytest
from fastapi.testclient import TestClient
from main import app, calculate_quotation, QuotationRequest, ClientInfo, QuotationItem

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Alrouf Quotation Microservice"
    assert data["status"] == "running"

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_create_quotation_success():
    """Test successful quotation creation."""
    request_data = {
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
    
    response = client.post("/quote", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "quotation_id" in data
    assert data["client"]["name"] == "Gulf Eng."
    assert data["currency"] == "SAR"
    assert len(data["items"]) == 2
    
    # Verify calculations
    # ALR-SL-90W: 240 * (1 + 22/100) * 120 = 240 * 1.22 * 120 = 35,136
    assert data["items"][0]["line_total"] == 35136.0
    # ALR-OBL-12V: 95.5 * (1 + 18/100) * 40 = 95.5 * 1.18 * 40 = 4,507.6
    assert data["items"][1]["line_total"] == 4507.6
    
    assert data["grand_total"] == 39643.6
    assert "email_draft" in data

def test_create_quotation_arabic():
    """Test quotation creation with Arabic language preference."""
    request_data = {
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
    
    response = client.post("/quote", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["client"]["lang"] == "ar"
    assert data["items"][0]["line_total"] == 28800.0  # 240 * 1.2 * 100

def test_create_quotation_invalid_data():
    """Test quotation creation with invalid data."""
    # Missing required fields
    request_data = {
        "client": {
            "name": "Test Company"
            # Missing contact and lang
        },
        "currency": "USD",
        "items": []
    }
    
    response = client.post("/quote", json=request_data)
    assert response.status_code == 422  # Validation error

def test_create_quotation_invalid_items():
    """Test quotation creation with invalid item data."""
    request_data = {
        "client": {
            "name": "Test Company",
            "contact": "test@company.com",
            "lang": "en"
        },
        "currency": "USD",
        "items": [
            {
                "sku": "TEST-001",
                "qty": -5,  # Invalid negative quantity
                "unit_cost": 100.0,
                "margin_pct": 15
            }
        ],
        "delivery_terms": "FOB Port",
        "notes": "Test notes"
    }
    
    response = client.post("/quote", json=request_data)
    assert response.status_code == 422  # Validation error

def test_calculate_quotation_function():
    """Test the calculate_quotation function directly."""
    request = QuotationRequest(
        client=ClientInfo(
            name="Test Company",
            contact="test@company.com",
            lang="en"
        ),
        currency="USD",
        items=[
            QuotationItem(
                sku="TEST-001",
                qty=10,
                unit_cost=100.0,
                margin_pct=20
            )
        ],
        delivery_terms="FOB Port",
        notes="Test quotation"
    )
    
    result = calculate_quotation(request)
    
    assert result.quotation_id is not None
    assert result.client.name == "Test Company"
    assert result.currency == "USD"
    assert len(result.items) == 1
    assert result.items[0].line_total == 1200.0  # 100 * 1.2 * 10
    assert result.grand_total == 1200.0
    assert result.email_draft is not None
    assert len(result.email_draft) > 0

def test_openapi_docs():
    """Test that OpenAPI documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200

def test_openapi_schema():
    """Test that OpenAPI schema is accessible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "paths" in schema
    assert "/quote" in schema["paths"]

if __name__ == "__main__":
    pytest.main([__file__])
