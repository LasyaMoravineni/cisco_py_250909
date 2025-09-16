from flask import Flask,request,jsonify
import app.crud as crud
from app.config import config

#application object is created
application = Flask(__name__) #server instance is created

#db conn str
application.config['SQLALCHEMY_DATABASE_URI']=config['DB_URL']
application.config['SQLALCHEMY_ECHO']=True

#configuring the database
crud.db.init_app(application) #connecting with application

#create tables
with application.app_context():
    crud.db.create_all()


#defining endpoints
@application.route("/employees",methods=['POST'])
def create():
    employee_dict = request.json
    crud.create_employee(employee_dict)
    emp_id=employee_dict['id']
    savedEmployee_dict=crud.read_by_id(emp_id)
    return jsonify(savedEmployee_dict)  #returns in json file

@application.route("/employees",methods=['GET'])
def read_all():
    employees_dict=crud.read_all_employee()
    return jsonify(employees_dict)

@application.route("/employees/<app_id>",methods=['GET'])
def read_by_id(app_id):
    app_id=int(app_id)
    employee_dict=crud.read_by_id(app_id)
    return jsonify(employee_dict)

@application.route("/employees/<app_id>",methods=['PUT'])
def update(app_id):
    app_id=int(app_id)
    employee_dict=request.json
    crud.update(app_id, employee_dict)
    savedEmployee_dict=crud.read_by_id(app_id)
    return jsonify(savedEmployee_dict)

@application.route("/employees/<app_id>",methods=['DELETE'])
def delete_employee(app_id):
    app_id=int(app_id)
    crud.delete_employee(app_id)
    return jsonify({'message':'Deleted successfully'})