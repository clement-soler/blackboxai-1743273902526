from flask import Blueprint, request, jsonify, render_template, send_from_directory
from models import Invoice, Consultation, db
from datetime import datetime, timedelta
import os

invoices_bp = Blueprint('invoices', __name__)

@invoices_bp.route('', methods=['GET'])
def list_invoices():
    invoices = Invoice.query.order_by(Invoice.issue_date.desc()).all()
    return render_template('invoices/list.html', invoices=invoices)

@invoices_bp.route('/<int:invoice_id>', methods=['GET'])
def view_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return render_template('invoices/view.html', invoice=invoice)

@invoices_bp.route('/<int:invoice_id>/download', methods=['GET'])
def download_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    # In a real implementation, this would generate and return a PDF
    return jsonify({'message': 'PDF generation would happen here'})

@invoices_bp.route('/consultation/<int:consultation_id>', methods=['POST'])
def create_invoice(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    
    # Generate invoice number (YYYYMMDD-XXX)
    today = datetime.now()
    invoice_count = Invoice.query.filter(
        db.func.strftime('%Y%m%d', Invoice.issue_date) == today.strftime('%Y%m%d')
    ).count()
    invoice_number = f"{today.strftime('%Y%m%d')}-{invoice_count + 1:03d}"
    
    invoice = Invoice(
        consultation_id=consultation.id,
        number=invoice_number,
        issue_date=today.date(),
        due_date=(today + timedelta(days=30)).date(),
        amount=consultation.price,
        tax_rate=0.0  # Assuming no tax for medical services
    )
    
    db.session.add(invoice)
    db.session.commit()
    return jsonify({'message': 'Invoice created successfully', 'id': invoice.id}), 201

@invoices_bp.route('/<int:invoice_id>/mark-paid', methods=['PUT'])
def mark_invoice_paid(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    invoice.status = 'paid'
    invoice.payment_date = datetime.now()
    db.session.commit()
    return jsonify({'message': 'Invoice marked as paid'})