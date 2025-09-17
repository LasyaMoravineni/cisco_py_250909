"""
routes.py - Flask routes for Hospital Management System (Patients CRUD).

This module defines API endpoints for:
- Creating, reading, updating, and deleting patients.
- Sending email notifications on patient creation.
- Scraping external medical news.
- Logging and centralized exception handling.
"""

from datetime import datetime

from flask import Flask, request, jsonify

from hms.app import crud, emailer
from hms.app.db import init_db
from hms.app.exceptions import PatientNotFoundError, DatabaseError, EmailError
from hms.app.logger import logger
from hms.app.scraper import scrape_medical_news


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
        except EmailError as err:
            logger.error("Email sending failed: %s", err)

        return jsonify(saved_patient)

    except DatabaseError as err:
        logger.error("Database error in create_patient: %s", err)
        return jsonify({"error": str(err)}), 400
    except Exception as err:  # pylint: disable=broad-exception-caught
        logger.error("Unexpected error in create_patient: %s", err)
        return jsonify({"error": "Internal server error"}), 500


@application.route("/patients", methods=["GET"])
def read_all_patients():
    """Return a list of all patients."""
    try:
        patients = crud.read_all_patients()
        return jsonify(patients)
    except DatabaseError as err:
        logger.error("Database error in read_all_patients: %s", err)
        return jsonify({"error": str(err)}), 500
    except Exception as err:  # pylint: disable=broad-exception-caught
        logger.error("Unexpected error in read_all_patients: %s", err)
        return jsonify({"error": "Internal server error"}), 500


@application.route("/patients/<int:patient_id>", methods=["GET"])
def read_patient_by_id(patient_id):
    """Return patient details by ID."""
    try:
        patient = crud.read_by_id(patient_id)
        return jsonify(patient)
    except PatientNotFoundError as err:
        logger.error("Patient not found: %s", err)
        return jsonify({"error": str(err)}), 404
    except DatabaseError as err:
        logger.error("Database error in read_patient_by_id: %s", err)
        return jsonify({"error": str(err)}), 500
    except Exception as err:  # pylint: disable=broad-exception-caught
        logger.error("Unexpected error in read_patient_by_id: %s", err)
        return jsonify({"error": "Internal server error"}), 500


@application.route("/news", methods=["GET"])
def get_news():
    """Return scraped medical news articles as JSON."""
    try:
        news = scrape_medical_news()
        return jsonify(news)
    except Exception as err:  # pylint: disable=broad-exception-caught
        logger.error("Unexpected error in get_news: %s", err)
        return jsonify({"error": str(err)}), 500


@application.route("/patients/<int:patient_id>", methods=["PUT"])
def update_patient(patient_id):
    """Update an existing patient's details."""
    try:
        patient_dict = request.json
        updated_patient = crud.update(patient_id, patient_dict)
        return jsonify(updated_patient)
    except PatientNotFoundError as err:
        logger.error("Patient not found: %s", err)
        return jsonify({"error": str(err)}), 404
    except DatabaseError as err:
        logger.error("Database error in update_patient: %s", err)
        return jsonify({"error": str(err)}), 500
    except Exception as err:  # pylint: disable=broad-exception-caught
        logger.error("Unexpected error in update_patient: %s", err)
        return jsonify({"error": "Internal server error"}), 500


@application.route("/patients/<int:patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    """Delete a patient by ID."""
    try:
        crud.delete_patient(patient_id)
        return jsonify({"message": "Deleted Successfully"})
    except PatientNotFoundError as err:
        logger.error("Patient not found: %s", err)
        return jsonify({"error": str(err)}), 404
    except DatabaseError as err:
        logger.error("Database error in delete_patient: %s", err)
        return jsonify({"error": str(err)}), 500
    except Exception as err:  # pylint: disable=broad-exception-caught
        logger.error("Unexpected error in delete_patient: %s", err)
        return jsonify({"error": "Internal server error"}), 500
