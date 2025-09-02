"""
PDF processing utilities
"""

import os
import logging
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class PDFSplitResult:
    """Result of PDF splitting operation"""
    success: bool
    output_files: List[str]
    error_message: Optional[str] = None


class PDFProcessor:
    """PDF processing utilities"""
    
    def __init__(self):
        """Initialize PDF processor"""
        self.pymupdf_available = self._check_pymupdf()
    
    def _check_pymupdf(self) -> bool:
        """Check if PyMuPDF is available"""
        try:
            import fitz
            return True
        except ImportError:
            logging.warning("PyMuPDF not available - PDF processing limited")
            return False
    
    def split_pdf_by_pages(self, pdf_path: str, output_dir: str, prefix: str = "page") -> PDFSplitResult:
        """
        Split PDF into individual pages
        
        Args:
            pdf_path: Path to input PDF
            output_dir: Directory for output files
            prefix: Prefix for output filenames
            
        Returns:
            PDFSplitResult with operation details
        """
        if not self.pymupdf_available:
            return PDFSplitResult(
                success=False,
                output_files=[],
                error_message="PyMuPDF not available"
            )
        
        try:
            import fitz
            
            doc = fitz.open(pdf_path)
            output_files = []
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            
            for page_num in range(doc.page_count):
                # Create new document with single page
                new_doc = fitz.open()
                new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                
                # Generate output filename
                output_filename = f"{base_name}_{prefix}_{page_num + 1:03d}.pdf"
                output_path = os.path.join(output_dir, output_filename)
                
                # Ensure unique filename
                output_path = self._get_unique_filename(output_path)
                
                # Save page
                new_doc.save(output_path)
                new_doc.close()
                
                output_files.append(output_path)
                logging.info(f"Created page {page_num + 1}: {os.path.basename(output_path)}")
            
            doc.close()
            
            return PDFSplitResult(
                success=True,
                output_files=output_files
            )
            
        except Exception as e:
            error_msg = f"PDF splitting failed: {str(e)}"
            logging.error(error_msg)
            return PDFSplitResult(
                success=False,
                output_files=[],
                error_message=error_msg
            )
    
    def merge_pdfs(self, pdf_paths: List[str], output_path: str) -> bool:
        """
        Merge multiple PDFs into single file
        
        Args:
            pdf_paths: List of PDF file paths to merge
            output_path: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        if not self.pymupdf_available:
            logging.error("PyMuPDF not available")
            return False
        
        try:
            import fitz
            
            # Create new document
            merged_doc = fitz.open()
            
            for pdf_path in pdf_paths:
                if os.path.exists(pdf_path):
                    doc = fitz.open(pdf_path)
                    merged_doc.insert_pdf(doc)
                    doc.close()
                else:
                    logging.warning(f"File not found: {pdf_path}")
            
            # Save merged document
            merged_doc.save(output_path)
            merged_doc.close()
            
            logging.info(f"Merged {len(pdf_paths)} PDFs into {output_path}")
            return True
            
        except Exception as e:
            logging.error(f"PDF merging failed: {str(e)}")
            return False
    
    def get_pdf_info(self, pdf_path: str) -> dict:
        """
        Get basic information about PDF file
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with PDF information
        """
        if not self.pymupdf_available:
            return {"error": "PyMuPDF not available"}
        
        try:
            import fitz
            
            doc = fitz.open(pdf_path)
            
            info = {
                "page_count": doc.page_count,
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
                "subject": doc.metadata.get("subject", ""),
                "creator": doc.metadata.get("creator", ""),
                "producer": doc.metadata.get("producer", ""),
                "creation_date": doc.metadata.get("creationDate", ""),
                "modification_date": doc.metadata.get("modDate", ""),
                "encrypted": doc.needs_pass,
                "file_size": os.path.getsize(pdf_path)
            }
            
            doc.close()
            return info
            
        except Exception as e:
            return {"error": str(e)}
    
    def extract_images_from_pdf(self, pdf_path: str, output_dir: str) -> List[str]:
        """
        Extract images from PDF file
        
        Args:
            pdf_path: Path to PDF file
            output_dir: Directory for extracted images
            
        Returns:
            List of extracted image file paths
        """
        if not self.pymupdf_available:
            return []
        
        try:
            import fitz
            
            doc = fitz.open(pdf_path)
            image_files = []
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    
                    if pix.n < 5:  # Skip CMYK images
                        if pix.n != 1:
                            pix = fitz.Pixmap(fitz.csRGB, pix)
                        
                        # Generate output filename
                        img_filename = f"{base_name}_page{page_num + 1}_img{img_index + 1}.png"
                        img_path = os.path.join(output_dir, img_filename)
                        
                        pix.save(img_path)
                        image_files.append(img_path)
                    
                    pix = None
            
            doc.close()
            return image_files
            
        except Exception as e:
            logging.error(f"Image extraction failed: {str(e)}")
            return []
    
    def _get_unique_filename(self, filepath: str) -> str:
        """Generate unique filename if file exists"""
        if not os.path.exists(filepath):
            return filepath
        
        base, ext = os.path.splitext(filepath)
        counter = 1
        
        while True:
            new_path = f"{base}_{counter:03d}{ext}"
            if not os.path.exists(new_path):
                return new_path
            counter += 1
    
    def is_pdf_valid(self, pdf_path: str) -> bool:
        """Check if PDF file is valid and readable"""
        if not self.pymupdf_available:
            return False
        
        try:
            import fitz
            doc = fitz.open(pdf_path)
            page_count = doc.page_count
            doc.close()
            return page_count > 0
        except Exception:
            return False