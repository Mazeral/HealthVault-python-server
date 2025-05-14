from flask_login import login_required
from flask import Blueprint, request, jsonify, session
import datetime
from models.patient import Patient
from models.base import db
from models.medical_record import MedicalRecord
from models.lab_result import LabResult


patientbp = Blueprint('Patient', __name__, url_prefix='/patient')


@patientbp.route('/', methods=['POST'])
@login_required
def new_patient():
    """Create a new patient."""
    data = request.get_json()
    if not data or 'name' not in data or 'dob' not in data or 'gender' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        dob = datetime.datetime.strptime(data['dob'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format for dob (YYYY-MM-DD)'}), 400

    new_patient = Patient(name=data['name'], dob=dob, gender=data['gender'],
                          contact=data.get('contact'))
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient created successfully', 'id': new_patient.id}), 201

@patientbp.route('/<int:patient_id>', methods=['GET'])
@login_required
def get_patient_id(patient_id):
    """Retrieve a specific patient by ID."""
    patient = db.session.get(Patient, patient_id)
    if patient:
        return jsonify(patient.to_dict())
    return jsonify({'error': 'Patient not found'}), 404

@patientbp.route('/patients', methods=['GET'])
@login_required
def get_patients():
    """Retrieve all patients."""
    patients = Patient.query.all()
    return jsonify([patient.to_dict() for patient in patients])

@patientbp.route('/<int:patient_id>', methods=['POST'])
@login_required
def update_patient(patient_id):
    """Update an existing patient's information."""
    patient = db.session.get(Patient, patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    data = request.get_json()
    if data:
        patient.name = data.get('name', patient.name)
        if 'dob' in data:
            try:
                patient.dob = datetime.datetime.strptime(data['dob'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format for dob (YYYY-MM-DD)'}), 400
        patient.gender = data.get('gender', patient.gender)
        patient.contact = data.get('contact', patient.contact)
        db.session.commit()
        return jsonify({'message': 'Patient updated successfully'})
    return jsonify({'message': 'No data provided for update'}), 200

@patientbp.route('/<int:patient_id>/medical_record',
                 methods=['POST'])
@login_required
def add_record(patient_id):
    """Add a medical record for a specific patient."""
    patient = db.session.get(Patient, patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    data = request.get_json()
    if not data or 'diagnosis' not in data or 'treatment' not in data:
        return jsonify({'error': 'Missing diagnosis or treatment'}), 400
    new_record = MedicalRecord(patient_id=patient_id, diagnosis=data['diagnosis'],
                               treatment=data['treatment'], notes=data.get('notes'))
    db.session.add(new_record)
    db.session.commit()
    return jsonify({'message': 'Medical record added successfully'}), 201

@patientbp.route('/<int:patient_id>/medical-record',
                 methods=['GET'])
@login_required
def get_med_record(patient_id):
    """Retrieve medical records for a specific patient."""
    patient = db.session.get(Patient, patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    records = MedicalRecord.query.filter_by(patient_id=patient_id).all()
    return jsonify([record.to_dict() for record in records])

@patientbp.route('/<int:patient_id>/lab-results',
                 methods=['GET'])
@login_required
def get_lab_result(patient_id):
    """Retrieve lab results for a specific patient."""
    patient = db.session.get(Patient, patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    lab_results = LabResult.query.filter_by(patient_id=patient_id).all()
    return jsonify([result.to_dict() for result in lab_results])

@patientbp.route('/<int:patient_id>',
                 methods=['DELETE'])
@login_required
def delete_patient(patient_id):
    """Delete a specific patient by ID."""
    patient = db.session.get(Patient, patient_id)
    if patient:
        db.session.delete(patient)
        db.session.commit()
        return jsonify({'message': 'Patient deleted successfully'})
    return jsonify({'error': 'Patient not found'}), 404

@patientbp.route('/statistics', methods=['GET'])
@login_required
def get_statistics():
    """Retrieve some patient statistics (e.g., total number of patients)."""
    total_patients = Patient.query.count()
    return jsonify({'total_patients': total_patients})
