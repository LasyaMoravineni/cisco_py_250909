from hms.app.models import Patient
from hms.app.db import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from hms.app.exceptions import PatientNotFoundError, DatabaseError
from hms.app.logger import logger


def create_patient(patient):
    try:
        patient_model = Patient(
            id=patient["id"],
            name=patient["name"],
            age=patient["age"],
            disease=patient["disease"],
        )
        db.session.add(patient_model)
        db.session.commit()
        logger.info(f"Patient created: {patient}")
        return patient_model.to_dict()
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Duplicate patient ID {patient['id']} - {e}")
        raise DatabaseError(f"Patient with ID {patient['id']} already exists")
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error while creating patient: {e}")
        raise DatabaseError(str(e))


def read_all_patients():
    try:
        patients = db.session.query(Patient).all()
        logger.info(f"Read all patients, count: {len(patients)}")
        return [patient.to_dict() for patient in patients]
    except SQLAlchemyError as e:
        logger.error(f"Database error while reading all patients: {e}")
        raise DatabaseError(str(e))


def read_model_by_id(patient_id):
    try:
        return db.session.query(Patient).filter_by(id=patient_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error while reading patient {patient_id}: {e}")
        raise DatabaseError(str(e))


def read_by_id(patient_id):
    patient = read_model_by_id(patient_id)
    if not patient:
        logger.error(f"Patient {patient_id} not found")
        raise PatientNotFoundError(patient_id)
    return patient.to_dict()


def update(patient_id, new_patient):
    patient = read_model_by_id(patient_id)
    if not patient:
        logger.error(f"Patient {patient_id} not found for update")
        raise PatientNotFoundError(patient_id)
    try:
        patient.name = new_patient["name"]
        patient.age = new_patient["age"]
        patient.disease = new_patient["disease"]
        db.session.commit()
        logger.info(f"Patient {patient_id} updated: {new_patient}")
        return patient.to_dict()
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error while updating patient {patient_id}: {e}")
        raise DatabaseError(str(e))


def delete_patient(patient_id):
    patient = read_model_by_id(patient_id)
    if not patient:
        logger.error(f"Patient {patient_id} not found for deletion")
        raise PatientNotFoundError(patient_id)
    try:
        db.session.delete(patient)
        db.session.commit()
        logger.info(f"Patient {patient_id} deleted")
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error while deleting patient {patient_id}: {e}")
        raise DatabaseError(str(e))
