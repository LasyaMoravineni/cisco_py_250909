"""
routes.py - Flask routes for Hospital Management System (Patients CRUD)
Handles patient creation, reading, updating, and deletion
with proper exception handling and logging.
"""

from datetime import datetime

from flask import Flask, request, jsonify

from app import crud, emailer
from app.db import init_db
from app.exceptions import PatientNotFoundError, DatabaseError, EmailError
from app.logger import logger

application = Flask(__name__)
init_db(application)


@application.route("/patients", methods=["POST"])
def create_patient():
    """Create a new patient and send an email notification."""
    try:
        patient_dict = request.json
        saved_patient = crud.create_patient(patient_dict)

        # Send email notification
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subject = f"{now} Patient {patient_dict['name']} Created"
        body = (
            f"Patient created successfully.\n\n"
            f"id : {patient_dict['id']}\n"
            f"name : {patient_dict['name']}\n"
            f"age : {patient_dict['age']}\n"
            f"disease : {patient_dict['disease']}\n"
        )
        try:
            emailer.send_email(emailer.TO_ADDRESS, subject, body)
        except EmailError as e:
            logger.error(f"Email sending failed: {e}")

        return jsonify(saved_patient)

    except DatabaseError as e:
        logger.error(f"Database error in create_patient: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error in create_patient: {e}")
        return jsonify({"error": "Internal server error"}), 500


@application.route("/patients", methods=["GET"])
def read_all_patients():
    """Return a list of all patients."""
    try:
        patients = crud.read_all_patients()
        return jsonify(patients)
    except DatabaseError as e:
        logger.error(f"Database error in read_all_patients: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error in read_all_patients: {e}")
        return jsonify({"error": "Internal server error"}), 500


@application.route("/patients/<int:patient_id>", methods=["GET"])
def read_patient_by_id(patient_id):
    """Return patient details by ID."""
    try:
        patient = crud.read_by_id(patient_id)
        return jsonify(patient)
    except PatientNotFoundError as e:
        logger.error(f"Patient not found: {e}")
        return jsonify({"error": str(e)}), 404
    except DatabaseError as e:
        logger.error(f"Database error in read_patient_by_id: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error in read_patient_by_id: {e}")
        return jsonify({"error": "Internal server error"}), 500


@application.route("/patients/<int:patient_id>", methods=["PUT"])
def update_patient(patient_id):
    """Update an existing patient's details."""
    try:
        patient_dict = request.json
        updated_patient = crud.update(patient_id, patient_dict)
        return jsonify(updated_patient)
    except PatientNotFoundError as e:
        logger.error(f"Patient not found: {e}")
        return jsonify({"error": str(e)}), 404
    except DatabaseError as e:
        logger.error(f"Database error in update_patient: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error in update_patient: {e}")
        return jsonify({"error": "Internal server error"}), 500


@application.route("/patients/<int:patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    """Delete a patient by ID."""
    try:
        crud.delete_patient(patient_id)
        return jsonify({"message": "Deleted Successfully"})
    except PatientNotFoundError as e:
        logger.error(f"Patient not found: {e}")
        return jsonify({"error": str(e)}), 404
    except DatabaseError as e:
        logger.error(f"Database error in delete_patient: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.error(f"Unexpected error in delete_patient: {e}")
        return jsonify({"error": "Internal server error"}), 500
