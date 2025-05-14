# mock_data.py (Modified)

import sys
from pathlib import Path

# Add the parent directory to sys.path to help with absolute imports
# (Still good practice when running standalone scripts)
sys.path.append(str(Path(__file__).parent))

import random
from datetime import date, timedelta
from faker import Faker
from werkzeug.security import generate_password_hash

# Import the application factory and db instance
from app import create_app
from models.base import db # db instance is needed for db operations

# Import your models (use absolute imports relative to project root)
from models.user import User, Role
from models.patient import Patient, Sex, BloodGroup
from models.medical_record import MedicalRecord
from models.prescription import Prescription
from models.lab_result import LabResult

# Initialize Faker
fake = Faker()

# Constants for the number of samples
NUM_USERS = 20  # Total users, including the 2 specific ones
NUM_PATIENTS = 100
NUM_MEDICAL_RECORDS_PER_PATIENT = 3
NUM_PRESCRIPTIONS_PER_PATIENT = 3
NUM_LAB_RESULTS_PER_PATIENT = 3

# Python Role Enum values (ensure these match your model)
USER_ROLES = [Role.ADMIN, Role.USER]


def create_users():
    """Creates and inserts mock users into the database."""
    print("Creating users...")
    users_to_add = [] # Use a list to batch adds

    # Ensure 'mohamad' (admin) and 'mamdoh' (user/doctor) are created first for predictability
    # Check if they already exist to avoid duplicates if script is run multiple times
    # Use db.session.get() or query for existing
    mohamad = User.query.filter_by(email="mohamad@example.com").first()
    if not mohamad:
        mohamad = User(
            name="mohamad",
            email="mohamad@example.com",
            password_hash=generate_password_hash("0000"),
            role=Role.ADMIN,
            createdAt=date.today(),
            updatedAt=date.today()
        )
        users_to_add.append(mohamad)

    mamdoh = User.query.filter_by(email="mamdoh@example.com").first()
    if not mamdoh:
        mamdoh = User(
            name="mamdoh",
            email="mamdoh@example.com",
            password_hash=generate_password_hash("0000"),
            role=Role.USER, # Assuming 'USER' can represent a doctor role
            createdAt=date.today(),
            updatedAt=date.today()
        )
        users_to_add.append(mamdoh)

    # Create additional fake users if needed to reach NUM_USERS
    # Check the *total* number of users after potentially adding specific ones
    current_user_count = db.session.query(User).count() # Use db.session.query().count()
    for _ in range(max(0, NUM_USERS - current_user_count)):
        user = User(
            name=fake.unique.user_name(),
            email=fake.unique.email(),
            password_hash=generate_password_hash(fake.password()),
            role=random.choice(USER_ROLES),
            createdAt=fake.date_between(start_date="-2y", end_date="today"), # Ensure date objects
            updatedAt=fake.date_between(start_date="-1y", end_date="today") # Ensure date objects
        )
        users_to_add.append(user)

    if users_to_add:
        db.session.add_all(users_to_add)
        db.session.commit()
        print(f"{len(users_to_add)} new users created.")
    else:
        print("Specific users might already exist. No new users created.")

    # Return all users currently in the database
    return User.query.all()


def create_patients(users):
    """Creates and inserts mock patients, associating them with a specific user."""
    print("Creating patients...")
    if not users:
        print("No users found to associate patients with. Aborting patient creation.")
        return []

    # Find the "mamdoh" user to associate patients with
    doctor_user = next((user for user in users if user.name == "mamdoh"), None)

    if not doctor_user:
        print("Could not find a suitable user to be the doctor ('mamdoh'). Aborting patient creation.")
        return []

    print(f"Assigning patients to user: {doctor_user.name} (ID: {doctor_user.id})")

    patients_to_create = []
    current_patient_count = db.session.query(Patient).filter_by(user_id=doctor_user.id).count()

    for _ in range(max(0, NUM_PATIENTS - current_patient_count)):
        patient = Patient(
            fullName=fake.unique.name(),
            dateOfBirth=fake.date_of_birth(minimum_age=1, maximum_age=90), # Ensure date object
            phone=fake.phone_number(),
            email=fake.unique.email(),
            address=fake.address(),
            sex=random.choice(list(Sex)),
            bloodGroup=random.choice(list(BloodGroup)),
            user_id=doctor_user.id,
            createdAt=fake.date_between(start_date="-5y", end_date="today"), # Ensure date object
            updatedAt=fake.date_between(start_date="-1y", end_date="today") # Ensure date object
        )
        patients_to_create.append(patient)

    if patients_to_create:
        db.session.add_all(patients_to_create)
        db.session.commit()
        print(f"{len(patients_to_create)} patients created for user {doctor_user.name}.")
    else:
        print(f"User {doctor_user.name} already has {current_patient_count} patients. No new patients created.")

    # Return all patients linked to this user
    return Patient.query.filter_by(user_id=doctor_user.id).all()


def create_medical_records(patients):
    """Creates mock medical records for the given patients."""
    print("Creating medical records...")
    if not patients:
        print("No patients found to create medical records for.")
        return

    medical_records_to_create = []
    for patient in patients:
        if not patient.user_id:
            print(f"Patient {patient.id} missing user_id. Skipping medical records.")
            continue

        # Create a fixed number per patient if they don't exist
        current_records_count = db.session.query(MedicalRecord).filter_by(patientId=patient.id).count()
        for _ in range(max(0, NUM_MEDICAL_RECORDS_PER_PATIENT - current_records_count)):
            record = MedicalRecord(
                patientId=patient.id,
                diagnosis=fake.bs(),
                notes=fake.paragraph(nb_sentences=2),
                userId=patient.user_id, # Associate with the patient's primary doctor/user
                createdAt=fake.date_between(start_date=patient.createdAt, end_date="today"), # Ensure date object
                updatedAt=fake.date_between(start_date=patient.createdAt, end_date="today") # Ensure date object
            )
            medical_records_to_create.append(record)

    if medical_records_to_create:
        db.session.add_all(medical_records_to_create)
        db.session.commit()
        print(f"{len(medical_records_to_create)} medical records created.")
    else:
        print("No new medical records to create.")


def create_prescriptions(patients):
    """Creates mock prescriptions for the given patients."""
    print("Creating prescriptions...")
    if not patients:
        print("No patients found to create prescriptions for.")
        return

    prescriptions_to_create = []
    for patient in patients:
        if not patient.user_id:
            print(f"Patient {patient.id} missing user_id. Skipping prescriptions.")
            continue

        current_prescriptions_count = db.session.query(Prescription).filter_by(patientId=patient.id).count()
        for _ in range(max(0, NUM_PRESCRIPTIONS_PER_PATIENT - current_prescriptions_count)):
            prescription = Prescription(
                patientId=patient.id,
                medication=fake.word().capitalize() + " " + fake.word(),
                dosage=f"{random.randint(1, 3)} pills, {random.randint(1, 4)} times a day",
                instructions=fake.sentence(),
                prescribedAt=fake.date_between(start_date=patient.createdAt, end_date="today"), # Ensure date object
                userId=patient.user_id
            )
            prescriptions_to_create.append(prescription)

    if prescriptions_to_create:
        db.session.add_all(prescriptions_to_create)
        db.session.commit()
        print(f"{len(prescriptions_to_create)} prescriptions created.")
    else:
        print("No new prescriptions to create.")


def create_lab_results(patients):
    """Creates mock lab results for the given patients."""
    print("Creating lab results...")
    if not patients:
        print("No patients found to create lab results for.")
        return

    lab_results_to_create = []
    for patient in patients:
        if not patient.user_id:
            print(f"Patient {patient.id} missing user_id. Skipping lab results.")
            continue

        current_lab_results_count = db.session.query(LabResult).filter_by(patientId=patient.id).count()
        for _ in range(max(0, NUM_LAB_RESULTS_PER_PATIENT - current_lab_results_count)):
            lab_result = LabResult(
                patientId=patient.id,
                testName=fake.catch_phrase(),
                result=f"{random.uniform(1.0, 100.0):.2f} " + fake.word(),
                notes=fake.paragraph(nb_sentences=1),
                performedAt=fake.date_between(start_date=patient.createdAt, end_date="today"), # Ensure date object
                createdAt=fake.date_between(start_date=patient.createdAt, end_date="today"), # Ensure date object
                userId=patient.user_id
            )
            lab_results_to_create.append(lab_result)

    if lab_results_to_create:
        db.session.add_all(lab_results_to_create)
        db.session.commit()
        print(f"{len(lab_results_to_create)} lab results created.")
    else:
        print("No new lab results to create.")


def seed_database():
    """Main function to generate all mock data."""
    # This function is now called WITHIN the app_context() block in __main__
    print("Starting database seeding...")

    # Clear existing data (optional, be careful with this)
    # print("Clearing existing data...")
    # db.session.query(MedicalRecord).delete()
    # db.session.query(Prescription).delete()
    # db.session.query(LabResult).delete()
    # db.session.query(Patient).delete()
    # db.session.query(User).delete()
    # db.session.commit()
    # print("Existing data cleared.")

    # Step 1: Create Users
    # This function now commits and returns users *within* the context
    all_users = create_users()

    # Step 2: Create Patients, ensuring they are linked to a user (e.g., "mamdoh")
    created_patients = create_patients(all_users)

    if created_patients:
        # Step 3-5: Create related data for these patients
        create_medical_records(created_patients)
        create_prescriptions(created_patients)
        create_lab_results(created_patients)
    else:
        print("Skipping creation of medical records, prescriptions, and lab results as no patients were created/found.")

    print("Mock data generation completed successfully!")


# This allows running the script directly: python mock_data.py
if __name__ == "__main__":
    app = create_app() # Create the app instance
    with app.app_context(): # Establish the application context
        # *** Add this line to create tables if they don't exist ***
        db.create_all()
        # ********************************************************

        seed_database() # Run the seeding function within the context
