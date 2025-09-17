"""
crud.py - CRUD operations for Patient model.
Handles database interactions with proper logging and custom exceptions.
"""

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from hms.app.db import db
from hms.app.models import Patient
from hms.app.exceptions import PatientNotFoundError, DatabaseError
from hms.app.logger import logger


def create_patient(patient):
    """
    Create a new patient record.

    Args:
        patient (dict): Patient data with keys id, name, age, disease.

    Returns:
        dict: The created patient record as a dictionary.

    Raises:
        DatabaseError: If there is a database issue or duplicate ID.
    """
    try:
        patient_model = Patient(
            id=patient["id"],
            name=patient["name"],
            age=patient["age"],
            disease=patient["disease"],
        )
        db.session.add(patient_model)
        db.session.commit()
        logger.info("Patient created: %s", patient)
        return patient_model.to_dict()
    except IntegrityError as e:
        db.session.rollback()
        logger.error("Duplicate patient ID %s - %s", patient["id"], e)
        raise DatabaseError(
            f"Patient with ID {patient['id']} already exists"
        ) from e
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Database error while creating patient: %s", e)
        raise DatabaseError(str(e)) from e


def read_all_patients():
    """
    Retrieve all patients from the database.

    Returns:
        list[dict]: A list of patient records.

    Raises:
        DatabaseError: If a database error occurs.
    """
    try:
        patients = db.session.query(Patient).all()
        logger.info("Read all patients, count: %d", len(patients))
        return [patient.to_dict() for patient in patients]
    except SQLAlchemyError as e:
        logger.error("Database error while reading all patients: %s", e)
        raise DatabaseError(str(e)) from e


def read_model_by_id(patient_id):
    """
    Fetch a Patient SQLAlchemy model instance by ID.

    Args:
        patient_id (int): The patient ID.

    Returns:
        Patient | None: Patient model if found, else None.

    Raises:
        DatabaseError: If a database error occurs.
    """
    try:
        return db.session.query(Patient).filter_by(id=patient_id).first()
    except SQLAlchemyError as e:
        logger.error("Database error while reading patient %s: %s", patient_id, e)
        raise DatabaseError(str(e)) from e


def read_by_id(patient_id):
    """
    Retrieve a patient by ID.

    Args:
        patient_id (int): The patient ID.

    Returns:
        dict: Patient record as a dictionary.

    Raises:
        PatientNotFoundError: If no patient is found with the given ID.
    """
    patient = read_model_by_id(patient_id)
    if not patient:
        logger.error("Patient %s not found", patient_id)
        raise PatientNotFoundError(patient_id)
    return patient.to_dict()


def update(patient_id, new_patient):
    """
    Update a patient record.

    Args:
        patient_id (int): The ID of the patient to update.
        new_patient (dict): Updated patient data.

    Returns:
        dict: Updated patient record.

    Raises:
        PatientNotFoundError: If the patient is not found.
        DatabaseError: If a database error occurs.
    """
    patient = read_model_by_id(patient_id)
    if not patient:
        logger.error("Patient %s not found for update", patient_id)
        raise PatientNotFoundError(patient_id)
    try:
        patient.name = new_patient["name"]
        patient.age = new_patient["age"]
        patient.disease = new_patient["disease"]
        db.session.commit()
        logger.info("Patient %s updated: %s", patient_id, new_patient)
        return patient.to_dict()
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Database error while updating patient %s: %s", patient_id, e)
        raise DatabaseError(str(e)) from e


def delete_patient(patient_id):
    """
    Delete a patient record.

    Args:
        patient_id (int): The ID of the patient to delete.

    Returns:
        bool: True if deleted successfully.

    Raises:
        PatientNotFoundError: If the patient does not exist.
        DatabaseError: If a database error occurs.
    """
    patient = read_model_by_id(patient_id)
    if not patient:
        logger.error("Patient %s not found for deletion", patient_id)
        raise PatientNotFoundError(patient_id)
    try:
        db.session.delete(patient)
        db.session.commit()
        logger.info("Patient %s deleted", patient_id)
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Database error while deleting patient %s: %s", patient_id, e)
        raise DatabaseError(str(e)) from e
