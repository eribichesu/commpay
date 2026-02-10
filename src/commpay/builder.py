"""
Document Builder Module

Core functionality for building PDF commercial documents.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional, Union, Dict, Any
from decimal import Decimal
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

from commpay.models import CommissionAcknowledgementData


class DocumentBuilder:
    """
    Main class for building PDF commercial documents.
    
    Supports generation of:
    - Commission acknowledgements
    """
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the DocumentBuilder.
        
        Args:
            output_dir: Directory where generated PDFs will be saved
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def create_commission_acknowledgement(
        self,
        data: Union[CommissionAcknowledgementData, Dict[str, Any]],
        output_filename: Optional[str] = None
    ) -> Path:
        """
        Generate a commission acknowledgement PDF document.
        
        Args:
            data: CommissionAcknowledgementData model or dictionary containing document data
            output_filename: Optional custom filename for the output PDF
            
        Returns:
            Path to the generated PDF file
        """
        # Validate and convert data
        if isinstance(data, dict):
            data = CommissionAcknowledgementData(**data)
        
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"commission_ack_{timestamp}.pdf"
        
        output_path = self.output_dir / output_filename
        
        # Create PDF
        c = canvas.Canvas(str(output_path), pagesize=A4)
        
        # Add document content
        self._add_commission_acknowledgement_content(c, data)
        
        c.save()
        return output_path
    
    def _add_commission_acknowledgement_content(
        self, 
        c: canvas.Canvas, 
        data: CommissionAcknowledgementData
    ) -> None:
        """
        Add commission acknowledgement content to the PDF.
        
        Args:
            c: ReportLab canvas object
            data: CommissionAcknowledgementData model
        """
        width, height = A4
        y_pos = height - 20*mm
        
        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(30*mm, y_pos, "COMMISSION ACKNOWLEDGEMENT")
        y_pos -= 10*mm
        
        # Date
        c.setFont("Helvetica", 10)
        c.drawRightString(width - 30*mm, y_pos, f"Date: {data.document_date.strftime('%d/%m/%Y')}")
        y_pos -= 15*mm
        
        # Agency info
        c.setFont("Helvetica-Bold", 11)
        c.drawString(30*mm, y_pos, "Agency:")
        y_pos -= 5*mm
        c.setFont("Helvetica", 10)
        c.drawString(30*mm, y_pos, data.agency.name)
        y_pos -= 4*mm
        c.drawString(30*mm, y_pos, f"{data.agency.street} {data.agency.street_number}, {data.agency.city}")
        y_pos -= 10*mm
        
        # Recipients
        c.setFont("Helvetica-Bold", 11)
        recipient_label = "Recipients:" if len(data.recipients) > 1 else "Recipient:"
        c.drawString(30*mm, y_pos, recipient_label)
        y_pos -= 5*mm
        c.setFont("Helvetica", 10)
        
        for recipient in data.recipients:
            if recipient.is_company:
                c.drawString(30*mm, y_pos, f"• {recipient.company_name}")
                y_pos -= 4*mm
            else:
                c.drawString(30*mm, y_pos, f"• {recipient.first_name} {recipient.last_name}")
                y_pos -= 4*mm
            c.drawString(35*mm, y_pos, f"Role: {recipient.role}")
            y_pos -= 4*mm
            c.drawString(35*mm, y_pos, f"CF: {recipient.codice_fiscale}")
            y_pos -= 4*mm
            c.drawString(35*mm, y_pos, f"Address: {recipient.street}, {recipient.city}")
            y_pos -= 5*mm
        y_pos -= 5*mm
        
        # Property information
        c.setFont("Helvetica-Bold", 11)
        c.drawString(30*mm, y_pos, "Property:")
        y_pos -= 5*mm
        c.setFont("Helvetica", 10)
        c.drawString(30*mm, y_pos, f"{data.property.street} {data.property.street_number}")
        y_pos -= 4*mm
        c.drawString(30*mm, y_pos, data.property.city_or_location)
        y_pos -= 4*mm
        if data.property.notes:
            c.setFont("Helvetica-Oblique", 9)
            c.drawString(30*mm, y_pos, f"Notes: {data.property.notes}")
            y_pos -= 4*mm
            c.setFont("Helvetica", 10)
        y_pos -= 6*mm
        
        # Deal information
        c.setFont("Helvetica-Bold", 11)
        c.drawString(30*mm, y_pos, "Deal Information:")
        y_pos -= 5*mm
        c.setFont("Helvetica", 10)
        c.drawString(30*mm, y_pos, f"Type: {data.deal_type.title()}")
        y_pos -= 4*mm
        c.drawString(30*mm, y_pos, f"Commission Amount: EUR {data.commission_amount:.2f}")
        y_pos -= 4*mm
        c.drawString(30*mm, y_pos, f"Due on: {data.commission_due_on}")
        y_pos -= 15*mm
        
        # Signatories
        c.setFont("Helvetica-Bold", 11)
        c.drawString(30*mm, y_pos, "Signatories:")
        y_pos -= 5*mm
        c.setFont("Helvetica", 10)
        
        for signatory in data.signatories:
            c.drawString(30*mm, y_pos, f"• {signatory.name} - {signatory.role}")
            y_pos -= 4*mm
        y_pos -= 10*mm
        
        # Bank details
        c.setFont("Helvetica-Bold", 11)
        c.drawString(30*mm, y_pos, "Payment Details:")
        y_pos -= 5*mm
        c.setFont("Helvetica", 9)
        c.drawString(30*mm, y_pos, f"Beneficiary: {data.agency.bank_account_beneficiary}")
        y_pos -= 4*mm
        c.drawString(30*mm, y_pos, f"Bank: {data.agency.bank}")
        y_pos -= 4*mm
        c.drawString(30*mm, y_pos, f"IBAN: {data.agency.iban}")
    
    def _wrap_text(self, text: str, max_length: int = 80) -> list[str]:
        """
        Wrap text to fit within a maximum character length.
        
        Args:
            text: Text to wrap
            max_length: Maximum characters per line
            
        Returns:
            List of wrapped lines
        """
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_length:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines if lines else [text]
