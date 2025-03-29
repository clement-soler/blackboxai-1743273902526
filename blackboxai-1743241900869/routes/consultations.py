from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models import Consultation, Patient, db
from datetime import datetime

consultations_bp = Blueprint('consultations', __name__)

@consultations_bp.route('', methods=['GET'])
def list_consultations():
    consultations = Consultation.query.order_by(Consultation.date.desc()).all()
    patients = Patient.query.all()
    return render_template('consultations/list.html', 
                         consultations=consultations,
                         patients=patients)

@consultations_bp.route('/<int:consultation_id>', methods=['GET'])
def view_consultation(consultation_id):
    consultation = Consultation.query.options(
        db.joinedload(Consultation.patient),
        db.joinedload(Consultation.invoice)
    ).get_or_404(consultation_id)
    return render_template('consultations/view.html', consultation=consultation)

@consultations_bp.route('/<int:consultation_id>/edit', methods=['GET', 'POST'])
def edit_consultation(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    patients = Patient.query.all()
    
    if request.method == 'POST':
        consultation.date = datetime.strptime(request.form['date'], '%Y-%m-%dT%H:%M')
        consultation.reason = request.form['reason']
        consultation.price = float(request.form['price'])
        consultation.patient_id = int(request.form['patient_id'])
        consultation.notes = request.form.get('notes', '')
        
        db.session.commit()
        return redirect(url_for('consultations.view_consultation', consultation_id=consultation.id))
    
    return render_template('consultations/edit.html', 
                         consultation=consultation,
                         patients=patients)

@consultations_bp.route('/new', methods=['GET'])
def new_consultation_form():
    patients = Patient.query.order_by(Patient.last_name).all()
    return render_template('consultations/form.html', 
                         patients=patients,
                         now=datetime.now())

@consultations_bp.route('/patient/<int:patient_id>/new', methods=['GET'])
def new_patient_consultation_form(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template('consultations/form.html',
                         patients=[patient],
                         now=datetime.now(),
                         from_patient=True)

@consultations_bp.route('', methods=['POST'])
def create_consultation():
    data = request.form
    date = datetime.strptime(f"{data['date']} {data['time']}", '%Y-%m-%d %H:%M')
    
    consultation = Consultation(
        patient_id=data['patient_id'],
        date=date,
        reason=data['reason'],
        notes=data['notes'],
        price=float(data['price'])
    )
    
    db.session.add(consultation)
    db.session.commit()
    return jsonify({'message': 'Consultation created successfully', 'id': consultation.id}), 201

@consultations_bp.route('/<int:consultation_id>', methods=['PUT'])
def update_consultation(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    data = request.form
    date = datetime.strptime(f"{data['date']} {data['time']}", '%Y-%m-%d %H:%M')
    
    consultation.patient_id = data['patient_id']
    consultation.date = date
    consultation.reason = data['reason']
    consultation.notes = data['notes']
    consultation.price = float(data['price'])
    
    db.session.commit()
    return jsonify({'message': 'Consultation updated successfully'})

@consultations_bp.route('/<int:consultation_id>', methods=['DELETE'])
def delete_consultation(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    db.session.delete(consultation)
    db.session.commit()
    return jsonify({'message': 'Consultation deleted successfully'})