#!/usr/bin/env python
"""
Example script demonstrating how to use commpay programmatically
"""

from commpay.builder import DocumentBuilder

def main():
    # Initialize the document builder
    builder = DocumentBuilder(output_dir="output")
    
    # Example 1: Create a credit note
    print("Creating credit note...")
    credit_note_data = {
        "client_name": "Example Real Estate Agency",
        "client_address": "123 Main Street, City, 12345",
        "document_number": "CN-2026-001",
        "amount": 1500.00,
        "description": "Credit note for property transaction XYZ",
        "date": "10/02/2026"
    }
    
    credit_note_path = builder.create_credit_note(
        credit_note_data,
        "example_credit_note.pdf"
    )
    print(f"✓ Credit note created: {credit_note_path}")
    
    # Example 2: Create a commission acknowledgement
    print("\nCreating commission acknowledgement...")
    commission_data = {
        "agent_name": "John Doe",
        "agency_name": "Premium Properties Ltd",
        "commission_amount": 5000.00,
        "property_address": "456 Oak Avenue, City, 12345",
        "transaction_date": "05/02/2026",
        "document_number": "CA-2026-001"
    }
    
    commission_path = builder.create_commission_acknowledgement(
        commission_data,
        "example_commission.pdf"
    )
    print(f"✓ Commission acknowledgement created: {commission_path}")
    
    print("\n✓ All documents generated successfully!")
    print(f"  Check the 'output' directory for generated PDFs")

if __name__ == "__main__":
    main()
