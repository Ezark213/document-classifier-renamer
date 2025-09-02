"""
Document classification rules and patterns
"""

# Document classification rules
# Each rule defines how to classify documents based on keywords and patterns
CLASSIFICATION_RULES = {
    # Financial Documents
    "1001": {
        "name": "Financial Statement",
        "keywords": [
            "financial statement", "statement of financial position",
            "balance sheet", "income statement", "profit and loss",
            "cash flow statement", "financial report"
        ],
        "priority": 150,
        "category": "financial"
    },
    
    "1002": {
        "name": "Income Statement",
        "keywords": [
            "income statement", "profit and loss statement", "p&l",
            "earnings report", "revenue statement", "operating income"
        ],
        "priority": 140,
        "category": "financial"
    },
    
    "1003": {
        "name": "Balance Sheet",
        "keywords": [
            "balance sheet", "statement of financial position",
            "assets and liabilities", "shareholders equity"
        ],
        "priority": 140,
        "category": "financial"
    },
    
    "1004": {
        "name": "Cash Flow Statement",
        "keywords": [
            "cash flow statement", "statement of cash flows",
            "cash flow report", "operating cash flow"
        ],
        "priority": 130,
        "category": "financial"
    },
    
    "1005": {
        "name": "Budget Report",
        "keywords": [
            "budget", "budget report", "financial budget",
            "annual budget", "budget analysis"
        ],
        "priority": 120,
        "category": "financial"
    },
    
    # Legal Documents
    "2001": {
        "name": "Contract",
        "keywords": [
            "contract", "agreement", "service agreement",
            "terms and conditions", "legal agreement", "parties agree"
        ],
        "priority": 160,
        "category": "legal"
    },
    
    "2002": {
        "name": "Non-Disclosure Agreement",
        "keywords": [
            "non-disclosure agreement", "nda", "confidentiality agreement",
            "confidential information", "proprietary information"
        ],
        "priority": 150,
        "category": "legal"
    },
    
    "2003": {
        "name": "Terms of Service",
        "keywords": [
            "terms of service", "terms of use", "user agreement",
            "service terms", "website terms"
        ],
        "priority": 130,
        "category": "legal"
    },
    
    # Business Reports
    "3001": {
        "name": "Annual Report",
        "keywords": [
            "annual report", "yearly report", "year end report",
            "annual summary", "business review"
        ],
        "priority": 140,
        "category": "reports"
    },
    
    "3002": {
        "name": "Monthly Report",
        "keywords": [
            "monthly report", "month end report", "monthly summary",
            "performance report", "status report"
        ],
        "priority": 130,
        "category": "reports"
    },
    
    "3003": {
        "name": "Project Report",
        "keywords": [
            "project report", "project status", "project summary",
            "milestone report", "progress report"
        ],
        "priority": 120,
        "category": "reports"
    },
    
    "3004": {
        "name": "Market Research",
        "keywords": [
            "market research", "market analysis", "industry report",
            "market survey", "competitive analysis"
        ],
        "priority": 125,
        "category": "reports"
    },
    
    # Invoicing and Billing
    "4001": {
        "name": "Invoice",
        "keywords": [
            "invoice", "bill", "invoice number", "amount due",
            "payment due", "billing", "invoice date"
        ],
        "priority": 170,
        "category": "billing"
    },
    
    "4002": {
        "name": "Receipt",
        "keywords": [
            "receipt", "payment receipt", "transaction receipt",
            "proof of payment", "received payment"
        ],
        "priority": 160,
        "category": "billing"
    },
    
    "4003": {
        "name": "Purchase Order",
        "keywords": [
            "purchase order", "po number", "order request",
            "purchase requisition", "procurement"
        ],
        "priority": 150,
        "category": "billing"
    },
    
    "4004": {
        "name": "Quote",
        "keywords": [
            "quote", "quotation", "estimate", "pricing",
            "proposal", "cost estimate"
        ],
        "priority": 130,
        "category": "billing"
    },
    
    # HR Documents
    "5001": {
        "name": "Employee Contract",
        "keywords": [
            "employment contract", "job offer", "employment agreement",
            "employee handbook", "job description"
        ],
        "priority": 150,
        "category": "hr"
    },
    
    "5002": {
        "name": "Payroll Report",
        "keywords": [
            "payroll", "salary report", "wage report",
            "payroll summary", "employee compensation"
        ],
        "priority": 140,
        "category": "hr"
    },
    
    "5003": {
        "name": "Performance Review",
        "keywords": [
            "performance review", "employee evaluation", "annual review",
            "performance appraisal", "employee assessment"
        ],
        "priority": 130,
        "category": "hr"
    },
    
    # Insurance Documents
    "6001": {
        "name": "Insurance Policy",
        "keywords": [
            "insurance policy", "policy number", "coverage",
            "insurance certificate", "policy holder"
        ],
        "priority": 140,
        "category": "insurance"
    },
    
    "6002": {
        "name": "Insurance Claim",
        "keywords": [
            "insurance claim", "claim number", "claim form",
            "damage report", "incident report"
        ],
        "priority": 150,
        "category": "insurance"
    },
    
    # Data and Analytics
    "7001": {
        "name": "Data Export",
        "keywords": [
            "data export", "database export", "data dump",
            "exported data", "data file"
        ],
        "priority": 100,
        "category": "data"
    },
    
    "7002": {
        "name": "Analytics Report",
        "keywords": [
            "analytics", "data analysis", "statistics",
            "metrics", "dashboard", "kpi"
        ],
        "priority": 110,
        "category": "data"
    },
    
    # Customer Documents
    "8001": {
        "name": "Customer Information",
        "keywords": [
            "customer", "client", "contact information",
            "customer data", "client list"
        ],
        "priority": 120,
        "category": "customer"
    },
    
    "8002": {
        "name": "Customer Feedback",
        "keywords": [
            "customer feedback", "survey", "review",
            "customer satisfaction", "testimonial"
        ],
        "priority": 110,
        "category": "customer"
    }
}

# Category descriptions
CATEGORY_DESCRIPTIONS = {
    "financial": "Financial statements, budgets, and accounting documents",
    "legal": "Contracts, agreements, and legal documents",
    "reports": "Business reports, analysis, and summaries",
    "billing": "Invoices, receipts, and payment documents",
    "hr": "Human resources and employee documents",
    "insurance": "Insurance policies and claims",
    "data": "Data exports and analytics reports",
    "customer": "Customer information and feedback"
}

# Default fallback rule
DEFAULT_RULE = {
    "code": "9999",
    "name": "Unclassified Document",
    "category": "general",
    "confidence": 0.1
}