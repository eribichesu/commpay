"""
Command Line Interface Module

Interactive console for document generation.
"""

import sys
from datetime import date, datetime
from decimal import Decimal
from commpay.builder import DocumentBuilder
from commpay.models import (
    CommissionAcknowledgementData,
    AgencyInfo,
    RecipientInfo,
    PropertyInfo,
    SignatoryInfo,
)


def print_banner():
    """Print application banner."""
    print("=" * 60)
    print("  COMMPAY - Commercial Document Builder")
    print("  Version 0.1.0")
    print("=" * 60)
    print()


def print_menu():
    """Print main menu options."""
    print("\nMain Menu:")
    print("1. Create Commission Acknowledgement")
    print("2. Exit")
    print()


def get_commission_data() -> CommissionAcknowledgementData:
    """
    Collect commission acknowledgement data from user input.
    
    Returns:
        CommissionAcknowledgementData model
    """
    print("\n--- Enter Commission Acknowledgement Details ---\n")
    
    # Agency information
    print("Agency Information:")
    agency = AgencyInfo(
        name=input("  Agency name: ").strip(),
        street=input("  Street: ").strip(),
        street_number=input("  Street number: ").strip(),
        city=input("  City: ").strip(),
        iban=input("  IBAN: ").strip(),
        bank=input("  Bank name: ").strip(),
        bank_account_beneficiary=input("  Account beneficiary: ").strip(),
    )
    
    # Recipients
    print("\nRecipient Information:")
    recipients = []
    while True:
        print(f"\n  Recipient #{len(recipients) + 1}:")
        role = input("    Role (seller/buyer/landlord/tenant): ").strip().lower()
        if role not in ["seller", "buyer", "landlord", "tenant"]:
            print("    Invalid role. Using 'buyer' as default.")
            role = "buyer"
        
        company_name = input("    Company name (optional, press Enter to skip): ").strip()
        recipients.append(RecipientInfo(
            role=role,
            company_name=company_name if company_name else None,
            street=input("    Street address: ").strip(),
            city=input("    City: ").strip(),
        ))
        
        add_more = input("\n  Add another recipient? (y/n): ").strip().lower()
        if add_more != 'y':
            break
    
    # Property information
    print("\nProperty Information:")
    property_info = PropertyInfo(
        city_or_location=input("  City/Location: ").strip(),
        street=input("  Street: ").strip(),
        street_number=input("  Street number: ").strip(),
    )
    
    # Deal information
    print("\nDeal Information:")
    deal_type = input("  Deal type (sale/lease): ").strip().lower()
    if deal_type not in ["sale", "lease"]:
        print("  Invalid deal type. Using 'sale' as default.")
        deal_type = "sale"
    
    commission_amount_str = input("  Commission amount: ").strip()
    try:
        commission_amount = Decimal(commission_amount_str)
    except:
        print("  Invalid amount. Using 0.00 as default.")
        commission_amount = Decimal("0.00")
    
    commission_due_on = input("  Commission due on (e.g., 'notary deed'): ").strip()
    
    # Signatories
    print("\nSignatory Information:")
    signatories = []
    while True:
        print(f"\n  Signatory #{len(signatories) + 1}:")
        signatories.append(SignatoryInfo(
            name=input("    Name: ").strip(),
            role=input("    Role: ").strip(),
        ))
        
        add_more = input("\n  Add another signatory? (y/n): ").strip().lower()
        if add_more != 'y':
            break
    
    # Document date
    date_str = input("\nDocument date (YYYY-MM-DD, press Enter for today): ").strip()
    if date_str:
        try:
            document_date = date.fromisoformat(date_str)
        except:
            print("Invalid date format. Using today's date.")
            document_date = date.today()
    else:
        document_date = date.today()
    
    return CommissionAcknowledgementData(
        document_date=document_date,
        agency=agency,
        recipients=recipients,
        property=property_info,
        signatories=signatories,
        deal_type=deal_type,
        commission_amount=commission_amount,
        commission_due_on=commission_due_on,
    )


def main():
    """Main CLI loop."""
    print_banner()
    
    builder = DocumentBuilder()
    
    while True:
        print_menu()
        choice = input("Select an option (1-2): ").strip()
        
        if choice == "1":
            try:
                data = get_commission_data()
                output_path = builder.create_commission_acknowledgement(data)
                print(f"\n✓ Commission acknowledgement generated successfully!")
                print(f"  Location: {output_path}")
            except KeyboardInterrupt:
                print("\n\n✗ Operation cancelled by user.")
            except Exception as e:
                print(f"\n✗ Error generating commission acknowledgement: {e}")
        
        elif choice == "2":
            print("\nThank you for using Commpay!")
            sys.exit(0)
        
        else:
            print("\n✗ Invalid option. Please select 1 or 2.")


if __name__ == "__main__":
    main()
