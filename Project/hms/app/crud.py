"""
crud.py - CRUD operations for Patient with exception handling
"""

from app.models import db, Patient
from app.logger import logger
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


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
        return patient_model.to_dict()
    except IntegrityError as ie:
        db.session.rollback()
        logger.warning(f"Duplicate patient ID {patient['id']}: {ie}")
        return {"error": f"Patient with ID {patient['id']} already exists."}
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.exception(f"Database error while creating patient: {e}")
        return {"error": "Failed to create patient due to database error."}


def read_all_patients():
    try:
        patients = db.session.query(Patient).all()
        return [patient.to_dict() for patient in patients]
    except SQLAlchemyError as e:
        logger.exception(f"Database error while reading all patients: {e}")
        return []


def read_model_by_id(patient_id):
    try:
        return db.session.query(Patient).filter_by(id=patient_id).first()
    except SQLAlchemyError as e:
        logger.exception(f"Database error while reading patient {patient_id}: {e}")
        return None


def read_by_id(patient_id):
    patient = read_model_by_id(patient_id)
    return None if not patient else patient.to_dict()


def update(patient_id, new_patient):
    try:
        patient = read_model_by_id(patient_id)
        if not patient:
            return None
        patient.name = new_patient.get("name", patient.name)
        patient.age = new_patient.get("age", patient.age)
        patient.disease = new_patient.get("disease", patient.disease)
        db.session.commit()
        return patient.to_dict()
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.exception(f"Database error while updating patient {patient_id}: {e}")
        return {"error": "Failed to update patient due to database error."}


def delete_patient(patient_id):
    try:
        patient = read_model_by_id(patient_id)
        if not patient:
            return None
        db.session.delete(patient)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.exception(f"Database error while deleting patient {patient_id}: {e}")
        return {"error": "Failed to delete patient due to database error."}
