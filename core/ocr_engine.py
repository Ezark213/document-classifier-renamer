"""
OCR Engine for text extraction from PDF documents
"""

import os
import tempfile
from typing import Optional
import logging


class OCREngine:
    """OCR engine for extracting text from PDF documents"""
    
    def __init__(self):
        """Initialize OCR engine"""
        self.tesseract_available = self._check_tesseract()
        
    def _check_tesseract(self) -> bool:
        """Check if Tesseract OCR is available"""
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            return True
        except Exception as e:
            logging.warning(f"Tesseract OCR not available: {e}")
            return False
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF using OCR
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        try:
            # First try to extract text directly from PDF
            text = self._extract_text_direct(pdf_path)
            
            # If direct extraction fails or returns minimal text, use OCR
            if not text or len(text.strip()) < 50:
                if self.tesseract_available:
                    text = self._extract_text_ocr(pdf_path)
                else:
                    logging.warning("OCR not available, using direct text extraction only")
            
            return text
            
        except Exception as e:
            logging.error(f"Text extraction failed for {pdf_path}: {e}")
            return ""
    
    def _extract_text_direct(self, pdf_path: str) -> str:
        """Extract text directly from PDF (non-OCR)"""
        try:
            import fitz  # PyMuPDF
            
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text += page.get_text()
            
            doc.close()
            return text
            
        except Exception as e:
            logging.error(f"Direct text extraction failed: {e}")
            return ""
    
    def _extract_text_ocr(self, pdf_path: str) -> str:
        """Extract text using OCR"""
        if not self.tesseract_available:
            return ""
        
        try:
            import fitz  # PyMuPDF
            import pytesseract
            from PIL import Image
            
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                
                # Convert page to image
                mat = fitz.Matrix(2.0, 2.0)  # Increase resolution for better OCR
                pix = page.get_pixmap(matrix=mat)
                
                # Convert to PIL Image
                img_data = pix.tobytes("ppm")
                img = Image.open(io.BytesIO(img_data))
                
                # Perform OCR
                page_text = pytesseract.image_to_string(img, lang='eng')
                text += page_text + "\n"
            
            doc.close()
            return text
            
        except Exception as e:
            logging.error(f"OCR extraction failed: {e}")
            return ""
    
    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extract text from image file using OCR
        
        Args:
            image_path: Path to image file
            
        Returns:
            Extracted text content
        """
        if not self.tesseract_available:
            logging.warning("OCR not available")
            return ""
        
        try:
            import pytesseract
            from PIL import Image
            
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img, lang='eng')
            return text
            
        except Exception as e:
            logging.error(f"Image OCR failed for {image_path}: {e}")
            return ""
    
    def is_ocr_available(self) -> bool:
        """Check if OCR functionality is available"""
        return self.tesseract_available
    
    def get_supported_languages(self) -> list:
        """Get list of supported OCR languages"""
        if not self.tesseract_available:
            return []
        
        try:
            import pytesseract
            langs = pytesseract.get_languages()
            return langs
        except Exception:
            return ['eng']  # Default to English