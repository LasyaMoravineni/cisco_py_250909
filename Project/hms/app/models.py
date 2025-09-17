"""
models.py - SQLAlchemy models for the Hospital Management System (HMS).
"""

from hms.app.db import db


class Patient(db.Model):
    """
    Patient model representing a hospital patient.

    Attributes:
        id (int): Primary key, unique identifier for the patient.
        name (str): Patient's full name.
        age (int): Patient's age.
        disease (str): Disease/condition diagnosed for the patient.
    """

    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    disease = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        """Return string representation of the patient object."""
        return (
            f"<Patient id={self.id}, name={self.name}, "
            f"age={self.age}, disease={self.disease}>"
        )

    def to_dict(self):
        """
        Convert the Patient object into a dictionary.

        Returns:
            dict: Patient details with keys `id`, `name`, `age`, `disease`.
        """
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "disease": self.disease,
        }
