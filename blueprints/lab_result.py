from flask import Blueprint, request, jsonify
from ..models.lab_result import LabResult
from ..models.base import db
from ..models.patient import Patient
"""Blueprint for lab result routes and controllers in the Flask application."""


lab_resultbp = Blueprint('labResult', __name__, url_prefix="lab-results")


@lab_resultbp.route('/', methods=['POST'])
def new_lab_result():
    """Create a new lab result for a patient."""
    try:
        test_name = request.form['testName']
        result = request.form['result']
        patient_full_name = request.form['patientFullName']
        notes = request.form['notes']
        performed_at = request.form['performedAt']
        # Query the patient by full name
        patient = db.session.query(Patient).filter_by(patient_full_name).first()
        if not patient:
            raise ValueError("Patient not found")
        patient_id = patient.id
    except Exception as e:
        raise e
    # TODO: Implement authentication logic and associate a user
    new_result = LabResult(
        testName=test_name,
        result=result,
        notes=notes,
        performedAt=performed_at,
        patientId=patient_id,
        patient=patient
    )
    db.session.add(new_result)
    db.session.commit()
    return jsonify({'message': f'Created a new lab result with name: \
            {test_name} for the patient {patient_full_name}'}), 201


@lab_resultbp.route('/<lab_id>', methods=['GET'])
@lab_resultbp.route('/', methods=['GET'], defaults={'id': None})
def get_lab_result(lab_id):
    """Retrieve a specific lab result by ID
    or all lab results if no ID is provided."""
    try:
        if lab_id:
            # TODO: Check authentication, then return the lab result
            pass
        else:
            # Return all lab results
            lab_results = db.session.query(LabResult).all()
            return jsonify({"Lab results": lab_results}), 200
    except Exception as e:
        return jsonify({'error': str(e)})


@lab_resultbp.route('/int:<patient_id>', methods=['POST'])
def update_lab_result(patient_id):
    """Update an existing lab result for a patient."""
    try:
        if patient_id is None or patient_id <= 0:
            raise ValueError("Invalid id")
        update_data = {
            key: request.form.get(key)
            for key in ['patientId',
                        'testName',
                        'result',
                        'notes',
                        'performedAt']
            if request.form.get(key)
        }

        if not update_data:
            raise ValueError("No values provided for update")

        patient = db.session.get(Patient, patient_id)
        for key, value in update_data.items():
            setattr(patient, key, value)
        db.session.commit()

        # Return the updated patient data
        return jsonify({'updated': {update_data, patient.fullName}}), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500


@lab_resultbp.route('/int:<lab_id>', methods=['DELETE'])
def delete_lab_result(lab_id):
    """Delete a lab result by its ID."""
    if lab_id is None or lab_id <= 0:
        raise ValueError("Invalid id")
    try:
        lab_result = db.session.get(LabResult, lab_id)
        if not lab_result:
            raise ValueError("Bad Request")
        db.session.delete(lab_result)
        db.session.commit()
        return jsonify({'message': f'Lab result with id {lab_id} \
                deleted successfully'})
    except Exception as e:
        raise e
