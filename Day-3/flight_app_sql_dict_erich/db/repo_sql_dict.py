#CRUD (Create, Read All | Read One, Update, Delete)
#Employee App - SQL DB - dict element 
# creating model 
# adding to session
# committing the session

from .db_setup import session,Flight
from .log import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError    #pre-defined exceptions
from .exc import FlightNotFoundError,FlightAlreadyExistsError,DatabaseError         #custom exceptions


def create_flight(flight):
    try:
        flight_model = Flight(
        id= flight['id'],
        flight_number= flight['flight_number'],
        airline=flight['airline'],
        seats=flight['seats'],
        price=flight['price'],
        source=flight['source'],
        destination=flight['destination'])
        session.add(flight_model)
        session.commit()
        logging.info("Flight created")

    except IntegrityError as ex:
        session.rollback()
        logging.error('Duplicate flight id:%s',ex)
        raise FlightAlreadyExistsError(f"Flight id={flight['id']} already exists.")
    
    except SQLAlchemyError as ex:
        session.rollback()
        logging.error('Database error in adding flight: %s',ex)
        raise DatabaseError(f"Error in adding flight.")


def read_all_flights():
    try: 
        flights=session.query(Flight).all()
        if not flights:
            raise FlightNotFoundError("No flights found in database.")
        
        dict_flights=[]
        for flight in flights:
            flight_dict={'id':flight.id,'flight_number':flight.flight_number,'airline':flight.airline,'seats':flight.seats,'price':flight.price,'source':flight.source,'destination':flight.destination}
            dict_flights.append(flight_dict)
        logging.info("Read all flights")
        return dict_flights

    except SQLAlchemyError as ex:
        session.rollback()
        logging.error('Database error in reading flights: %s',ex)
        raise DatabaseError(f"Error in reading flights.")

def read_model_by_id(id):
    try:
        flight=session.query(Flight).filter_by(id=id).first()
        if not flight:
            logging.error(f"Flight not found {id}.")
            raise FlightNotFoundError(f"Flight id={id} not found.")
        logging.info("Read flight model")
        return flight

    except SQLAlchemyError as ex:
        logging.error("Database error while reading flight: %s", ex)
        raise DatabaseError("Error while reading flight.")

def read_by_id(id):
    try:
        flight=read_model_by_id(id)
        if not flight:
            logging.error(f"Flight not found {id}.")
            raise FlightNotFoundError(f"Flight id={id} not found.")
                        
        flight_dict={'id':flight.id,'flight_number':flight.flight_number,'airline':flight.airline,'seats':flight.seats,'price':flight.price,'source':flight.source,'destination':flight.destination}
        logging.info("Read flight for given id")
        return flight_dict 
    
    except SQLAlchemyError as ex:
        logging.error("Database error while reading flight: %s", ex)
        raise DatabaseError("Error while reading flight.")


def update(id, new_flight):
    try:
        flight=read_model_by_id(id)
        if not flight:
            logging.error(f"Flight not found{id}")
            raise FlightNotFoundError(f"Flight id={id} not found.")

        flight.price=new_flight['price']
        session.commit()
        logging.info("Flight price updated")

    except SQLAlchemyError as ex:
        session.rollback()
        logging.error('Database error while updating flight details: %s', ex)
        raise DatabaseError("Error while updating flight details.")
  
    
def delete_flight(id):
    try:
        flight=read_model_by_id(id)
        if not flight:
            logging.error(f"Flight not found {id}")
            raise FlightNotFoundError(f"Flight id={id} not found.")
        session.delete(flight)
        session.commit()
        logging.info("Flight deleted")

    except SQLAlchemyError as ex:
        session.rollback()
        logging.error('Database error while deleting flight: %s', ex)
        raise DatabaseError(f"Error while deleting flight id={flight['id']}.")
