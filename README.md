# Document Classifier & Renamer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-orange.svg)](https://docs.python.org/3/library/tkinter.html)

**An intelligent document classification and renaming system with OCR capabilities.**

Automatically classifies PDF and CSV documents using OCR text recognition and predefined rules, then renames them with structured naming conventions.

## 🚀 Features

- **Automatic Document Classification**: Classifies documents based on content analysis
- **OCR Text Recognition**: Extracts text from PDF documents for analysis
- **Smart Renaming**: Generates structured filenames based on classification
- **Batch Processing**: Process multiple files at once
- **GUI Interface**: Easy-to-use drag-and-drop interface
- **PDF Splitting**: Automatically splits multi-page PDFs when needed
- **Customizable Rules**: Easily add new document types and classification rules

## 📋 Supported Document Types

| Category | Code | Document Type | Example Output |
|----------|------|---------------|----------------|
| **Financial** | 1001 | Financial Statement | `1001_Financial_Statement_2024.pdf` |
| | 1002 | Income Statement | `1002_Income_Statement_2024.pdf` |
| | 1003 | Balance Sheet | `1003_Balance_Sheet_2024.pdf` |
| **Legal** | 2001 | Contract | `2001_Contract_2024.pdf` |
| | 2002 | Agreement | `2002_Agreement_2024.pdf` |
| **Reports** | 3001 | Annual Report | `3001_Annual_Report_2024.pdf` |
| | 3002 | Monthly Report | `3002_Monthly_Report_2024.pdf` |
| **Invoices** | 4001 | Invoice | `4001_Invoice_2024.pdf` |
| | 4002 | Receipt | `4002_Receipt_2024.pdf` |

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Tesseract OCR (for PDF text extraction)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/your-username/document-classifier-renamer.git
cd document-classifier-renamer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Tesseract OCR**
   - **Windows**: Download from [GitHub Tesseract releases](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

4. **Run the application**
```bash
python main.py
```

## 📁 Project Structure

```
document-classifier-renamer/
├── main.py                    # Main application entry point
├── requirements.txt           # Python dependencies
├── core/                      # Core modules
│   ├── __init__.py
│   ├── classifier.py          # Document classification engine
│   ├── ocr_engine.py          # OCR processing
│   ├── pdf_processor.py       # PDF handling
│   └── csv_processor.py       # CSV handling
├── ui/                        # User interface
│   ├── __init__.py
│   └── drag_drop.py           # Drag and drop GUI
├── config/                    # Configuration files
│   └── classification_rules.py
└── examples/                  # Sample documents
    ├── sample_invoice.pdf
    ├── sample_contract.pdf
    └── sample_report.pdf
```

## 🎯 How to Use

### GUI Mode (Recommended)

1. **Launch the application**
   ```bash
   python main.py
   ```

2. **Add documents**
   - Drag and drop files into the application window
   - Or use the "Select Files" button to browse

3. **Configure settings**
   - Set the output date format (YYYY, YYMM, etc.)
   - Choose output directory
   - Enable/disable automatic PDF splitting

4. **Process documents**
   - Click "Classify & Rename" to start processing
   - View results in the results tab

### Command Line Mode

```bash
python main.py --input /path/to/documents --output /path/to/output --batch
```

## 🔧 Configuration

### Adding New Document Types

Edit `config/classification_rules.py` to add new document types:

```python
CLASSIFICATION_RULES = {
    "5001": {
        "name": "Purchase Order",
        "keywords": ["purchase order", "PO", "order request"],
        "priority": 100,
        "category": "procurement"
    }
}
```

### Customizing File Naming

Modify the naming pattern in the configuration:

```python
NAMING_PATTERN = "{code}_{document_type}_{date}.{extension}"
```

## 🧪 Examples

### Sample Input Documents
The `examples/` directory contains sample documents you can use to test the system:
- Business contract
- Financial statement
- Invoice
- Report

### Expected Output
After processing, documents will be renamed following the pattern:
- `input_contract.pdf` → `2001_Contract_2024.pdf`
- `financial_doc.pdf` → `1001_Financial_Statement_2024.pdf`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/your-username/document-classifier-renamer/issues)
- **Documentation**: Check the [Wiki](https://github.com/your-username/document-classifier-renamer/wiki) for detailed documentation

## 🔗 Related Projects

- [OCR Text Recognition](https://github.com/tesseract-ocr/tesseract)
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF) - PDF processing library
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI framework

---

**Built with ❤️ for document management automation**