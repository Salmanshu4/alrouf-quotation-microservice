# Alrouf Quotation Microservice

A FastAPI-based microservice for generating quotations with pricing calculations and AI-powered email drafts. This service handles the business logic for calculating product pricing with margins and generates professional quotation emails in multiple languages.

## Features

- **Pricing Calculations**: Automatically calculate line item totals and grand totals with configurable margins
- **Multi-language Support**: Generate quotation emails in English (EN) and Arabic (AR)
- **AI Email Drafts**: Uses OpenAI GPT to generate professional business emails
- **RESTful API**: Clean FastAPI endpoints with automatic OpenAPI documentation
- **Mock Mode**: Runs locally without requiring OpenAI API keys
- **Comprehensive Testing**: Full test coverage with pytest
- **Docker Support**: Containerized deployment ready

## Business Logic

The service implements the following pricing formula:
```
Unit Price = Unit Cost × (1 + Margin Percentage)
Line Total = Unit Price × Quantity
Grand Total = Sum of all Line Totals
```

## API Endpoints

### POST /quote
Generate a quotation with pricing calculations and email draft.

**Request Body:**
```json
{
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
```

**Response:**
```json
{
  "quotation_id": "A1B2C3D4",
  "client": { ... },
  "currency": "SAR",
  "items": [
    {
      "sku": "ALR-SL-90W",
      "qty": 120,
      "unit_cost": 240.0,
      "margin_pct": 22,
      "unit_price": 292.80,
      "line_total": 35136.0
    }
  ],
  "delivery_terms": "DAP Dammam, 4 weeks",
  "notes": "Client asked for spec compliance with Tarsheed.",
  "subtotal": 39643.6,
  "grand_total": 39643.6,
  "email_draft": "Subject: Quotation - Streetlight Poles\n\nDear Eng. Omar..."
}
```

### GET /
Health check and service information.

### GET /health
Service health status for monitoring.

### GET /docs
Interactive API documentation (Swagger UI).

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Docker (optional)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd evaluation_task
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env and add your OpenAI API key if available
   ```

5. **Run the service:**
   ```bash
   python main.py
   # Or with uvicorn directly:
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the service:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Docker Deployment

1. **Build the image:**
   ```bash
   docker build -t alrouf-quotation-service .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 alrouf-quotation-service
   ```

3. **With environment variables:**
   ```bash
   docker run -p 8000:8000 \
     -e OPENAI_API_KEY=your_key_here \
     alrouf-quotation-service
   ```

## Testing

### Run all tests:
```bash
pytest
```

### Run with coverage:
```bash
pytest --cov=main --cov-report=html
```

### Run specific test file:
```bash
pytest test_main.py
```

### Run tests with verbose output:
```bash
pytest -v
```

## Mock Mode

The service includes a mock OpenAI client that allows it to run locally without requiring API keys. When no `OPENAI_API_KEY` is provided, the service automatically switches to mock mode and generates sample email drafts.

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key for email generation | None | No (uses mock if not provided) |
| `APP_ENV` | Application environment | development | No |
| `APP_DEBUG` | Enable debug mode | true | No |
| `APP_HOST` | Host to bind to | 0.0.0.0 | No |
| `APP_PORT` | Port to bind to | 8000 | No |

## Example Usage

### Using curl:
```bash
curl -X POST "http://localhost:8000/quote" \
  -H "Content-Type: application/json" \
  -d '{
    "client": {
      "name": "Test Company",
      "contact": "test@company.com",
      "lang": "en"
    },
    "currency": "USD",
    "items": [
      {
        "sku": "TEST-001",
        "qty": 10,
        "unit_cost": 100.0,
        "margin_pct": 20
      }
    ],
    "delivery_terms": "FOB Port",
    "notes": "Test quotation"
  }'
```

### Using Python requests:
```python
import requests

url = "http://localhost:8000/quote"
data = {
    "client": {
        "name": "Test Company",
        "contact": "test@company.com",
        "lang": "en"
    },
    "currency": "USD",
    "items": [
        {
            "sku": "TEST-001",
            "qty": 10,
            "unit_cost": 100.0,
            "margin_pct": 20
        }
    ],
    "delivery_terms": "FOB Port",
    "notes": "Test quotation"
}

response = requests.post(url, json=data)
quotation = response.json()
print(f"Quotation ID: {quotation['quotation_id']}")
print(f"Total: {quotation['currency']} {quotation['grand_total']}")
```

## Error Handling

The service includes comprehensive error handling:

- **Validation Errors (422)**: Invalid input data
- **Internal Server Errors (500)**: Service errors during quotation generation
- **Detailed Error Messages**: Clear error descriptions for debugging

## Security Features

- Input validation using Pydantic models
- CORS middleware configuration
- Environment variable configuration
- No sensitive data in logs

## Performance Considerations

- Async endpoint handlers
- Efficient pricing calculations
- Mock mode for development without API costs
- Health check endpoints for monitoring

## Future Enhancements

- Database persistence for quotations
- User authentication and authorization
- Rate limiting
- Caching for frequently requested calculations
- Export to PDF functionality
- Integration with external CRM systems

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is part of the Alrouf Lighting Technology evaluation task.

## Support

For questions or issues related to this evaluation task, please contact the Alrouf Hiring Team.
