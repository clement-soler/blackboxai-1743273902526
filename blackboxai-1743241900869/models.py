from datetime import datetime
from app import db

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    consultations = db.relationship('Consultation', backref='patient', lazy=True)
    medical_history = db.relationship('MedicalHistory', backref='patient', lazy=True)
    documents = db.relationship('Document', backref='patient', lazy=True)

class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(200))
    notes = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    invoice = db.relationship('Invoice', backref='consultation', uselist=False, lazy=True)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consultation_id = db.Column(db.Integer, db.ForeignKey('consultation.id'), nullable=False)
    number = db.Column(db.String(20), unique=True, nullable=False)
    issue_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.Date)
    amount = db.Column(db.Float, nullable=False)
    tax_rate = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='pending')  # pending/paid/cancelled
    payment_type = db.Column(db.String(20))  # CB/Cheque/Especes/Other
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MedicalHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    treatment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    document_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)