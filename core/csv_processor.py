"""
CSV file processing utilities
"""

import pandas as pd
import os
import logging
from typing import Optional, Dict, List
from dataclasses import dataclass


@dataclass
class CSVAnalysisResult:
    """Result of CSV file analysis"""
    success: bool
    row_count: int
    column_count: int
    columns: List[str]
    sample_data: Dict
    detected_type: str
    confidence: float
    error_message: Optional[str] = None


class CSVProcessor:
    """CSV file processing and analysis utilities"""
    
    def __init__(self):
        """Initialize CSV processor"""
        self.encoding_options = ['utf-8', 'utf-8-sig', 'iso-8859-1', 'cp1252']
    
    def analyze_csv(self, file_path: str) -> CSVAnalysisResult:
        """
        Analyze CSV file structure and content
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            CSVAnalysisResult with analysis details
        """
        try:
            # Try different encodings
            df = None
            used_encoding = 'utf-8'
            
            for encoding in self.encoding_options:
                try:
                    df = pd.read_csv(file_path, encoding=encoding, nrows=1000)  # Limit rows for analysis
                    used_encoding = encoding
                    break
                except UnicodeDecodeError:
                    continue
                except Exception:
                    continue
            
            if df is None:
                return CSVAnalysisResult(
                    success=False,
                    row_count=0,
                    column_count=0,
                    columns=[],
                    sample_data={},
                    detected_type="unknown",
                    confidence=0.0,
                    error_message="Could not read CSV file with any supported encoding"
                )
            
            # Basic analysis
            row_count = len(df)
            column_count = len(df.columns)
            columns = df.columns.tolist()
            
            # Sample data (first 3 rows)
            sample_data = {}
            for i, (idx, row) in enumerate(df.head(3).iterrows()):
                sample_data[f"row_{i + 1}"] = row.to_dict()
            
            # Detect CSV type based on columns and content
            detected_type, confidence = self._detect_csv_type(df, os.path.basename(file_path))
            
            logging.info(f"CSV analysis complete: {row_count} rows, {column_count} columns")
            
            return CSVAnalysisResult(
                success=True,
                row_count=row_count,
                column_count=column_count,
                columns=columns,
                sample_data=sample_data,
                detected_type=detected_type,
                confidence=confidence
            )
            
        except Exception as e:
            error_msg = f"CSV analysis failed: {str(e)}"
            logging.error(error_msg)
            
            return CSVAnalysisResult(
                success=False,
                row_count=0,
                column_count=0,
                columns=[],
                sample_data={},
                detected_type="unknown",
                confidence=0.0,
                error_message=error_msg
            )
    
    def _detect_csv_type(self, df: pd.DataFrame, filename: str) -> tuple[str, float]:
        """
        Detect the type of CSV file based on content and filename
        
        Args:
            df: DataFrame with CSV data
            filename: Original filename
            
        Returns:
            Tuple of (detected_type, confidence_score)
        """
        filename_lower = filename.lower()
        columns_str = ' '.join(df.columns.astype(str)).lower()
        
        # Financial data indicators
        financial_keywords = ['amount', 'price', 'cost', 'total', 'balance', 'payment', 'invoice', 'transaction']
        financial_score = sum(1 for keyword in financial_keywords if keyword in columns_str or keyword in filename_lower)
        
        # Customer/Contact data indicators
        contact_keywords = ['name', 'email', 'phone', 'address', 'customer', 'client', 'contact']
        contact_score = sum(1 for keyword in contact_keywords if keyword in columns_str or keyword in filename_lower)
        
        # Inventory data indicators
        inventory_keywords = ['product', 'item', 'sku', 'quantity', 'stock', 'inventory']
        inventory_score = sum(1 for keyword in inventory_keywords if keyword in columns_str or keyword in filename_lower)
        
        # Sales data indicators
        sales_keywords = ['sales', 'revenue', 'order', 'purchase', 'sold', 'profit']
        sales_score = sum(1 for keyword in sales_keywords if keyword in columns_str or keyword in filename_lower)
        
        # Employee data indicators
        employee_keywords = ['employee', 'staff', 'payroll', 'salary', 'department']
        employee_score = sum(1 for keyword in employee_keywords if keyword in columns_str or keyword in filename_lower)
        
        # Calculate scores
        scores = {
            'financial_data': financial_score / len(financial_keywords),
            'customer_data': contact_score / len(contact_keywords),
            'inventory_data': inventory_score / len(inventory_keywords),
            'sales_data': sales_score / len(sales_keywords),
            'employee_data': employee_score / len(employee_keywords)
        }
        
        # Find best match
        best_type = max(scores, key=scores.get)
        best_score = scores[best_type]
        
        # Minimum confidence threshold
        if best_score < 0.1:
            return "general_data", 0.1
        
        return best_type, min(best_score * 2, 1.0)  # Scale confidence
    
    def convert_csv_to_excel(self, csv_path: str, excel_path: str) -> bool:
        """
        Convert CSV file to Excel format
        
        Args:
            csv_path: Path to input CSV file
            excel_path: Path to output Excel file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read CSV with best encoding
            df = None
            for encoding in self.encoding_options:
                try:
                    df = pd.read_csv(csv_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                logging.error("Could not read CSV file")
                return False
            
            # Write to Excel
            df.to_excel(excel_path, index=False, engine='openpyxl')
            logging.info(f"Converted CSV to Excel: {excel_path}")
            return True
            
        except Exception as e:
            logging.error(f"CSV to Excel conversion failed: {str(e)}")
            return False
    
    def clean_csv_data(self, csv_path: str, output_path: str) -> bool:
        """
        Clean CSV data (remove duplicates, handle missing values)
        
        Args:
            csv_path: Path to input CSV file
            output_path: Path to cleaned output file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Read CSV
            df = None
            for encoding in self.encoding_options:
                try:
                    df = pd.read_csv(csv_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                return False
            
            original_rows = len(df)
            
            # Remove duplicates
            df = df.drop_duplicates()
            
            # Handle missing values (fill with empty string for object columns)
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].fillna('')
                else:
                    df[col] = df[col].fillna(0)
            
            # Save cleaned data
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            
            cleaned_rows = len(df)
            removed_rows = original_rows - cleaned_rows
            
            logging.info(f"CSV cleaned: {removed_rows} duplicate rows removed")
            return True
            
        except Exception as e:
            logging.error(f"CSV cleaning failed: {str(e)}")
            return False
    
    def get_csv_stats(self, file_path: str) -> Dict:
        """
        Get statistical information about CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Dictionary with statistics
        """
        try:
            analysis = self.analyze_csv(file_path)
            if not analysis.success:
                return {"error": analysis.error_message}
            
            # Read full file for stats
            df = None
            for encoding in self.encoding_options:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                return {"error": "Could not read file"}
            
            stats = {
                "rows": len(df),
                "columns": len(df.columns),
                "file_size_bytes": os.path.getsize(file_path),
                "column_types": df.dtypes.to_dict(),
                "null_counts": df.isnull().sum().to_dict(),
                "detected_type": analysis.detected_type,
                "confidence": analysis.confidence
            }
            
            # Add numeric column statistics
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                stats["numeric_stats"] = df[numeric_cols].describe().to_dict()
            
            return stats
            
        except Exception as e:
            return {"error": str(e)}