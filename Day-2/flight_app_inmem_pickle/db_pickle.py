import pickle
import os

def read_from_file(filename='db.dat'):
    if not os.path.exists(filename):
        flights=[]
        return flights
    
    with open(filename,'rb') as reader:
        flights=pickle.load(reader)
        return flights

def write_to_file(flights, filename='db.dat'):
    with open(filename,'wb') as writer:
        pickle.dump(flights,writer)
    