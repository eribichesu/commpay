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
from jinja2 import Environment, FileSystemLoader, select_autoescape

from commpay.models import CommissionAcknowledgementData


class DocumentBuilder:
    """
    Main class for building PDF commercial documents.
    
    Supports generation of:
    - Commission acknowledgements
    """
    
    def __init__(self, output_dir: str = "output", templates_dir: Optional[str] = None):
        """
        Initialize the DocumentBuilder.
        
        Args:
            output_dir: Directory where generated PDFs will be saved
            templates_dir: Directory containing Jinja2 templates (defaults to package templates)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Set up Jinja2 environment
        if templates_dir is None:
            # Use package templates directory
            templates_dir = Path(__file__).parent.parent.parent / "templates"
        
        self.templates_dir = Path(templates_dir)
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def render_template(
        self,
        template_name: str,
        data: Union[CommissionAcknowledgementData, Dict[str, Any]]
    ) -> str:
        """
        Render a Jinja2 template with the provided data.
        
        Args:
            template_name: Name of the template file in templates directory
            data: CommissionAcknowledgementData model or dictionary
            
        Returns:
            Rendered template as string
        """
        # Validate and convert data
        if isinstance(data, dict):
            data = CommissionAcknowledgementData(**data)
        
        # Load template
        template = self.jinja_env.get_template(template_name)
        
        # Prepare context - convert Pydantic model to dict for Jinja2
        context = {
            'document_date': data.document_date,
            'agency': data.agency.model_dump(),
            'recipients': [r.model_dump() for r in data.recipients],
            'property': data.property.model_dump(),
            'signatories': [s.model_dump() for s in data.signatories],
            'deal_type': data.deal_type,
            'commission_amount': float(data.commission_amount),
            'commission_due_on': data.commission_due_on
        }
        
        # Render template
        return template.render(**context)
    
    def create_commission_acknowledgement_from_template(
        self,
        data: Union[CommissionAcknowledgementData, Dict[str, Any]],
        template_name: str = "commission_acknowledgement.j2",
        output_filename: Optional[str] = None
    ) -> Path:
        """
        Generate a commission acknowledgement PDF using a Jinja2 template.
        
        Args:
            data: CommissionAcknowledgementData model or dictionary
            template_name: Name of the Jinja2 template file
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
        
        # Render template
        rendered_text = self.render_template(template_name, data)
        
        # Create PDF from rendered text
        c = canvas.Canvas(str(output_path), pagesize=A4)
        self._add_text_content(c, rendered_text)
        c.save()
        
        return output_path
    
    def _add_text_content(self, c: canvas.Canvas, text: str) -> None:
        """
        Add plain text content to PDF with proper formatting and print margins.
        
        Args:
            c: ReportLab canvas object
            text: Text content to add
        """
        width, height = A4
        
        # Professional printing margins: 25mm top/bottom, 20mm left, 15mm right
        left_margin = 20*mm
        right_margin = 15*mm
        top_margin = 25*mm
        bottom_margin = 25*mm
        
        y_pos = height - top_margin
        line_height = 4.5*mm
        max_width = width - left_margin - right_margin
        
        c.setFont("Helvetica", 10)
        
        for line in text.split('\n'):
            # Check if we need a new page
            if y_pos < bottom_margin:
                c.showPage()
                c.setFont("Helvetica", 10)
                y_pos = height - top_margin
            
            # Handle empty lines
            if not line.strip():
                y_pos -= line_height * 0.7
                continue
            
            # Wrap long lines to fit within margins
            wrapped_lines = self._wrap_text_to_width(line, max_width, c)
            
            for wrapped_line in wrapped_lines:
                # Check page break for wrapped lines too
                if y_pos < bottom_margin:
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    y_pos = height - top_margin
                
                # Apply formatting based on content
                if wrapped_line.startswith('Oggetto:'):
                    c.setFont("Helvetica-Bold", 11)
                    c.drawString(left_margin, y_pos, wrapped_line)
                    c.setFont("Helvetica", 10)
                    y_pos -= line_height * 1.2  # Extra space after subject
                elif wrapped_line.startswith('In fede'):
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(left_margin, y_pos, wrapped_line)
                    c.setFont("Helvetica", 10)
                    y_pos -= line_height
                elif wrapped_line.startswith('Spett.le'):
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(left_margin, y_pos, wrapped_line)
                    c.setFont("Helvetica", 10)
                    y_pos -= line_height
                elif wrapped_line.startswith('Coordinate bancarie'):
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(left_margin, y_pos, wrapped_line)
                    c.setFont("Helvetica", 10)
                    y_pos -= line_height
                elif wrapped_line.strip().startswith(('1)', '2)', '3)')):
                    # Numbered points - slightly indented
                    c.drawString(left_margin + 5*mm, y_pos, wrapped_line)
                    y_pos -= line_height * 1.1
                elif wrapped_line.startswith('_________________________'):
                    # Signature line
                    c.drawString(left_margin, y_pos, wrapped_line)
                    y_pos -= line_height * 0.8
                else:
                    c.drawString(left_margin, y_pos, wrapped_line)
                    y_pos -= line_height
    
    def _wrap_text_to_width(self, text: str, max_width: float, c: canvas.Canvas) -> list:
        """
        Wrap text to fit within specified width.
        
        Args:
            text: Text to wrap
            max_width: Maximum width in points
            c: Canvas object to measure text width
            
        Returns:
            List of wrapped lines
        """
        if not text.strip():
            return [text]
        
        # Check if text fits
        if c.stringWidth(text, "Helvetica", 10) <= max_width:
            return [text]
        
        # Need to wrap - split by words
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if c.stringWidth(test_line, "Helvetica", 10) <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines if lines else [text]

    
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
