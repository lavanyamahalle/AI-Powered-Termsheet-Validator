"""NLP utilities for term sheet validation"""

import logging
import spacy
import re
from datetime import datetime

logger = logging.getLogger(__name__)

# Initialize spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.warning("Downloading spaCy model 'en_core_web_sm'...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    """
    Extract named entities from text using spaCy
    
    Args:
        text (str): Input text
    
    Returns:
        dict: Dictionary of entities grouped by type
    """
    if not text:
        return {}
    
    try:
        doc = nlp(text)
        
        # Group entities by type
        entities = {}
        for ent in doc.ents:
            entity_type = ent.label_
            if entity_type not in entities:
                entities[entity_type] = []
            
            # Add entity if not already present
            if ent.text.strip() not in entities[entity_type]:
                entities[entity_type].append(ent.text.strip())
        
        return entities
    
    except Exception as e:
        logger.error(f"Error extracting entities: {str(e)}")
        return {}

def extract_dates(text):
    """
    Extract dates from text using regex and spaCy
    
    Args:
        text (str): Input text
    
    Returns:
        list: List of date strings found in text
    """
    if not text:
        return []
    
    try:
        # Use spaCy to extract DATE entities
        doc = nlp(text)
        dates = [ent.text for ent in doc.ents if ent.label_ == 'DATE']
        
        # Also use regex patterns for common date formats
        date_patterns = [
            # MM/DD/YYYY
            r'\b(0?[1-9]|1[0-2])[\/\-](0?[1-9]|[12][0-9]|3[01])[\/\-](19|20)\d{2}\b',
            # YYYY/MM/DD
            r'\b(19|20)\d{2}[\/\-](0?[1-9]|1[0-2])[\/\-](0?[1-9]|[12][0-9]|3[01])\b',
            # Month DD, YYYY
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+(0?[1-9]|[12][0-9]|3[01])(?:st|nd|rd|th)?,?\s+(19|20)\d{2}\b'
        ]
        
        for pattern in date_patterns:
            regex_dates = re.findall(pattern, text)
            if regex_dates:
                # Convert tuple matches to strings if necessary
                for match in regex_dates:
                    if isinstance(match, tuple):
                        date_str = '/'.join(match)
                    else:
                        date_str = match
                    
                    if date_str not in dates:
                        dates.append(date_str)
        
        # Try to parse and standardize dates
        standardized_dates = []
        for date_str in dates:
            try:
                # Try to parse the date - this is simplified and would need more robust handling
                standardized_date = parse_and_standardize_date(date_str)
                if standardized_date and standardized_date not in standardized_dates:
                    standardized_dates.append(standardized_date)
            except:
                # If parsing fails, keep the original string
                if date_str not in standardized_dates:
                    standardized_dates.append(date_str)
        
        return standardized_dates
    
    except Exception as e:
        logger.error(f"Error extracting dates: {str(e)}")
        return []

def parse_and_standardize_date(date_str):
    """
    Attempt to parse a date string into a standardized format
    
    Args:
        date_str (str): Input date string
    
    Returns:
        str: Standardized date string in YYYY-MM-DD format or original if parsing fails
    """
    # This is a simplified version - would need more robust handling for production
    try:
        # Try to handle multiple formats
        for fmt in ('%m/%d/%Y', '%Y/%m/%d', '%Y-%m-%d', 
                   '%B %d, %Y', '%b %d, %Y', '%d %B %Y', '%d %b %Y'):
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        # If none of the formats match, return the original
        return date_str
    
    except Exception:
        return date_str

def extract_amounts(text):
    """
    Extract monetary amounts from text
    
    Args:
        text (str): Input text
    
    Returns:
        list: List of monetary amount strings found in text
    """
    if not text:
        return []
    
    try:
        # Pattern for currency amounts like $1,000.00 or 1,000.00 USD
        amount_patterns = [
            r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:USD|EUR|GBP|JPY|CHF)',
            r'(?:USD|EUR|GBP|JPY|CHF)\s*(\d+(?:,\d{3})*(?:\.\d{2})?)'
        ]
        
        amounts = []
        for pattern in amount_patterns:
            matches = re.findall(pattern, text)
            amounts.extend(matches)
        
        # Filter out duplicates and sort by value (if possible)
        unique_amounts = list(set(amounts))
        
        # Try to sort by numeric value
        try:
            # Convert to numeric values for sorting
            numeric_amounts = [(amount, float(amount.replace(',', ''))) for amount in unique_amounts]
            numeric_amounts.sort(key=lambda x: x[1], reverse=True)
            return [amount for amount, _ in numeric_amounts]
        except:
            # If conversion fails, return unsorted
            return unique_amounts
    
    except Exception as e:
        logger.error(f"Error extracting amounts: {str(e)}")
        return []
