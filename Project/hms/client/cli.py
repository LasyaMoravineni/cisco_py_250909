import requests

BASE_URL = "http://127.0.0.1:5000"

def menu():
    message = '''
Options are:
1 - Create Patient
2 - List All Patients
3 - Read Patient By Id
4 - Update Patient
5 - Delete Patient
6 - Exit 
Your Option: '''
    choice = int(input(message))

    if choice == 1:
        pid = int(input('ID: '))
        name = input('Name: ')
        age = int(input('Age: '))
        disease = input('Disease: ')

        patient = {"id": pid, "name": name, "age": age, "disease": disease}

        response = requests.post(f"{BASE_URL}/patients", json=patient)
        if response.ok:
            print("Patient Created Successfully:", response.json())
        else:
            print("Error:", response.text)

    elif choice == 2:
        print("List of Patients:")
        response = requests.get(f"{BASE_URL}/patients")
        if response.ok:
            for patient in response.json():
                print(patient)
        else:
            print("Error:", response.text)

    elif choice == 3:
        pid = int(input('ID: '))
        response = requests.get(f"{BASE_URL}/patients/{pid}")
        if response.ok:
            patient = response.json()
            if patient:
                print(patient)
            else:
                print("Patient not found.")
        else:
            print("Error:", response.text)

    elif choice == 4:
        pid = int(input('ID: '))
        response = requests.get(f"{BASE_URL}/patients/{pid}")
        if not response.ok or not response.json():
            print("Patient Not Found")
        else:
            print("Current Patient:", response.json())
            name = input("New Name (leave blank to keep current): ")
            age_input = input("New Age (leave blank to keep current): ")
            disease = input("New Disease (leave blank to keep current): ")

            patient = response.json()
            if name:
                patient["name"] = name
            if age_input:
                patient["age"] = int(age_input)
            if disease:
                patient["disease"] = disease

            updated = requests.put(f"{BASE_URL}/patients/{pid}", json=patient)
            if updated.ok:
                print("Patient updated successfully:", updated.json())
            else:
                print("Error:", updated.text)

    elif choice == 5:
        pid = int(input('ID: '))
        response = requests.delete(f"{BASE_URL}/patients/{pid}")
        if response.ok:
            print(response.json()["message"])
        else:
            print("Error:", response.text)

    elif choice == 6:
        print("Thank you for using the Hospital Management System")

    return choice

def menus():
    choice = menu()
    while choice != 6:
        choice = menu()

if __name__ == "__main__":
    menus()
