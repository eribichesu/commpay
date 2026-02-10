"""
Tests for DocumentBuilder
"""

import pytest
from datetime import date
from decimal import Decimal
from pathlib import Path
from commpay.builder import DocumentBuilder
from commpay.models import (
    CommissionAcknowledgementData,
    CreditNoteData,
    AgencyInfo,
    RecipientInfo,
    PropertyInfo,
    SignatoryInfo,
)


@pytest.fixture
def sample_agency():
    """Sample agency information."""
    return AgencyInfo(
        name="Test Real Estate",
        street="Via Roma",
        street_number="123",
        city="Milano",
        iban="IT60X0542811101000000123456",
        bank="Test Bank",
        bank_account_beneficiary="Test Real Estate S.r.l."
    )


@pytest.fixture
def sample_recipient():
    """Sample recipient information."""
    return RecipientInfo(
        role="buyer",
        company_name="Test Company",
        street="Via Verdi 45",
        city="Roma"
    )


@pytest.fixture
def sample_property():
    """Sample property information."""
    return PropertyInfo(
        city_or_location="Milano",
        street="Corso Buenos Aires",
        street_number="100"
    )


@pytest.fixture
def sample_signatory():
    """Sample signatory information."""
    return SignatoryInfo(
        name="Mario Rossi",
        role="Legal Representative"
    )


class TestDocumentBuilder:
    """Test cases for DocumentBuilder class."""
    
    def test_init_creates_output_dir(self, tmp_path):
        """Test that initialization creates output directory."""
        output_dir = tmp_path / "output"
        builder = DocumentBuilder(str(output_dir))
        
        assert output_dir.exists()
        assert builder.output_dir == output_dir
    
    def test_create_credit_note_with_model(
        self, 
        tmp_path, 
        sample_agency, 
        sample_recipient
    ):
        """Test credit note generation with Pydantic model."""
        builder = DocumentBuilder(str(tmp_path))
        
        credit_note_data = CreditNoteData(
            document_date=date(2026, 2, 10),
            document_number="CN-2026-001",
            agency=sample_agency,
            recipient=sample_recipient,
            amount=Decimal("1500.50"),
            description="Test credit note",
            reference_document="INV-001"
        )
        
        output_path = builder.create_credit_note(credit_note_data, "test_credit_note.pdf")
        
        assert output_path.exists()
        assert output_path.name == "test_credit_note.pdf"
        assert output_path.suffix == ".pdf"
        assert output_path.stat().st_size > 0
    
    def test_create_credit_note_with_dict(self, tmp_path, sample_agency):
        """Test credit note generation with dictionary."""
        builder = DocumentBuilder(str(tmp_path))
        
        data = {
            "document_date": "2026-02-10",
            "document_number": "CN-2026-002",
            "agency": sample_agency.model_dump(),
            "recipient": {
                "role": "seller",
                "company_name": "ABC Corp",
                "street": "Via Test 1",
                "city": "Torino"
            },
            "amount": 2500.00,
            "description": "Test description"
        }
        
        output_path = builder.create_credit_note(data, "test_dict.pdf")
        
        assert output_path.exists()
        assert output_path.suffix == ".pdf"
    
    def test_create_commission_acknowledgement_with_model(
        self,
        tmp_path,
        sample_agency,
        sample_recipient,
        sample_property,
        sample_signatory
    ):
        """Test commission acknowledgement generation with Pydantic model."""
        builder = DocumentBuilder(str(tmp_path))
        
        commission_data = CommissionAcknowledgementData(
            document_date=date(2026, 2, 10),
            agency=sample_agency,
            recipients=[sample_recipient],
            property=sample_property,
            signatories=[sample_signatory],
            deal_type="sale",
            commission_amount=Decimal("5000.00"),
            commission_due_on="notary deed"
        )
        
        output_path = builder.create_commission_acknowledgement(
            commission_data,
            "test_commission.pdf"
        )
        
        assert output_path.exists()
        assert output_path.name == "test_commission.pdf"
        assert output_path.suffix == ".pdf"
        assert output_path.stat().st_size > 0
    
    def test_create_commission_with_multiple_recipients(
        self,
        tmp_path,
        sample_agency,
        sample_property,
        sample_signatory
    ):
        """Test commission acknowledgement with multiple recipients."""
        builder = DocumentBuilder(str(tmp_path))
        
        recipients = [
            RecipientInfo(
                role="seller",
                company_name="Seller Corp",
                street="Via Seller 1",
                city="Milano"
            ),
            RecipientInfo(
                role="buyer",
                company_name="Buyer Corp",
                street="Via Buyer 2",
                city="Roma"
            )
        ]
        
        commission_data = CommissionAcknowledgementData(
            document_date=date(2026, 2, 10),
            agency=sample_agency,
            recipients=recipients,
            property=sample_property,
            signatories=[sample_signatory],
            deal_type="sale",
            commission_amount=Decimal("7500.00"),
            commission_due_on="notary deed"
        )
        
        output_path = builder.create_commission_acknowledgement(
            commission_data,
            "test_multiple_recipients.pdf"
        )
        
        assert output_path.exists()
    
    def test_validation_error_on_invalid_data(self, tmp_path):
        """Test that validation errors are raised for invalid data."""
        builder = DocumentBuilder(str(tmp_path))
        
        invalid_data = {
            "document_date": "2026-02-10",
            "document_number": "CN-001",
            "amount": -100  # Invalid: negative amount
        }
        
        with pytest.raises(Exception):  # Pydantic will raise validation error
            builder.create_credit_note(invalid_data)
