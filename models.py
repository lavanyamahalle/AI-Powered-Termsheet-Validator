from app import db
from datetime import datetime

class Document(db.Model):
    """Model for storing document information"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(255), nullable=True)
    validation_results = db.relationship('ValidationResult', backref='document', lazy=True)

    def __repr__(self):
        return f'<Document {self.name}>'

class ValidationRule(db.Model):
    """Model for storing validation rules"""
    id = db.Column(db.Integer, primary_key=True)
    field_name = db.Column(db.String(100), nullable=False)
    rule_type = db.Column(db.String(50), nullable=False)  # e.g., 'required', 'date_format', 'range', 'regex'
    rule_value = db.Column(db.String(255), nullable=True)  # Rule parameters, e.g., regex pattern, min/max values

    def __repr__(self):
        return f'<ValidationRule {self.field_name}: {self.rule_type}>'

class ValidationResult(db.Model):
    """Model for storing validation results for each document"""
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    field_name = db.Column(db.String(100), nullable=False)
    is_valid = db.Column(db.Boolean, default=False)
    message = db.Column(db.String(255), nullable=True)  # Validation message or error

    def __repr__(self):
        return f'<ValidationResult {self.field_name}: {"valid" if self.is_valid else "invalid"}>'

class ExtractedTerm(db.Model):
    """Model for storing extracted terms from term sheets"""
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    term_name = db.Column(db.String(100), nullable=False)  # e.g., 'party_name', 'effective_date', 'amount'
    term_value = db.Column(db.Text, nullable=True)
    confidence_score = db.Column(db.Float, nullable=True)  # Confidence level of the extraction

    def __repr__(self):
        return f'<ExtractedTerm {self.term_name}: {self.term_value}>'
