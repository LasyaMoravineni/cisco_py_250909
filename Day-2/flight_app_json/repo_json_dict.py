#CRUD (Create, Read All | Read One, Update, Delete)
#Employee App - Inmem array - dict element 
import db_json as db

file_name='flights.json'
flights = db.read_from_file(file_name) 


def create_flight(flight):
    global flights 
    flights.append(flight)
    db.write_to_file(flights,file_name)


def read_all_flights():
    return flights 


def read_by_id(id):
    for flight in flights:
        if flight['id'] == id:
            return flight 
    return None 


def update(id, new_flight):
    global flights
    I = 0
    for flight in flights:
        if flight['id'] == id:
            flights[I] = new_flight
            db.write_to_file(flights,file_name)
            break 
        I += 1
    
    
def delete_flight(id):
    global flights
    index = -1
    I = 0
    for flight in flights:
        if flight['id'] == id:
            index = I
            break 
        I += 1
    if index != -1:
        flights.pop(index)
        db.write_to_file(flights,file_name)