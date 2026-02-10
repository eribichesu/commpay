"""
Data Models Module

Pydantic models for document data validation.
"""

from datetime import date
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from decimal import Decimal


class AgencyInfo(BaseModel):
    """Agency information model."""
    
    name: str = Field(..., min_length=1, description="Agency name")
    street: str = Field(..., min_length=1, description="Street name")
    street_number: str = Field(..., min_length=1, description="Street number")
    city: str = Field(..., min_length=1, description="City")
    iban: str = Field(..., min_length=15, description="IBAN code")
    bank: str = Field(..., min_length=1, description="Bank name")
    bank_account_beneficiary: str = Field(..., min_length=1, description="Account beneficiary")


class RecipientInfo(BaseModel):
    """Recipient information model."""
    
    role: Literal["Buyer", "Seller", "Landlord", "Tenant"] = Field(
        ..., 
        description="Recipient role in the transaction"
    )
    is_company: bool = Field(default=False, description="Whether recipient is a company or individual")
    company_name: Optional[str] = Field(None, description="Company name (if company)")
    first_name: Optional[str] = Field(None, description="First name (if individual)")
    last_name: Optional[str] = Field(None, description="Last name (if individual)")
    codice_fiscale: str = Field(..., min_length=1, description="Codice Fiscale (tax code)")
    street: str = Field(..., min_length=1, description="Street address")
    city: str = Field(..., min_length=1, description="City")


class PropertyInfo(BaseModel):
    """Property information model."""
    
    city_or_location: str = Field(..., min_length=1, description="City or location")
    street: str = Field(..., min_length=1, description="Street name")
    street_number: str = Field(..., min_length=1, description="Street number")
    notes: Optional[str] = Field(None, description="Optional notes to identify the unit")


class SignatoryInfo(BaseModel):
    """Signatory information model."""
    
    name: str = Field(..., min_length=1, description="Signatory name")
    role: str = Field(..., min_length=1, description="Signatory role")


class CommissionAcknowledgementData(BaseModel):
    """
    Complete data model for commission acknowledgement documents.
    
    Supports multiple recipients.
    """
    
    # Document metadata
    document_date: date = Field(..., description="Document date")
    
    # Agency information
    agency: AgencyInfo = Field(..., description="Agency details")
    
    # Recipients (can be multiple)
    recipients: List[RecipientInfo] = Field(
        ..., 
        min_length=1,
        description="List of recipients (sellers/buyers)"
    )
    
    # Property information
    property: PropertyInfo = Field(..., description="Property details")
    
    # Signatories
    signatories: List[SignatoryInfo] = Field(
        ...,
        min_length=1,
        description="List of signatories"
    )
    
    # Deal information
    deal_type: Literal["sale", "lease"] = Field(..., description="Type of deal")
    commission_amount: Decimal = Field(..., gt=0, description="Commission amount")
    commission_due_on: str = Field(
        ..., 
        min_length=1,
        description="When commission is due (e.g., 'notary deed', 'lease contract registration')"
    )
    
    @field_validator('commission_amount', mode='before')
    @classmethod
    def validate_commission_amount(cls, v):
        """Convert commission amount to Decimal."""
        if isinstance(v, (int, float, str)):
            return Decimal(str(v))
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "document_date": "2026-02-10",
                "agency": {
                    "name": "Premium Real Estate",
                    "street": "Via Roma",
                    "street_number": "123",
                    "city": "Milano",
                    "iban": "IT60X0542811101000000123456",
                    "bank": "Intesa Sanpaolo",
                    "bank_account_beneficiary": "Premium Real Estate S.r.l."
                },
                "recipients": [
                    {
                        "role": "seller",
                        "company_name": "Acme Properties",
                        "street": "Via Dante",
                        "city": "Milano"
                    }
                ],
                "property": {
                    "city_or_location": "Milano",
                    "street": "Corso Buenos Aires",
                    "street_number": "45"
                },
                "signatories": [
                    {
                        "name": "Mario Rossi",
                        "role": "Legal Representative"
                    }
                ],
                "deal_type": "sale",
                "commission_amount": "5000.00",
                "commission_due_on": "notary deed"
            }
        }
    )
