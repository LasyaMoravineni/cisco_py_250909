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
    try:
        choice = int(input(message))
    except ValueError:
        print("Invalid choice. Please enter a number from 1 to 6.")
        return 0

    try:
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
                print("Error:", response.json().get("error", response.text))

        elif choice == 2:
            print("List of Patients:")
            response = requests.get(f"{BASE_URL}/patients")
            if response.ok:
                patients = response.json()
                if patients:
                    for patient in patients:
                        print(patient)
                else:
                    print("No patients found.")
            else:
                print("Error:", response.json().get("error", response.text))

        elif choice == 3:
            pid = int(input('ID: '))
            response = requests.get(f"{BASE_URL}/patients/{pid}")
            if response.ok:
                print(response.json())
            else:
                print("Error:", response.json().get("error", response.text))

        elif choice == 4:
            pid = int(input('ID: '))
            response = requests.get(f"{BASE_URL}/patients/{pid}")
            if not response.ok:
                print("Patient Not Found:", response.json().get("error", response.text))
            else:
                patient = response.json()
                print("Current Patient:", patient)

                name = input(f"New Name (leave blank to keep '{patient['name']}'): ")
                age_input = input(f"New Age (leave blank to keep '{patient['age']}'): ")
                disease = input(f"New Disease (leave blank to keep '{patient['disease']}'): ")

                if name:
                    patient["name"] = name
                if age_input:
                    try:
                        patient["age"] = int(age_input)
                    except ValueError:
                        print("Invalid age. Keeping current value.")
                if disease:
                    patient["disease"] = disease

                updated = requests.put(f"{BASE_URL}/patients/{pid}", json=patient)
                if updated.ok:
                    print("Patient updated successfully:", updated.json())
                else:
                    print("Error:", updated.json().get("error", updated.text))

        elif choice == 5:
            pid = int(input('ID: '))
            response = requests.delete(f"{BASE_URL}/patients/{pid}")
            if response.ok:
                print(response.json().get("message", "Deleted Successfully"))
            else:
                print("Error:", response.json().get("error", response.text))

        elif choice == 6:
            print("Thank you for using the Hospital Management System")

        else:
            print("Invalid choice. Please select 1-6.")

    except requests.exceptions.ConnectionError:
        print("Cannot connect to the server. Make sure Flask is running.")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return choice


def menus():
    choice = menu()
    while choice != 6:
        choice = menu()


if __name__ == "__main__":
    menus()
