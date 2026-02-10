"""
Tests for DocumentBuilder
"""

import pytest
from pathlib import Path
from commpay.builder import DocumentBuilder


class TestDocumentBuilder:
    """Test cases for DocumentBuilder class."""
    
    def test_init_creates_output_dir(self, tmp_path):
        """Test that initialization creates output directory."""
        output_dir = tmp_path / "output"
        builder = DocumentBuilder(str(output_dir))
        
        assert output_dir.exists()
        assert builder.output_dir == output_dir
    
    def test_create_credit_note(self, tmp_path):
        """Test credit note generation."""
        builder = DocumentBuilder(str(tmp_path))
        
        data = {
            "client_name": "Test Client",
            "amount": 100.50,
            "document_number": "CN-001"
        }
        
        output_path = builder.create_credit_note(data, "test_credit_note.pdf")
        
        assert output_path.exists()
        assert output_path.name == "test_credit_note.pdf"
        assert output_path.suffix == ".pdf"
    
    def test_create_commission_acknowledgement(self, tmp_path):
        """Test commission acknowledgement generation."""
        builder = DocumentBuilder(str(tmp_path))
        
        data = {
            "client_name": "Test Agent",
            "amount": 250.00,
            "document_number": "CA-001"
        }
        
        output_path = builder.create_commission_acknowledgement(
            data, 
            "test_commission.pdf"
        )
        
        assert output_path.exists()
        assert output_path.name == "test_commission.pdf"
        assert output_path.suffix == ".pdf"
