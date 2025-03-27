"""Validation engine for term sheet data"""

import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

def validate_extracted_data(extracted_data):
    """
    Validate extracted data against predefined rules
    
    Args:
        extracted_data (dict): Extracted data from term sheet
    
    Returns:
        dict: Validation results for each field
    """
    if not extracted_data:
        return {}
    
    validation_results = {}
    
    # Validate parties field
    if 'parties' in extracted_data:
        parties = extracted_data['parties']
        if parties and len(parties) >= 2:
            validation_results['parties'] = {
                'is_valid': True,
                'message': f'Found {len(parties)} parties'
            }
        else:
            validation_results['parties'] = {
                'is_valid': False,
                'message': 'At least two parties are required'
            }
    else:
        validation_results['parties'] = {
            'is_valid': False,
            'message': 'Parties information not found'
        }
    
    # Validate effective date
    if 'effective_date' in extracted_data:
        effective_date = extracted_data['effective_date']
        date_valid = validate_date(effective_date)
        
        validation_results['effective_date'] = {
            'is_valid': date_valid,
            'message': 'Valid date format' if date_valid else 'Invalid date format'
        }
    else:
        validation_results['effective_date'] = {
            'is_valid': False,
            'message': 'Effective date not found'
        }
    
    # Validate expiration date if present
    if 'expiration_date' in extracted_data:
        expiration_date = extracted_data['expiration_date']
        date_valid = validate_date(expiration_date)
        
        # Check if expiration is after effective date
        if date_valid and 'effective_date' in extracted_data:
            try:
                effective = datetime.strptime(extracted_data['effective_date'], '%Y-%m-%d')
                expiration = datetime.strptime(expiration_date, '%Y-%m-%d')
                
                if expiration > effective:
                    validation_results['expiration_date'] = {
                        'is_valid': True,
                        'message': 'Valid date and after effective date'
                    }
                else:
                    validation_results['expiration_date'] = {
                        'is_valid': False,
                        'message': 'Expiration date must be after effective date'
                    }
            except:
                validation_results['expiration_date'] = {
                    'is_valid': date_valid,
                    'message': 'Valid date format' if date_valid else 'Invalid date format'
                }
        else:
            validation_results['expiration_date'] = {
                'is_valid': date_valid,
                'message': 'Valid date format' if date_valid else 'Invalid date format'
            }
    
    # Validate transaction amount
    if 'transaction_amount' in extracted_data:
        amount = extracted_data['transaction_amount']
        
        # Convert amount to numeric
        try:
            # Remove currency symbols and commas
            cleaned_amount = re.sub(r'[^\d.]', '', amount)
            numeric_amount = float(cleaned_amount)
            
            if numeric_amount > 0:
                validation_results['transaction_amount'] = {
                    'is_valid': True,
                    'message': f'Valid amount: {amount}'
                }
            else:
                validation_results['transaction_amount'] = {
                    'is_valid': False,
                    'message': 'Amount must be positive'
                }
        except:
            validation_results['transaction_amount'] = {
                'is_valid': False,
                'message': f'Unable to parse amount: {amount}'
            }
    else:
        validation_results['transaction_amount'] = {
            'is_valid': False,
            'message': 'Transaction amount not found'
        }
    
    # Validate interest rate if present
    if 'interest_rate' in extracted_data:
        rate = extracted_data['interest_rate']
        
        try:
            # Remove percentage symbol if present
            cleaned_rate = rate.replace('%', '').strip()
            numeric_rate = float(cleaned_rate)
            
            if 0 <= numeric_rate <= 100:
                validation_results['interest_rate'] = {
                    'is_valid': True,
                    'message': f'Valid rate: {rate}'
                }
            else:
                validation_results['interest_rate'] = {
                    'is_valid': False,
                    'message': 'Interest rate must be between 0 and 100%'
                }
        except:
            validation_results['interest_rate'] = {
                'is_valid': False,
                'message': f'Unable to parse interest rate: {rate}'
            }
    
    # Validate payment terms if present
    if 'payment_terms' in extracted_data:
        terms = extracted_data['payment_terms']
        
        if len(terms) > 10:  # Simple validation just checking length
            validation_results['payment_terms'] = {
                'is_valid': True,
                'message': 'Payment terms provided'
            }
        else:
            validation_results['payment_terms'] = {
                'is_valid': False,
                'message': 'Payment terms insufficient'
            }
    
    # Validate governing law if present
    if 'governing_law' in extracted_data:
        law = extracted_data['governing_law']
        
        if len(law) > 3:  # Simple validation just checking length
            validation_results['governing_law'] = {
                'is_valid': True,
                'message': f'Governing law specified: {law}'
            }
        else:
            validation_results['governing_law'] = {
                'is_valid': False,
                'message': 'Governing law description insufficient'
            }
    
    # Mark any fields required by configuration but not present as invalid
    required_fields = ['parties', 'effective_date', 'transaction_amount', 'payment_terms', 'governing_law']
    for field in required_fields:
        if field not in validation_results:
            validation_results[field] = {
                'is_valid': False,
                'message': f'Required field {field} not found'
            }
    
    return validation_results

def validate_date(date_str):
    """
    Validate a date string
    
    Args:
        date_str (str): Date string to validate
    
    Returns:
        bool: True if valid date format, False otherwise
    """
    try:
        # Try to parse the date - assuming YYYY-MM-DD format
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except:
        # If standard format fails, try other common formats
        for fmt in ('%m/%d/%Y', '%Y/%m/%d', '%B %d, %Y', '%b %d, %Y'):
            try:
                datetime.strptime(date_str, fmt)
                return True
            except:
                continue
        
        return False
