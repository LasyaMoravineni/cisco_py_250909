"""
routes.py - Flask routes for Hospital Management System (Patients CRUD)
"""

from flask import Flask, request, jsonify
from datetime import datetime
import app.crud as crud
from app.db import init_db
import app.emailer as emailer

application = Flask(__name__)
init_db(application)


@application.route("/patients", methods=['POST'])
def create_patient():
    patient_dict = request.json
    crud.create_patient(patient_dict)
    saved_patient = crud.read_by_id(patient_dict["id"])

    # Send email notification
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"{now} Patient {patient_dict['name']} Created"
    body = f"""
    Patient created successfully.

    id : {patient_dict['id']}
    name : {patient_dict['name']}
    age : {patient_dict['age']}
    disease : {patient_dict['disease']}
    """
    emailer.send_email(emailer.TO_ADDRESS, subject, body)

    return jsonify(saved_patient)


@application.route("/patients", methods=['GET'])
def read_all_patients():
    return jsonify(crud.read_all_patients())


@application.route("/patients/<int:patient_id>", methods=['GET'])
def read_patient_by_id(patient_id):
    patient = crud.read_by_id(patient_id)
    if not patient:
        return jsonify({"error": f"Patient with id {patient_id} not found"}), 404
    return jsonify(patient)


@application.route("/patients/<int:patient_id>", methods=['PUT'])
def update_patient(patient_id):
    patient_dict = request.json
    updated_patient = crud.update(patient_id, patient_dict)
    if not updated_patient:
        return jsonify({"error": f"Patient with id {patient_id} not found"}), 404
    return jsonify(updated_patient)


@application.route("/patients/<int:patient_id>", methods=['DELETE'])
def delete_patient(patient_id):
    deleted = crud.delete_patient(patient_id)
    if not deleted:
        return jsonify({"error": f"Patient with id {patient_id} not found"}), 404
    return jsonify({"message": "Deleted Successfully"})
