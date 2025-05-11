from flask import Blueprint, request, jsonify
from ..models.patient import Patient
from ..models.base import db
from ..models.medical_record import MedicalRecord
from ..models.lab_result import LabResult


patientbp = Blueprint('Patient', __name__, url_prefix='patient')


@patientbp.route('/', methods=['POST'])
def new_patient():
    try:
        create_data = {
                'fullName': request.form['fullName'],
                'sex': request.form['sex'],
                'dateOfBirth': request.form.get('dateOfBirth'),
                'phone': request.form.get('phone'),
                'email': request.form.get('email'),
                'address': request.form.get('address'),
                }
        patient = Patient(**create_data)
        db.session.add(patient)
        db.session.commit()
        return jsonify({'message': f'Patient data: {patient}'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@patientbp.route('/int:<patient_id>', methods=['GET'])
def get_patient_id(patient_id):
    try:
        patient = db.session.get(Patient, patient_id)
        if not patient:
            raise ValueError('No patient found')
        return jsonify({'patient': patient}), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 500


@patientbp.route('/patients', methods=['GET'])
def get_patients():
    try:
        patients = db.session.query(Patient).all()
        return jsonify({'data': patients}), 200
    except Exception as e:
        return jsonify({'error': str(e)})


@patientbp.route('/int:<patient_id>', methods=['POST'])
def update_patient(patient_id):
    try:
        if patient_id is None or patient_id <= 0:
            raise ValueError("No id provided")
        patient = db.session.get(Patient, patient_id)
        if not patient:
            raise ValueError('No patient found')
        # TODO add userId after implementing auth
        update_data = {
            key: request.form.get(key)
            for key in ['fullName',
                        'dateOfBirth',
                        'phone',
                        'email',
                        'address',
                        'sex',
                        'bloodGroup'
                        ]
            if request.form.get(key)
                }
        for key, value in update_data:
            setattr(patient, key, value)
            db.session.commit()
        return jsonify({'updated': update_data})
    except Exception as e:
        return jsonify({'error': str(e)})


@patientbp.route('/<int:patient_id>/medical_record',
                 methods=['POST'])
def add_record(patient_id):
    try:
        if patient_id is None or patient_id <= 0:
            raise ValueError("Patient id not provided ")
        if not db.session.get(Patient, patient_id):
            raise ValueError("Patient not found")
        data = {
                'patientId': patient_id,
                'diagnosis': request.form['diagnosis'],
                'notes': request.form.get('notes')
                }
        new_record = MedicalRecord(**data)
        db.session.add(new_record)
        db.commit()
        return jsonify({'message': f'Created a medical record for \
                patient: with id {patient_id}'}), 201
    except Exception as e:
        return jsonify({'error': str(e)})


@patientbp.route('/<int:patient_id>/medical-record',
                 methods=['GET'])
def get_med_record(patient_id):
    try:
        if patient_id is None or patient_id <= 0:
            raise ValueError("Patient id not provided ")
        if not db.session.get(Patient, patient_id):
            raise ValueError("Patient not found")
        medical_records = db.sesion.query(MedicalRecord).filter(
                MedicalRecord.patientId == patient_id
                )
        return jsonify({'Medical Record': medical_records}), 200
    except Exception as e:
        return jsonify({'error': str(e)})



@patientbp.route('/<int:patient_id>/lab-results',
                 methods=['GET'])
def get_lab_result(patient_id):
    try:
        if patient_id is None or patient_id <= 0:
            raise ValueError("Patient id not provided ")
        if not db.session.get(Patient, patient_id):
            raise ValueError("Patient not found")
        lab_results = db.sesion.query(LabResult).filter(
                LabResult.patientId == patient_id
                )
        return jsonify({'Lab result': lab_results}), 200
    except Exception as e:
        return jsonify({'error': str(e)})


@patientbp.route('/<int:patient_id>',
                 methods=['DELETE'])
def delete_patient(patient_id):
    try:
        if patient_id is None or patient_id <= 0:
            raise ValueError("Patient id not provided ")
        patient = db.session.get(Patient, patient_id):
        if not patient
            raise ValueError("Patient not found")
        db.session.delete(patient)
        db.session.commit()
        return jsonify({'message': f'Patient with id: {patient_id} deleted'})
    except Exception as e:
        return jsonify({'error': str(e)})


@patientbp.route('/statistics', methods=['GET'])
def get_statistics():
    """
    Calculates and returns the number of patients created today, this month, and this year.
    """
    try:
        today = datetime.utcnow().date()

        # Calculate today's count
        start_of_day = datetime(today.year, today.month, today.day, 0, 0, 0)
        end_of_day = datetime(today.year,
                              today.month,
                              today.day,
                              23, 59, 59, 999999)
        today_count = db.session.query(Patient)
        .filter(Patient.createdAt >= start_of_day,
                Patient.createdAt <= end_of_day).count()

        # Calculate monthly count
        start_of_month = datetime(today.year, today.month, 1, 0, 0, 0)
        next_month = today.month + 1
        year_of_next_month = today.year
        if next_month > 12:
            next_month = 1
            year_of_next_month += 1
        end_of_month = datetime(year_of_next_month,
                                next_month,
                                1, 0, 0, 0) - timedelta(seconds=1)
        monthly_count = db.session.query(Patient)
        .filter(Patient.createdAt >= start_of_month,
                Patient.createdAt <= end_of_month).count()

        # Calculate yearly count
        start_of_year = datetime(today.year, 1, 1, 0, 0, 0)
        end_of_year = datetime(today.year, 12, 31, 23, 59, 59, 999999)
        yearly_count = db.session.query(Patient)
        .filter(Patient.createdAt >= start_of_year,
                Patient.createdAt <= end_of_year).count()

        return jsonify({
            'today': today_count,
            'monthly': monthly_count,
            'yearly': yearly_count
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
