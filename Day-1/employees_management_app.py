employees = []

employee=('Bhanu',22,50000, True)
employees.append(employee)

employee=('Mahesh',46,4000.50, True)
employees.append(employee)

employee=('Vaishnavi',21,40000.75, True)
employees.append(employee)

print("After add all employees: ",employees)

i=0
search='Vaishnavi'
index=-1
for emp in employees:
    if emp[0] == search:
        index=i
        break
    i+=1

if index==-1:
    print("Employee not found")

else:
    search_employee = employees[index]
    print(search_employee)
    salary=float(input('Salary'))
    employee=(search_employee[0],search_employee[1],salary, search_employee[3])
    employees[index]=employee
print('After search and update: ',employees)

employee=('Dravid',50,200.75,True)
employees.append(employee)
print('after add Dravid: ',employees)
#delete last employee
employees.pop()
print('after delete Dravid: ',employees)


#delete employee ny position
position = 1
employees.pop(position)
print('after delete Mahesh: ',employees)
