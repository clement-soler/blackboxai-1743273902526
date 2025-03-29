from flask import Blueprint, request, jsonify, render_template
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
    consultation = Consultation.query.get_or_404(consultation_id)
    return render_template('consultations/view.html', consultation=consultation)

@consultations_bp.route('/new', methods=['GET'])
def new_consultation_form():
    patients = Patient.query.order_by(Patient.last_name).all()
    return render_template('consultations/form.html', 
                         patients=patients,
                         now=datetime.now())

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