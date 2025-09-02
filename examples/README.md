# Example Documents

This directory contains sample documents that you can use to test the Document Classifier & Renamer system.

## Sample Files

### 1. Financial Documents
- **sample_invoice.pdf** - A typical business invoice
- **sample_financial_statement.pdf** - A basic financial statement
- **sample_balance_sheet.pdf** - A company balance sheet

### 2. Legal Documents  
- **sample_contract.pdf** - A service agreement contract
- **sample_nda.pdf** - A non-disclosure agreement

### 3. Reports
- **sample_monthly_report.pdf** - A monthly business report
- **sample_project_report.pdf** - A project status report

### 4. Data Files
- **sample_customer_data.csv** - Customer information in CSV format
- **sample_sales_data.csv** - Sales transaction data
- **sample_inventory.csv** - Product inventory data

## How to Test

1. Launch the Document Classifier & Renamer application
2. Drag and drop these sample files into the application
3. Configure your settings (date format, output directory)
4. Click "Classify & Rename Files" to see the classification in action
5. Check the results tab to see how each document was classified

## Expected Results

The classifier should automatically detect and rename files as follows:

| Original File | Expected Classification | New Filename |
|---------------|------------------------|--------------|
| sample_invoice.pdf | Invoice (4001) | 4001_Invoice_2024.pdf |
| sample_contract.pdf | Contract (2001) | 2001_Contract_2024.pdf |
| sample_monthly_report.pdf | Monthly Report (3002) | 3002_Monthly_Report_2024.pdf |
| sample_customer_data.csv | Customer Information (8001) | 8001_Customer_Information_2024.csv |
| sample_sales_data.csv | Data Export (7001) | 7001_Data_Export_2024.csv |

## Creating Your Own Test Files

To create additional test documents:

1. Create documents with relevant keywords from the classification rules
2. Include terms like "invoice", "contract", "report", etc. in the content
3. Use descriptive filenames that hint at the document type
4. Test with both PDF and CSV formats

## Notes

- The actual classification depends on the content of the documents
- The system uses OCR to read PDF content, so image-based PDFs may have different results
- CSV files are classified based on column headers and filenames
- You can adjust classification rules in `config/classification_rules.py`