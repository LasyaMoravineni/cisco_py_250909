class HMSException(Exception):
    """Base exception class for Hospital Management System"""
    pass


class PatientNotFoundError(HMSException):
    """Raised when a patient with the given ID is not found"""
    def __init__(self, patient_id):
        super().__init__(f"Patient with ID {patient_id} not found.")


class DatabaseError(HMSException):
    """Raised when there is a database-related error"""
    def __init__(self, message="Database operation failed"):
        super().__init__(message)


class EmailError(HMSException):
    """Raised when email sending fails"""
    def __init__(self, message="Failed to send email notification"):
        super().__init__(message)
