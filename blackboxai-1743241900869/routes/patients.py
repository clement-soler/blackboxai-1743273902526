from flask import Blueprint, request, jsonify, render_template
from models import Patient, db
from datetime import datetime

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('', methods=['GET'])
def list_patients():
    patients = Patient.query.order_by(Patient.last_name).all()
    return render_template('patients/list.html', patients=patients)

@patients_bp.route('/<int:patient_id>', methods=['GET'])
def view_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template('patients/view.html', patient=patient)

@patients_bp.route('/new', methods=['GET'])
def new_patient_form():
    return render_template('patients/form.html')

@patients_bp.route('', methods=['POST'])
def create_patient():
    data = request.form
    birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date() if data['birth_date'] else None
    
    patient = Patient(
        first_name=data['first_name'],
        last_name=data['last_name'],
        birth_date=birth_date,
        phone=data['phone'],
        email=data['email'],
        address=data['address']
    )
    
    db.session.add(patient)
    db.session.commit()
    return jsonify({'message': 'Patient created successfully', 'id': patient.id}), 201

@patients_bp.route('/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.form
    birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date() if data['birth_date'] else None
    
    patient.first_name = data['first_name']
    patient.last_name = data['last_name']
    patient.birth_date = birth_date
    patient.phone = data['phone']
    patient.email = data['email']
    patient.address = data['address']
    
    db.session.commit()
    return jsonify({'message': 'Patient updated successfully'})

@patients_bp.route('/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({'message': 'Patient deleted successfully'})