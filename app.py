import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.utils import secure_filename
import tempfile
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize SQLAlchemy base class
class Base(DeclarativeBase):
    pass

# Initialize Flask app and database
db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Configure database
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url or "sqlite:///termsheet.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["UPLOAD_FOLDER"] = tempfile.gettempdir()
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB limit
app.config["ALLOWED_EXTENSIONS"] = {"pdf", "docx", "doc", "xlsx", "xls", "png", "jpg", "jpeg"}

# Initialize the app with SQLAlchemy extension
db.init_app(app)

# Import models and utils after app initialization to avoid circular imports
from models import Document, ValidationRule, ValidationResult
from utils.document_processor import process_document
from utils.validation_engine import validate_extracted_data

# Add context processor to provide datetime in all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route('/')
def index():
    """Render the home page"""
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handle document uploads - PROTOTYPE DEMO VERSION (FRONTEND ONLY)"""
    if request.method == 'POST':
        # In prototype version, we just simulate a successful upload
        # and redirect to results with sample data
        
        # Sample extracted data for prototype
        extracted_data = {
            'parties': ['ACME CORPORATION INC.', 'GLOBAL INVESTMENTS LTD.'],
            'effective_date': '2025-03-25',
            'expiration_date': '2030-03-25',
            'transaction_amount': '$5,000,000.00 USD',
            'interest_rate': '5.25%',
            'payment_terms': 'Quarterly payments of interest only with principal due at maturity',
            'collateral': 'All assets of ACME CORPORATION INC.',
            'governing_law': 'State of New York, United States'
        }
        
        # Sample validation results for prototype
        validation_results = {
            'parties': {
                'is_valid': True,
                'message': 'All parties properly identified'
            },
            'effective_date': {
                'is_valid': True,
                'message': 'Date format is valid'
            },
            'expiration_date': {
                'is_valid': True,
                'message': 'Date is after effective date'
            },
            'transaction_amount': {
                'is_valid': True,
                'message': 'Amount is properly formatted'
            },
            'interest_rate': {
                'is_valid': True,
                'message': 'Rate is within acceptable range'
            },
            'payment_terms': {
                'is_valid': True,
                'message': 'Payment terms specified'
            },
            'collateral': {
                'is_valid': True,
                'message': 'Collateral information provided'
            },
            'governing_law': {
                'is_valid': True,
                'message': 'Governing law jurisdiction specified'
            }
        }
        
        # Store in session for prototype
        session['document_id'] = 1
        session['extracted_data'] = extracted_data
        session['validation_results'] = validation_results
        
        flash('Document processed successfully (PROTOTYPE MODE)', 'success')
        return redirect(url_for('results'))
    
    return render_template('upload.html')

@app.route('/results')
def results():
    """Display validation results"""
    if 'extracted_data' not in session or 'validation_results' not in session:
        flash('No document has been processed yet', 'warning')
        return redirect(url_for('upload'))
    
    extracted_data = session.get('extracted_data', {})
    validation_results = session.get('validation_results', {})
    
    # Calculate validation summary
    total_fields = len(validation_results)
    valid_fields = sum(1 for result in validation_results.values() if result['is_valid'])
    validation_percentage = (valid_fields / total_fields * 100) if total_fields > 0 else 0
    
    return render_template(
        'results.html',
        extracted_data=extracted_data,
        validation_results=validation_results,
        validation_percentage=validation_percentage
    )

@app.route('/dashboard')
def dashboard():
    """Display dashboard with sample document data (PROTOTYPE ONLY)"""
    # Create sample document data for prototype
    sample_documents = [
        {
            'id': 1,
            'name': 'ACME-Global Term Sheet',
            'file_type': 'docx',
            'upload_date': datetime.now() - timedelta(hours=2)
        },
        {
            'id': 2,
            'name': 'Financing Agreement Q1-2025',
            'file_type': 'pdf',
            'upload_date': datetime.now() - timedelta(days=2)
        },
        {
            'id': 3,
            'name': 'Investment Terms Summary',
            'file_type': 'xlsx',
            'upload_date': datetime.now() - timedelta(days=5)
        }
    ]
    return render_template('dashboard.html', documents=sample_documents)

@app.route('/document/<int:document_id>')
def document_details(document_id):
    """Display details for a specific document"""
    # Sample document data for prototype
    sample_documents = {
        1: {
            'id': 1,
            'name': 'ACME-Global Term Sheet',
            'file_type': 'docx',
            'upload_date': datetime.now() - timedelta(hours=2)
        },
        2: {
            'id': 2,
            'name': 'Financing Agreement Q1-2025',
            'file_type': 'pdf',
            'upload_date': datetime.now() - timedelta(days=2)
        },
        3: {
            'id': 3,
            'name': 'Investment Terms Summary',
            'file_type': 'xlsx',
            'upload_date': datetime.now() - timedelta(days=5)
        }
    }
    
    document = sample_documents.get(document_id)
    if not document:
        flash('Document not found (Prototype Mode)', 'warning')
        return redirect(url_for('dashboard'))
    
    # Sample validation results for prototype
    validation_results = {
        'parties': {
            'is_valid': True,
            'message': 'All parties properly identified'
        },
        'effective_date': {
            'is_valid': True,
            'message': 'Date format is valid'
        },
        'expiration_date': {
            'is_valid': True,
            'message': 'Date is after effective date'
        },
        'transaction_amount': {
            'is_valid': document_id != 2,  # Simulate an issue in document 2
            'message': 'Amount is properly formatted' if document_id != 2 else 'Invalid amount format'
        },
        'interest_rate': {
            'is_valid': True,
            'message': 'Rate is within acceptable range'
        },
        'payment_terms': {
            'is_valid': document_id != 3,  # Simulate an issue in document 3
            'message': 'Payment terms specified' if document_id != 3 else 'Missing payment terms'
        },
        'collateral': {
            'is_valid': True,
            'message': 'Collateral information provided'
        },
        'governing_law': {
            'is_valid': True,
            'message': 'Governing law jurisdiction specified'
        }
    }
    
    # Calculate validation summary
    total_fields = len(validation_results)
    valid_fields = sum(1 for result in validation_results.values() if result['is_valid'])
    validation_percentage = (valid_fields / total_fields * 100) if total_fields > 0 else 0
    
    return render_template(
        'results.html',
        document=document,
        validation_results=validation_results,
        validation_percentage=validation_percentage
    )

@app.route('/validation_rules', methods=['GET', 'POST'])
def validation_rules():
    """Manage validation rules"""
    if request.method == 'POST':
        field_name = request.form.get('field_name')
        rule_type = request.form.get('rule_type')
        rule_value = request.form.get('rule_value')
        
        if not field_name or not rule_type:
            flash('Field name and rule type are required', 'danger')
            return redirect(url_for('validation_rules'))
        
        # In prototype mode, we just simulate success
        flash('Validation rule added (PROTOTYPE MODE)', 'success')
        return redirect(url_for('validation_rules'))
    
    # Sample validation rules for prototype
    sample_rules = [
        {
            'id': 1,
            'field_name': 'parties',
            'rule_type': 'required',
            'rule_value': 'true'
        },
        {
            'id': 2,
            'field_name': 'effective_date',
            'rule_type': 'date_format',
            'rule_value': '%Y-%m-%d'
        },
        {
            'id': 3,
            'field_name': 'expiration_date',
            'rule_type': 'date_after',
            'rule_value': 'effective_date'
        },
        {
            'id': 4,
            'field_name': 'transaction_amount',
            'rule_type': 'positive_number',
            'rule_value': 'true'
        },
        {
            'id': 5,
            'field_name': 'interest_rate',
            'rule_type': 'range',
            'rule_value': '0,100'
        }
    ]
    
    return render_template('validation_rules.html', rules=sample_rules)

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500

# Create database tables within app context
with app.app_context():
    db.create_all()
