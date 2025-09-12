import repo_pickle_dict as repo

employee=(101,'Bhanu',22,50000,True)
repo.create_employee(employee)
print(f'Employee {employee[1]} created successfully')
print('After add: ',repo.read_all_employee())

employee=(102,'Mahesh',46,4000.50,True)
repo.create_employee(employee)
print(f'Employee {employee[1]} created successfully')
print('After add: ',repo.read_all_employee())

employee=(103,'Vaishnavi',21,40000.75,True)
repo.create_employee(employee)
print(f'Employee {employee[1]} created successfully')
print('After add: ',repo.read_all_employee())


#test read by id
employee=repo.read_by_id(103)
if employee == None:
    print('Employee not found')
else:
    print(employee)



#test upadte
employee=repo.read_by_id(103)
if employee==None:
    print('Employee not found')

else:
    id,name,age,salary,is_active = employee
    salary+=20000
    new_employee = (id,name,age,salary,is_active)
    repo.update(103,new_employee)
    print('After update:', repo.read_all_employee())


#test delete
repo.delete_employee(102)
print('After delete: ',repo.read_all_employee())
