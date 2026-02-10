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
        role="Buyer",
        is_company=True,
        company_name="Test Company",
        codice_fiscale="12345678901",
        street="Via Verdi 45",
        city="Roma"
    )


@pytest.fixture
def sample_property():
    """Sample property information."""
    return PropertyInfo(
        city_or_location="Milano",
        street="Corso Buenos Aires",
        street_number="100",
        notes="Apartment on 3rd floor"
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
                role="Seller",
                is_company=True,
                company_name="Seller Corp",
                codice_fiscale="12345678901",
                street="Via Seller 1",
                city="Milano"
            ),
            RecipientInfo(
                role="Buyer",
                is_company=False,
                first_name="Giovanni",
                last_name="Verdi",
                codice_fiscale="VRDGNN85M01F205Z",
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
    
    def test_validation_error_on_invalid_data(
        self, 
        tmp_path,
        sample_agency
    ):
        """Test that validation errors are raised for invalid data."""
        builder = DocumentBuilder(str(tmp_path))
        
        invalid_data = {
            "document_date": "2026-02-10",
            "agency": sample_agency.model_dump(),
            "recipients": [],  # Invalid: empty recipients list
            "property": {
                "city_or_location": "Milano",
                "street": "Via Test",
                "street_number": "1"
            },
            "signatories": [{
                "name": "Test",
                "role": "Test"
            }],
            "deal_type": "sale",
            "commission_amount": -100,  # Invalid: negative amount
            "commission_due_on": "deed"
        }
        
        with pytest.raises(Exception):  # Pydantic will raise validation error
            builder.create_commission_acknowledgement(invalid_data)
    
    def test_render_template(
        self,
        tmp_path,
        sample_agency,
        sample_recipient,
        sample_property,
        sample_signatory
    ):
        """Test Jinja2 template rendering."""
        builder = DocumentBuilder(str(tmp_path))
        
        commission_data = CommissionAcknowledgementData(
            document_date=date(2026, 2, 10),
            agency=sample_agency,
            recipients=[sample_recipient],
            property=sample_property,
            signatories=[sample_signatory],
            deal_type="sale",
            commission_amount=Decimal("5000.00"),
            commission_due_on="notary deed",
            payment_reference="Commission payment - Property Milano"
        )
        
        rendered = builder.render_template("commission_acknowledgement.j2", commission_data)
        
        assert "Test Real Estate" in rendered
        assert "Test Company" in rendered
        assert "Milano" in rendered
        assert "5000.00" in rendered
        assert "Mario Rossi" in rendered
        assert "Causale: Commission payment - Property Milano" in rendered
    
    def test_create_commission_from_template(
        self,
        tmp_path,
        sample_agency,
        sample_recipient,
        sample_property,
        sample_signatory
    ):
        """Test PDF generation from Jinja2 template."""
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
        
        output_path = builder.create_commission_acknowledgement_from_template(
            commission_data,
            "commission_acknowledgement.j2",
            "test_template.pdf"
        )
        
        assert output_path.exists()
        assert output_path.name == "test_template.pdf"
        assert output_path.suffix == ".pdf"
        assert output_path.stat().st_size > 0
    
    def test_template_with_multiple_recipients(
        self,
        tmp_path,
        sample_agency,
        sample_property,
        sample_signatory
    ):
        """Test template rendering with multiple recipients."""
        builder = DocumentBuilder(str(tmp_path))
        
        recipients = [
            RecipientInfo(
                role="Seller",
                is_company=False,
                first_name="Mario",
                last_name="Rossi",
                codice_fiscale="RSSMRA80A01H501X",
                street="Via Seller 1",
                city="Milano"
            ),
            RecipientInfo(
                role="Buyer",
                is_company=True,
                company_name="Buyer Corp",
                codice_fiscale="98765432101",
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
            deal_type="lease",
            commission_amount=Decimal("3500.00"),
            commission_due_on="contract signing"
        )
        
        rendered = builder.render_template("commission_acknowledgement.j2", commission_data)
        
        assert "Mario Rossi" in rendered
        assert "Buyer Corp" in rendered
        assert "RSSMRA80A01H501X" in rendered
        assert "98765432101" in rendered
        assert "locazione" in rendered

