from flask import Flask, request, jsonify 
from datetime import datetime
import app.crud as crud 
from app.config import config 
import app.mail as mail 
application = Flask(__name__)

# db conn str
application.config['SQLALCHEMY_DATABASE_URI'] = config['DB_URL']
application.config['SQLALCHEMY_ECHO'] = True 

crud.db.init_app(application) #app to db configuration update

# create tables 
with application.app_context():
    crud.db.create_all()

@application.route("/employees", methods = ['POST'])
def create():
    employee_dict = request.json 
    crud.create_employee(employee_dict)
    emp_id = employee_dict['id']
    savedEmployee_dict = crud.read_by_id(emp_id)
    
    # send the mail     
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

    emp_id = employee_dict["id"]
    name = employee_dict["name"]
    age  = employee_dict["age"]
    salary  = employee_dict["salary"]
    is_active_str  = 'Yes' if employee_dict["is_active"] else 'No' 

    subject = f'{date_time_str} Employee {name} Created.'
    mail_body = f'''Employee created successfully.
id : {emp_id}
name : {name}
age : {age}
salary : {salary}
is_active : {is_active_str}
    '''
    result = mail.send_gmail(mail.to_address, subject, mail_body)
    print(f'mail sent?{result}')
    # end send the mail
    return jsonify(savedEmployee_dict)

@application.route("/employees", methods = ['GET'])
def read_all():
    employees_dict = crud.read_all_employee()
    return jsonify(employees_dict)

@application.route("/employees/<app_id>", methods = ['GET'])
def read_by_id(app_id):
    app_id = int(app_id)
    employee_dict = crud.read_by_id(app_id)
    return jsonify(employee_dict)

@application.route("/employees/<app_id>", methods = ['PUT'])
def update(app_id):
    app_id = int(app_id)
    employee_dict = request.json 
    crud.update(app_id, employee_dict)
    savedEmployee_dict = crud.read_by_id(app_id)
    return jsonify(savedEmployee_dict)

@application.route("/employees/<app_id>", methods = ['DELETE'])
def delete_employee(app_id):
    app_id = int(app_id)    
    crud.delete_employee(app_id)
    return jsonify({'message' : 'Deleted Successfully'})