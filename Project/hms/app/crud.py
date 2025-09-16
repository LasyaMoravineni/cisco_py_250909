"""
crud.py - CRUD operations for Patient
"""

from app.models import db, Patient


def create_patient(patient):
    patient_model = Patient(
        id=patient["id"],
        name=patient["name"],
        age=patient["age"],
        disease=patient["disease"],
    )
    db.session.add(patient_model)
    db.session.commit()


def read_all_patients():
    patients = db.session.query(Patient).all()
    return [patient.to_dict() for patient in patients]


def read_model_by_id(patient_id):
    return db.session.query(Patient).filter_by(id=patient_id).first()


def read_by_id(patient_id):
    patient = read_model_by_id(patient_id)
    return None if not patient else patient.to_dict()


def update(patient_id, new_patient):
    patient = read_model_by_id(patient_id)
    if not patient:
        return None
    patient.name = new_patient["name"]
    patient.age = new_patient["age"]
    patient.disease = new_patient["disease"]
    db.session.commit()
    return patient.to_dict()


def delete_patient(patient_id):
    patient = read_model_by_id(patient_id)
    if not patient:
        return None
    db.session.delete(patient)
    db.session.commit()
    return True
