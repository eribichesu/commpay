"""
Command Line Interface Module

Interactive console for document generation.
"""

import sys
from datetime import datetime
from commpay.builder import DocumentBuilder


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
    print("1. Create Credit Note")
    print("2. Create Commission Acknowledgement")
    print("3. Exit")
    print()


def get_document_data() -> dict:
    """
    Collect document data from user input.
    
    Returns:
        Dictionary containing document data
    """
    print("\nEnter document details:")
    data = {}
    
    data["client_name"] = input("Client name: ").strip()
    data["client_address"] = input("Client address: ").strip()
    data["document_number"] = input("Document number: ").strip()
    
    amount = input("Amount: ").strip()
    try:
        data["amount"] = float(amount)
    except ValueError:
        data["amount"] = 0.0
    
    data["description"] = input("Description: ").strip()
    
    return data


def main():
    """Main CLI loop."""
    print_banner()
    
    builder = DocumentBuilder()
    
    while True:
        print_menu()
        choice = input("Select an option (1-3): ").strip()
        
        if choice == "1":
            print("\n--- Create Credit Note ---")
            data = get_document_data()
            
            try:
                output_path = builder.create_credit_note(data)
                print(f"\n✓ Credit note generated successfully!")
                print(f"  Location: {output_path}")
            except Exception as e:
                print(f"\n✗ Error generating credit note: {e}")
        
        elif choice == "2":
            print("\n--- Create Commission Acknowledgement ---")
            data = get_document_data()
            
            try:
                output_path = builder.create_commission_acknowledgement(data)
                print(f"\n✓ Commission acknowledgement generated successfully!")
                print(f"  Location: {output_path}")
            except Exception as e:
                print(f"\n✗ Error generating commission acknowledgement: {e}")
        
        elif choice == "3":
            print("\nThank you for using Commpay!")
            sys.exit(0)
        
        else:
            print("\n✗ Invalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
