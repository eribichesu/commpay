"""
Document Builder Module

Core functionality for building PDF commercial documents.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


class DocumentBuilder:
    """
    Main class for building PDF commercial documents.
    
    Supports generation of:
    - Credit notes
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
    
    def create_credit_note(
        self,
        data: Dict[str, Any],
        output_filename: Optional[str] = None
    ) -> Path:
        """
        Generate a credit note PDF document.
        
        Args:
            data: Dictionary containing document data
            output_filename: Optional custom filename for the output PDF
            
        Returns:
            Path to the generated PDF file
        """
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"credit_note_{timestamp}.pdf"
        
        output_path = self.output_dir / output_filename
        
        # Create PDF
        c = canvas.Canvas(str(output_path), pagesize=A4)
        
        # Add basic content (placeholder for template integration)
        self._add_header(c, "CREDIT NOTE")
        self._add_document_data(c, data)
        
        c.save()
        return output_path
    
    def create_commission_acknowledgement(
        self,
        data: Dict[str, Any],
        output_filename: Optional[str] = None
    ) -> Path:
        """
        Generate a commission acknowledgement PDF document.
        
        Args:
            data: Dictionary containing document data
            output_filename: Optional custom filename for the output PDF
            
        Returns:
            Path to the generated PDF file
        """
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"commission_ack_{timestamp}.pdf"
        
        output_path = self.output_dir / output_filename
        
        # Create PDF
        c = canvas.Canvas(str(output_path), pagesize=A4)
        
        # Add basic content (placeholder for template integration)
        self._add_header(c, "COMMISSION ACKNOWLEDGEMENT")
        self._add_document_data(c, data)
        
        c.save()
        return output_path
    
    def _add_header(self, c: canvas.Canvas, title: str) -> None:
        """
        Add header section to the document.
        
        Args:
            c: ReportLab canvas object
            title: Document title
        """
        width, height = A4
        
        # Title
        c.setFont("Helvetica-Bold", 20)
        c.drawString(30*mm, height - 30*mm, title)
        
        # Date
        c.setFont("Helvetica", 10)
        date_str = datetime.now().strftime("%d/%m/%Y")
        c.drawString(30*mm, height - 40*mm, f"Date: {date_str}")
    
    def _add_document_data(self, c: canvas.Canvas, data: Dict[str, Any]) -> None:
        """
        Add document data to the PDF.
        
        Args:
            c: ReportLab canvas object
            data: Document data dictionary
        """
        width, height = A4
        y_position = height - 60*mm
        
        c.setFont("Helvetica", 10)
        
        for key, value in data.items():
            text = f"{key}: {value}"
            c.drawString(30*mm, y_position, text)
            y_position -= 6*mm
