#!/usr/bin/env python
"""
Example script demonstrating how to use commpay programmatically with the new data models.
"""

from datetime import date
from decimal import Decimal
from commpay.builder import DocumentBuilder
from commpay.models import (
    CommissionAcknowledgementData,
    CreditNoteData,
    AgencyInfo,
    RecipientInfo,
    PropertyInfo,
    SignatoryInfo,
)


def main():
    # Initialize the document builder
    builder = DocumentBuilder(output_dir="output")
    
    # Sample agency information
    agency = AgencyInfo(
        name="Premium Real Estate Agency",
        street="Via Roma",
        street_number="123",
        city="Milano",
        iban="IT60X0542811101000000123456",
        bank="Intesa Sanpaolo",
        bank_account_beneficiary="Premium Real Estate S.r.l."
    )
    
    # Example 1: Create a credit note
    print("Creating credit note...")
    credit_note_data = CreditNoteData(
        document_date=date(2026, 2, 10),
        document_number="CN-2026-001",
        agency=agency,
        recipient=RecipientInfo(
            role="Buyer",
            is_company=True,
            company_name="ABC Properties Ltd",
            codice_fiscale="12345678901",
            street="Via Verdi 45",
            city="Roma"
        ),
        amount=Decimal("1500.00"),
        description="Credit note for property transaction cancellation",
        reference_document="INV-2026-050"
    )
    
    credit_note_path = builder.create_credit_note(
        credit_note_data,
        "example_credit_note.pdf"
    )
    print(f"✓ Credit note created: {credit_note_path}")
    
    # Example 2: Create a commission acknowledgement
    print("\nCreating commission acknowledgement...")
    commission_data = CommissionAcknowledgementData(
        document_date=date(2026, 2, 10),
        agency=agency,
        recipients=[
            RecipientInfo(
                role="Seller",
                is_company=True,
                company_name="Seller Properties S.r.l.",
                codice_fiscale="98765432101",
                street="Corso Buenos Aires 100",
                city="Milano"
            ),
            RecipientInfo(
                role="Buyer",
                is_company=False,
                first_name="Marco",
                last_name="Bianchi",
                codice_fiscale="BNCMRC75D15F205X",
                street="Via Dante 50",
                city="Roma"
            )
        ],
        property=PropertyInfo(
            city_or_location="Milano Centro",
            street="Via Montenapoleone",
            street_number="15",
            notes="Residential unit, 2nd floor, entrance A"
        ),
        signatories=[
            SignatoryInfo(
                name="Mario Rossi",
                role="Legal Representative"
            ),
            SignatoryInfo(
                name="Laura Bianchi",
                role="Agency Director"
            )
        ],
        deal_type="sale",
        commission_amount=Decimal("8500.00"),
        commission_due_on="notary deed"
    )
    
    commission_path = builder.create_commission_acknowledgement(
        commission_data,
        "example_commission.pdf"
    )
    print(f"✓ Commission acknowledgement created: {commission_path}")
    
    # Example 3: Using dictionaries (alternative approach)
    print("\nCreating document from dictionary...")
    dict_data = {
        "document_date": "2026-02-10",
        "document_number": "CN-2026-002",
        "agency": {
            "name": "Test Agency",
            "street": "Test Street",
            "street_number": "1",
            "city": "Test City",
            "iban": "IT60X0542811101000000123456",
            "bank": "Test Bank",
            "bank_account_beneficiary": "Test Agency S.r.l.",
        },
        "recipient": {
            "role": "Seller",
            "is_company": True,
            "company_name": "Test Company",
            "codice_fiscale": "11223344556",
            "street": "Test Address",
            "city": "Test City"
        },
        "amount": 500.00,
        "description": "Test credit note"
    }
    
    dict_path = builder.create_credit_note(dict_data, "example_from_dict.pdf")
    print(f"✓ Document from dictionary created: {dict_path}")
    
    print("\n✓ All documents generated successfully!")
    print(f"  Check the 'output' directory for generated PDFs")


if __name__ == "__main__":
    main()
