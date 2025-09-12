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
    flights=session.query(Flight).all()
    dict_flights=[]
    for flight in flights:
        flight_dict={'id':flight.id,'flight_number':flight.flight_number,'airline':flight.airline,'seats':flight.seats,'price':flight.price,'source':flight.source,'destination':flight.destination}
        dict_flights.append(flight_dict)
    logging.info("Read all flights")
    return dict_flights

def read_model_by_id(id):
    flight=session.query(Flight).filter_by(id=id).first()
    logging.info("Read flight model")
    return flight

def read_by_id(id):
    flight=read_model_by_id(id)
    if not flight:
        logging.info(f"Flight not found {id}.")
        return None
    flight_dict={'id':flight.id,'flight_number':flight.flight_number,'airline':flight.airline,'seats':flight.seats,'price':flight.price,'source':flight.source,'destination':flight.destination}
    
    logging.info("Read flight for given id")
    return flight_dict 

def update(id, new_flight):
    flight=read_model_by_id(id)
    if not flight:
        logging.info(f"Flight not found{id}")
        return
    flight.price=new_flight['price']
    session.commit()
    logging.info("Flight price updated")
  
    
def delete_flight(id):
    flight=read_model_by_id(id)
    if not flight:
        logging.info(f"Flight not found {id}")
        return
    session.delete(flight)
    session.commit()
    logging.info("Flight deleted")