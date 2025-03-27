"""Configuration settings for the term sheet validation application"""

import os

class Config:
    """Base configuration class"""
    # Flask configuration
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev_secret_key')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/tmp')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///termsheet.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    
    # File types
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'xlsx', 'xls', 'png', 'jpg', 'jpeg'}
    
    # NLP and OCR settings
    SPACY_MODEL = 'en_core_web_sm'
    OCR_LANG = 'eng'
    
    # Term sheet field definitions - these are key fields we'll extract from term sheets
    TERM_SHEET_FIELDS = {
        'parties': {
            'type': 'entity',
            'required': True,
            'description': 'Names of parties involved in the agreement'
        },
        'effective_date': {
            'type': 'date',
            'required': True,
            'description': 'The date when the agreement becomes effective'
        },
        'expiration_date': {
            'type': 'date',
            'required': False,
            'description': 'The date when the agreement expires'
        },
        'transaction_amount': {
            'type': 'currency',
            'required': True,
            'description': 'The principal amount of the transaction'
        },
        'interest_rate': {
            'type': 'percentage',
            'required': False,
            'description': 'The interest rate applicable to the transaction'
        },
        'payment_terms': {
            'type': 'text',
            'required': True,
            'description': 'Terms describing payment schedule and conditions'
        },
        'collateral': {
            'type': 'text',
            'required': False,
            'description': 'Description of any collateral securing the transaction'
        },
        'governing_law': {
            'type': 'text',
            'required': True,
            'description': 'The jurisdiction whose laws govern the agreement'
        }
    }
    
    # Default validation rules
    DEFAULT_VALIDATION_RULES = [
        {
            'field_name': 'parties',
            'rule_type': 'required',
            'rule_value': 'true'
        },
        {
            'field_name': 'effective_date',
            'rule_type': 'date_format',
            'rule_value': '%Y-%m-%d'
        },
        {
            'field_name': 'expiration_date',
            'rule_type': 'date_after',
            'rule_value': 'effective_date'
        },
        {
            'field_name': 'transaction_amount',
            'rule_type': 'positive_number',
            'rule_value': 'true'
        },
        {
            'field_name': 'interest_rate',
            'rule_type': 'range',
            'rule_value': '0,100'
        }
    ]
