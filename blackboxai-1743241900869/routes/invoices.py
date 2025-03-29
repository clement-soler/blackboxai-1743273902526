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
    invoice = Invoice.query.options(
        db.joinedload(Invoice.consultation).joinedload(Consultation.patient)
    ).get_or_404(invoice_id)
    return render_template('invoices/view.html', invoice=invoice)

from fpdf import FPDF
import os

@invoices_bp.route('/<int:invoice_id>/download', methods=['GET'])
def download_invoice(invoice_id):
    invoice = Invoice.query.options(
        db.joinedload(Invoice.consultation).joinedload(Consultation.patient)
    ).get_or_404(invoice_id)
    
    # Création du PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # En-tête
    pdf.cell(200, 10, txt="Facture #" + invoice.number, ln=1, align='C')
    pdf.cell(200, 10, txt="Date: " + invoice.issue_date.strftime('%d/%m/%Y'), ln=1, align='C')
    pdf.ln(10)
    
    # Informations praticien
    pdf.cell(200, 10, txt="OsteoManager", ln=1)
    pdf.cell(200, 10, txt="123 Rue des Ostéopathes", ln=1)
    pdf.cell(200, 10, txt="75000 Paris", ln=1)
    pdf.ln(10)
    
    # Informations patient
    patient = invoice.consultation.patient
    pdf.cell(200, 10, txt=f"Patient: {patient.first_name} {patient.last_name}", ln=1)
    pdf.ln(5)
    
    # Détails facture
    pdf.cell(200, 10, txt="Consultation du: " + invoice.consultation.date.strftime('%d/%m/%Y'), ln=1)
    pdf.cell(200, 10, txt="Motif: " + invoice.consultation.reason, ln=1)
    pdf.ln(10)
    
    # Montant
    # Utilisation d'une police système standard
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, txt=f"Montant: {invoice.amount} EUR", ln=1)
    pdf.ln(10)
    
    # Mentions légales
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="TVA non applicable, article 293B du CGI", ln=1)
    
    # Génération du fichier
    filename = f"facture_{invoice.number.replace('/', '-')}.pdf"
    pdf.output(filename)
    
    response = send_from_directory('.', filename, as_attachment=True)
    
    # Suppression du fichier après l'envoi
    @response.call_on_close
    def remove_file():
        try:
            os.remove(filename)
        except:
            pass
            
    return response

@invoices_bp.route('/consultation/<int:consultation_id>', methods=['GET', 'POST'])
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