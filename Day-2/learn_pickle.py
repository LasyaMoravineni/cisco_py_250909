import pickle #conv python obj to byte stream and then back to obj

flight = {'id':123,'flight_number': 'I700', 'airline':'Indigo', 
          'capacity':225, 'price': 4500, 
          'source': 'Bangalore', 
          'destination':'Hyderabad'}

file_name='flight.dat'

print('Before file: ',flight)
with open(file_name,'wb') as writer:
    pickle.dump(flight,writer) #flight is written byte by byte into file
    print("Saved the flight to file")

with open(file_name,'rb') as reader:
    flight_from_file = pickle.load(reader) #byte by byte from file is read and converted as flight object
    print('Flight after read from file: ',flight_from_file)