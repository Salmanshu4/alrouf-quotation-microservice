from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from dotenv import load_dotenv
import openai
import json

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Alrouf Quotation Microservice",
    description="Generate quotations with pricing calculations and email drafts",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock OpenAI client for local development
class MockOpenAI:
    def __init__(self):
        self.api_key = "mock-key"
    
    def chat(self, **kwargs):
        class MockResponse:
            def __init__(self, content):
                self.choices = [type('obj', (object,), {'message': type('obj', (object,), {'content': content})()})]
        return MockResponse(self._generate_mock_response(kwargs.get('messages', [])))
    
    def _generate_mock_response(self, messages):
        # Mock response based on the last message
        last_message = messages[-1].get('content', '') if messages else ''
        
        if 'quotation' in last_message.lower():
            # Parse the actual quotation data from the prompt
            try:
                # Extract currency and items from the prompt
                import re
                
                # Find currency
                currency_match = re.search(r'Currency: (\w+)', last_message)
                currency = currency_match.group(1) if currency_match else "SAR"
                
                # Find items
                items_match = re.search(r'Items: \[(.*?)\]', last_message)
                if items_match:
                    items_text = items_match.group(1)
                    # Parse items like "ALR-SL-90W: 100 pcs × SAR 288.00 = SAR 28,800.00"
                    items = []
                    for item in items_text.split(', '):
                        if ':' in item and 'pcs' in item:
                            parts = item.split(': ')
                            sku = parts[0]
                            details = parts[1]
                            # Extract quantity, unit price, and line total
                            qty_match = re.search(r'(\d+) pcs', details)
                            price_match = re.search(rf'{currency} ([\d.]+)', details)
                            total_match = re.search(rf'= {currency} ([\d,]+)', details)
                            
                            if qty_match and price_match and total_match:
                                qty = qty_match.group(1)
                                price = price_match.group(1)
                                total = total_match.group(1).replace(',', '')
                                items.append(f"- {sku}: {qty} pcs × {currency} {price} = {currency} {total}")
                
                # Find total amount
                total_match = re.search(rf'Total: {currency} ([\d.]+)', last_message)
                total_amount = total_match.group(1) if total_match else "0.00"
                
                # Find delivery terms
                delivery_match = re.search(r'Delivery Terms: (.+?)(?:\n|$)', last_message)
                delivery_terms = delivery_match.group(1) if delivery_match else "Standard delivery"
                
                # Find notes
                notes_match = re.search(r'Notes: (.+?)(?:\n|$)', last_message)
                notes = notes_match.group(1) if notes_match else "None"
                
                # Generate dynamic email
                email_content = f"""Subject: Quotation - Streetlight Poles

Dear Valued Customer,

Thank you for your inquiry regarding our lighting products. Please find our quotation below:

**Quotation Summary:**
{chr(10).join(items) if items else "- No items specified"}

**Total Amount: {currency} {total_amount}**

**Delivery Terms:** {delivery_terms}
**Payment Terms:** 30% advance, 70% before shipment

**Additional Notes:** {notes}

Please let us know if you need any clarification or have questions.

Best regards,
Alrouf Lighting Technology Team
+966 11 123 4567
info@alrouf.com"""
                
                return email_content
                
            except Exception as e:
                # Fallback to generic response if parsing fails
                return f"Mock quotation email generated. Error parsing details: {str(e)}"

        return "Mock response generated for local development."

# Initialize OpenAI client (mock for local development)
if os.getenv("OPENAI_API_KEY"):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
else:
    client = MockOpenAI()

# Pydantic models
class ClientInfo(BaseModel):
    name: str = Field(..., description="Client company name")
    contact: str = Field(..., description="Client contact email")
    lang: str = Field(..., description="Language preference (en/ar)")

class QuotationItem(BaseModel):
    sku: str = Field(..., description="Product SKU")
    qty: int = Field(..., gt=0, description="Quantity")
    unit_cost: float = Field(..., gt=0, description="Unit cost in base currency")
    margin_pct: float = Field(..., ge=0, description="Margin percentage")

class QuotationRequest(BaseModel):
    client: ClientInfo
    currency: str = Field(..., description="Currency code (e.g., SAR, USD)")
    items: List[QuotationItem]
    delivery_terms: str = Field(..., description="Delivery terms")
    notes: Optional[str] = Field(None, description="Additional notes")

class QuotationLine(BaseModel):
    sku: str
    qty: int
    unit_cost: float
    margin_pct: float
    unit_price: float
    line_total: float

class QuotationResponse(BaseModel):
    quotation_id: str
    client: ClientInfo
    currency: str
    items: List[QuotationLine]
    delivery_terms: str
    notes: Optional[str]
    subtotal: float
    grand_total: float
    email_draft: str

def calculate_quotation(request: QuotationRequest) -> QuotationResponse:
    """Calculate quotation with pricing and generate email draft."""
    
    # Calculate line items
    calculated_items = []
    subtotal = 0.0
    
    for item in request.items:
        unit_price = item.unit_cost * (1 + item.margin_pct / 100)
        line_total = unit_price * item.qty
        subtotal += line_total
        
        calculated_items.append(QuotationLine(
            sku=item.sku,
            qty=item.qty,
            unit_cost=item.unit_cost,
            margin_pct=item.margin_pct,
            unit_price=round(unit_price, 2),
            line_total=round(line_total, 2)
        ))
    
    # Generate quotation ID
    import uuid
    quotation_id = str(uuid.uuid4())[:8].upper()
    
    # Generate email draft using OpenAI
    email_prompt = f"""
    Generate a professional quotation email in {request.client.lang} language for the following:
    
    Client: {request.client.name} ({request.client.contact})
    Currency: {request.currency}
    Items: {[f"{item.sku}: {item.qty} pcs × {request.currency} {item.unit_price:.2f} = {request.currency} {item.line_total:.2f}" for item in calculated_items]}
    Total: {request.currency} {subtotal:.2f}
    Delivery Terms: {request.delivery_terms}
    Notes: {request.notes or 'None'}
    
    Please format as a professional business email with subject line, greeting, quotation details, and closing.
    """
    
    try:
        response = client.chat(
            model="gpt-3.5-turbo" if os.getenv("OPENAI_API_KEY") else "mock",
            messages=[{"role": "user", "content": email_prompt}],
            max_tokens=500
        )
        email_draft = response.choices[0].message.content
    except Exception as e:
        email_draft = f"Error generating email draft: {str(e)}"
    
    return QuotationResponse(
        quotation_id=quotation_id,
        client=request.client,
        currency=request.currency,
        items=calculated_items,
        delivery_terms=request.delivery_terms,
        notes=request.notes,
        subtotal=round(subtotal, 2),
        grand_total=round(subtotal, 2),  # No additional taxes/fees in this example
        email_draft=email_draft
    )

@app.post("/quote", response_model=QuotationResponse)
async def create_quotation(request: QuotationRequest):
    """
    Create a quotation with pricing calculations and email draft.
    
    - **client**: Client information including name, contact, and language preference
    - **currency**: Currency code for pricing
    - **items**: List of products with quantities, costs, and margins
    - **delivery_terms**: Delivery terms and timeline
    - **notes**: Additional notes or requirements
    """
    try:
        quotation = calculate_quotation(request)
        return quotation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quotation: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "Alrouf Quotation Microservice",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "POST /quote": "Create quotation with pricing and email draft",
            "GET /docs": "Interactive API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "quotation-microservice"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
