import repo_json_dict as repo

def menu():
    message = '''
Options are:
1 - Add Flight
2 - List All Flights
3 - Read Flight By Id
4 - Update Flight Destination
5 - Delete Flight
6 - Exit 
Your Option:'''
    choice = int(input(message))
    if choice == 1:
        id = int(input('ID:'))
        flight_number = input('Flight Number:')
        airline = input('Airline:')
        seats = int(input('Seats:'))
        price = int(input('Price:'))
        source = (input('Source:'))
        destination = (input('Destination:'))

        flight = {'id':id, 'flight_number':flight_number, 'airline':airline, 
                    'seats':seats, 'price':price, 'source':source, 'destination':destination}

        repo.create_flight(flight)

        print('Flight Added Successfully.')
    elif choice == 2:
        print('List of Flights:')
        for flight in repo.read_all_flights():
            print(flight)
    elif choice == 3:
        id = int(input('ID:'))
        flight = repo.read_by_id(id)
        if flight == None:
            print('Flight not found.')
        else:
            print(flight)
    elif choice == 4:
        id = int(input('ID:'))
        flight = repo.read_by_id(id)
        if flight == None: 
            print('Flight Not Found')
        else:
            print(flight)
            destination = input('New Destination:')
            new_flight = {'id':flight['id'], 
                'flight_number':flight['flight_number'], 
                'airline':flight['airline'], 
                'seats':flight['seats'], 
                'price':flight['price'],
                'source':flight['source'],
                'destination':destination}
            repo.update(id, new_flight)
            print('Flight details updated successfully.')
    elif choice == 5:
        id = int(input('ID:'))
        flight = repo.read_by_id(id)
        if flight == None: 
            print('Flight Not Found')
        else:
            repo.delete_flight(id)
            print('Flight Deleted Succesfully.')
    elif choice == 6: 
        print('Thank you for using Application')

    return choice 

def menus():
    choice = menu()
    while choice != 6:
        choice = menu()
    
menus()