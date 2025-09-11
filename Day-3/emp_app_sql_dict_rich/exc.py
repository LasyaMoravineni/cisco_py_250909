class EmployeeException(Exception):
    pass

class EmployeeNotFoundError(EmployeeException):
    pass

class EmployeeAlreadyExistsError(EmployeeException):
    pass

class DatabaseError(EmployeeException):
    pass
