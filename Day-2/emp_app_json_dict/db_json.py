import json
import os

def read_from_file(filename='db.json'):
    if not os.path.exists(filename):
        employees=[]
        return employees
    
    with open(filename,'r') as reader:
        employees=json.load(reader)
        return employees

def write_to_file(employees, filename='db.dat'):
    with open(filename,'w') as writer:
        json.dump(employees,writer)
    