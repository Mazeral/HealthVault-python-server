from flask_login import login_required
from flask import Blueprint, request, jsonify, session
from models.patient import Patient
from models.prescription import Prescription
from models.base import db
from models.user import User


prescriptionbp = Blueprint('Prescription', __name__)


@prescriptionbp.route('/prescriptions', methods=['POST'])
def add_prescription():
    try:
        patient = db.session.query(Patient).filter(
                Patient.patient_full_name == request.form.get(
                    'patientFullName',
                    None)
                ).first()
        if not patient:
            raise ValueError("Patient doesn't exist")
        data = {
            'patientFullName': request.form['patientFullName'],
            'medication': request.form['medication'],
            'dosage': request.form['dosage'],
            'instructions': request.form.get('instructions')
                }
        new_prescription = Prescription(**data)
        db.session.add(new_prescription)
        db.session.commit()
        return jsonify({new_prescription}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@prescriptionbp.route('/prescriptions/<int:prescription_id>', methods=['GET'])
def get_prescription(prescription_id):
    try:
        if prescription_id is None or prescription_id <= 0:
            raise ValueError("No id provided")
        prescription = db.commit.get(Prescription, prescription_id)
        if not prescription:
            raise ValueError("No prescription found")
        return jsonify({prescription}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@prescriptionbp.route('/prescriptions', methods=['GET'])
def all_prescriptions():
    try:
        return jsonify({db.session.query(Prescription).all()})
    except Exception as e:
        return jsonify({'error': str(e)})


@prescriptionbp.route('/prescriptions/<int:prescription_id>', methods=['PUT'])
def update_prescription(prescription_id):
    try:
        if prescription_id is None or prescription_id <= 0:
            raise ValueError("No id provided")
        prescription = db.session.get(Prescription, prescription_id)
        if not prescription:
            raise ValueError('Prescription not found')
        data = { key: request.form.get(key)
                for key in [
                    'patientFullName',
                    'medication',
                    'dosage',
                    'instructions'
                    ]
                if request.form.get(key)
                }
        for key, value in data.items():
            setattr(prescription, key, value)
        db.session.commit()
        return jsonify({'updated': prescription})
    except Exception as e:
        return jsonify({'error': str(e)})


@prescriptionbp.route('/prescriptions/<int:prescription_id>',
                      methods=['DELETE'])
def delete_prescription(prescription_id):
    try:
        if prescription_id is None or prescription_id <= 0:
            raise ValueError("No id provided")
        prescription = db.session.get(Prescription, prescription_id)
        if not prescription:
            raise ValueError('Prescription not found')
        db.session.delete(prescription)
        db.session.commit()
        return jsonify({'message':
                        f"Prescription deleted: {prescription_id}"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@prescriptionbp.route('/my-prescriptions', methods=['GET'])
@login_required
def user_presceriptions():
    try:
        user_name = session['name']
        user = db.session.query(User).filter(
                User.name == user_name
                ).first()
        return jsonify(user.prescriptions)
    except Exception as e:
        raise e
