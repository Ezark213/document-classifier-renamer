"""
Document classification engine
Classifies documents based on content analysis and predefined rules
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional
from config.classification_rules import CLASSIFICATION_RULES


@dataclass
class ClassificationResult:
    """Result of document classification"""
    code: str
    name: str
    confidence: float
    category: str
    matched_keywords: List[str]


class DocumentClassifier:
    """Intelligent document classifier"""
    
    def __init__(self):
        """Initialize classifier with rules"""
        self.rules = CLASSIFICATION_RULES
    
    def classify_document(self, text: str, filename: str = "") -> ClassificationResult:
        """
        Classify a document based on its text content and filename
        
        Args:
            text: Extracted text from document
            filename: Original filename
            
        Returns:
            ClassificationResult with classification details
        """
        # Combine text and filename for analysis
        content = f"{filename} {text}".lower()
        
        best_match = None
        highest_score = 0.0
        
        for code, rule in self.rules.items():
            score, matched_keywords = self._calculate_match_score(content, rule)
            
            if score > highest_score:
                highest_score = score
                best_match = {
                    'code': code,
                    'rule': rule,
                    'matched_keywords': matched_keywords
                }
        
        if best_match and highest_score > 0.1:  # Minimum confidence threshold
            return ClassificationResult(
                code=best_match['code'],
                name=best_match['rule']['name'],
                confidence=min(highest_score, 1.0),
                category=best_match['rule']['category'],
                matched_keywords=best_match['matched_keywords']
            )
        else:
            # Default classification for unrecognized documents
            return ClassificationResult(
                code="9999",
                name="Unclassified Document",
                confidence=0.1,
                category="general",
                matched_keywords=[]
            )
    
    def classify_csv_file(self, file_path: str) -> ClassificationResult:
        """
        Classify CSV files based on filename and headers
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            ClassificationResult
        """
        import pandas as pd
        import os
        
        filename = os.path.basename(file_path).lower()
        
        try:
            # Read first few rows to analyze headers
            df = pd.read_csv(file_path, nrows=5)
            headers = ' '.join(df.columns.astype(str)).lower()
            content = f"{filename} {headers}"
            
            return self.classify_document(content, filename)
        
        except Exception:
            # If can't read CSV, classify based on filename only
            return self.classify_document("", filename)
    
    def _calculate_match_score(self, content: str, rule: Dict) -> tuple[float, List[str]]:
        """
        Calculate match score for a classification rule
        
        Args:
            content: Document content (text + filename)
            rule: Classification rule dictionary
            
        Returns:
            Tuple of (score, matched_keywords)
        """
        matched_keywords = []
        total_score = 0.0
        
        keywords = rule.get('keywords', [])
        priority = rule.get('priority', 1)
        
        for keyword in keywords:
            if keyword.lower() in content:
                matched_keywords.append(keyword)
                # Score based on keyword importance and rule priority
                keyword_score = 1.0 / len(keywords)  # Distribute score among keywords
                total_score += keyword_score
        
        # Apply priority multiplier
        total_score *= (priority / 100.0)
        
        # Bonus for exact filename matches
        if rule['name'].lower() in content:
            total_score += 0.2
        
        return total_score, matched_keywords
    
    def get_supported_categories(self) -> List[str]:
        """Get list of supported document categories"""
        categories = set()
        for rule in self.rules.values():
            categories.add(rule['category'])
        return sorted(list(categories))
    
    def get_rules_by_category(self, category: str) -> Dict[str, Dict]:
        """Get all classification rules for a specific category"""
        return {
            code: rule for code, rule in self.rules.items()
            if rule['category'] == category
        }