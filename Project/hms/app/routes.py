"""
routes.py - Flask routes for Hospital Management System (Patients CRUD)
with exception handling and logging
"""

from flask import Flask, request, jsonify
from datetime import datetime
import app.crud as crud
from app.db import init_db
import app.emailer as emailer
from app.logger import logger

application = Flask(__name__)
init_db(application)


@application.route("/patients", methods=['POST'])
def create_patient():
    try:
        patient_dict = request.json
        result = crud.create_patient(patient_dict)

        if "error" in result:
            return jsonify(result), 400

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
        try:
            emailer.send_email(emailer.TO_ADDRESS, subject, body)
        except Exception as e:
            logger.warning(f"Email sending failed for patient {patient_dict['id']}: {e}")

        return jsonify(saved_patient)
    except Exception as e:
        logger.exception("Unexpected error in create_patient route")
        return jsonify({"error": "Failed to create patient"}), 500


@application.route("/patients", methods=['GET'])
def read_all_patients():
    try:
        patients = crud.read_all_patients()
        return jsonify(patients)
    except Exception as e:
        logger.exception("Unexpected error in read_all_patients route")
        return jsonify({"error": "Failed to fetch patients"}), 500


@application.route("/patients/<int:patient_id>", methods=['GET'])
def read_patient_by_id(patient_id):
    try:
        patient = crud.read_by_id(patient_id)
        if not patient:
            return jsonify({"error": f"Patient with id {patient_id} not found"}), 404
        return jsonify(patient)
    except Exception as e:
        logger.exception(f"Unexpected error in read_patient_by_id route for {patient_id}")
        return jsonify({"error": "Failed to fetch patient"}), 500


@application.route("/patients/<int:patient_id>", methods=['PUT'])
def update_patient(patient_id):
    try:
        patient_dict = request.json
        updated_patient = crud.update(patient_id, patient_dict)
        if not updated_patient:
            return jsonify({"error": f"Patient with id {patient_id} not found"}), 404
        if "error" in updated_patient:
            return jsonify(updated_patient), 400
        return jsonify(updated_patient)
    except Exception as e:
        logger.exception(f"Unexpected error in update_patient route for {patient_id}")
        return jsonify({"error": "Failed to update patient"}), 500


@application.route("/patients/<int:patient_id>", methods=['DELETE'])
def delete_patient(patient_id):
    try:
        deleted = crud.delete_patient(patient_id)
        if not deleted:
            return jsonify({"error": f"Patient with id {patient_id} not found"}), 404
        if isinstance(deleted, dict) and "error" in deleted:
            return jsonify(deleted), 400
        return jsonify({"message": "Deleted Successfully"})
    except Exception as e:
        logger.exception(f"Unexpected error in delete_patient route for {patient_id}")
        return jsonify({"error": "Failed to delete patient"}), 500
