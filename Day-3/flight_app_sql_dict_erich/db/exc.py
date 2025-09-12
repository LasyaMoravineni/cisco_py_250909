class FlightException(Exception):
    pass

class FlightNotFoundError(FlightException):
    pass

class FlightAlreadyExistsError(FlightException):
    pass

class DatabaseError(FlightException):
    pass
