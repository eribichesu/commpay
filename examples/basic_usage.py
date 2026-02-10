#!/usr/bin/env python
"""
Example script demonstrating how to use commpay programmatically with the new data models.
"""

from datetime import date
from decimal import Decimal
from commpay.builder import DocumentBuilder
from commpay.models import (
    CommissionAcknowledgementData,
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
    
    # Create a commission acknowledgement
    print("Creating commission acknowledgement...")
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
    
    print("\n✓ Document generated successfully!")
    print(f"  Check the 'output' directory for generated PDF")


if __name__ == "__main__":
    main()
