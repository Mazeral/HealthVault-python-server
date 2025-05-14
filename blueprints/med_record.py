from flask_login import login_required
from flask import Blueprint, request, jsonify, session
from ..models.medical_record import MedicalRecord
from ..models.base import db
from ..models.patient import Patient

"""Blueprint for medical record routes and controllers
in the Flask application."""

med_recordbp = Blueprint('MedRecord', __name__, url_prefix='medical_record')


@med_recordbp.route('/', methods=['GET'])
@login_required
def new_record():
    """Create a new medical record for a patient."""
    try:
        patient_id = request.form['patientId']
        diagnosis = request.form['diagnosis']
        notes = request.form['notes']

        # use get if using a unique key, else query
        patient = db.session.get(Patient, patient_id)
        if not patient:
            raise ValueError("No patient found")
        new_record = MedicalRecord(diagnosis=diagnosis,
                                   notes=notes,
                                   patientId=patient_id,
                                   userId=session.get('id')
                                   )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({'message': f"Created new medical record for patient \
                {patient.name}"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@med_recordbp.route('/int:<med_id>', methods=['POST'])
@login_required
def update_record(med_id):
    """Update an existing medical record for a patient."""
    try:
        if not med_id:
            raise ValueError("Error in id")
        update_data = {
                key: for key in [
                    'diagnosis',
                    'notes',
                    'patient_id',
                    'patient'
                    ]
            'diagnosis': request.form['diagnosis'],
            'notes': request.form['notes'],
            'patientId': request.form['patientId'],
            'patientFullName': request.form['patientFullName']
        }
        record = db.session.get(MedicalRecord, med_id)
        for key, value in update_data.items():
            setattr(record, key, value)
        db.session.commit()
        return jsonify({'message': f'updated record successfully with \
                data: f{update_data}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@med_recordbp.route('/int:<med_id>', methods=['GET'])
@login_required
def get_record(med_id):
    """Retrieve a specific medical record by ID or all medical records
    if no ID is provided."""
    try:
        if med_id is None or med_id <= 0:
            raise ValueError("No id provided")
        record = db.session.get(MedicalRecord, med_id)
        if not record:
            raise ValueError("Medical record not found")
        return jsonify({'Medical Record': record}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@med_recordbp.route('/int:<med_id>', methods=['DELETE'])
@login_required
def del_record(med_id):
    """Delete a medical record by its ID."""
    if med_id is None or med_id <= 0:
        raise ValueError("No id provided")
    try:
        record = db.session.get(MedicalRecord, med_id)
        if not record:
            raise ValueError("Medical record not found")
        db.session.delete(record)
        db.session.commit()
        return jsonify({'message': f'Deleted medical record with if: {med_id}'})
    except ValueError as ve:
        return jsonify({'error': f'{str(ve)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
