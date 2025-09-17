"""
cli.py - Command-line interface for Hospital Management System (HMS)
Provides interactive menu to manage patients via REST API.
"""

import requests

BASE_URL = "http://127.0.0.1:5000"
TIMEOUT = 5  # seconds


def create_patient():
    """Create a new patient via API."""
    pid = int(input("ID: "))
    name = input("Name: ")
    age = int(input("Age: "))
    disease = input("Disease: ")

    patient = {"id": pid, "name": name, "age": age, "disease": disease}
    response = requests.post(f"{BASE_URL}/patients", json=patient, timeout=TIMEOUT)
    if response.ok:
        print("Patient Created Successfully:", response.json())
    else:
        print("Error:", response.json().get("error", response.text))


def list_patients():
    """List all patients from the API."""
    response = requests.get(f"{BASE_URL}/patients", timeout=TIMEOUT)
    if response.ok:
        patients = response.json()
        if patients:
            for patient in patients:
                print(patient)
        else:
            print("No patients found.")
    else:
        print("Error:", response.json().get("error", response.text))


def read_patient():
    """Read a patient by ID."""
    pid = int(input("ID: "))
    response = requests.get(f"{BASE_URL}/patients/{pid}", timeout=TIMEOUT)
    if response.ok:
        print(response.json())
    else:
        print("Error:", response.json().get("error", response.text))


def update_patient():
    """Update an existing patient's details."""
    pid = int(input("ID: "))
    response = requests.get(f"{BASE_URL}/patients/{pid}", timeout=TIMEOUT)
    if not response.ok:
        print("Patient Not Found:", response.json().get("error", response.text))
        return

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

    updated = requests.put(f"{BASE_URL}/patients/{pid}", json=patient, timeout=TIMEOUT)
    if updated.ok:
        print("Patient updated successfully:", updated.json())
    else:
        print("Error:", updated.json().get("error", updated.text))


def delete_patient():
    """Delete a patient by ID."""
    pid = int(input("ID: "))
    response = requests.delete(f"{BASE_URL}/patients/{pid}", timeout=TIMEOUT)
    if response.ok:
        print(response.json().get("message", "Deleted Successfully"))
    else:
        print("Error:", response.json().get("error", response.text))


def menu():
    """
    Display the menu and process user input.
    Returns the selected choice (int).
    """
    message = (
        "\nOptions are:\n"
        "1 - Create Patient\n"
        "2 - List All Patients\n"
        "3 - Read Patient By Id\n"
        "4 - Update Patient\n"
        "5 - Delete Patient\n"
        "6 - Exit \n"
        "Your Option: "
    )
    try:
        choice = int(input(message))
    except ValueError:
        print("Invalid choice. Please enter a number from 1 to 6.")
        return 0

    try:
        if choice == 1:
            create_patient()
        elif choice == 2:
            list_patients()
        elif choice == 3:
            read_patient()
        elif choice == 4:
            update_patient()
        elif choice == 5:
            delete_patient()
        elif choice == 6:
            print("Thank you for using the Hospital Management System")
        else:
            print("Invalid choice. Please select 1-6.")
    except requests.exceptions.ConnectionError:
        print("Cannot connect to the server. Make sure Flask is running.")
    except requests.RequestException as e:
        print(f"Request error: {e}")

    return choice


def menus():
    """Loop through menu until user exits."""
    choice = menu()
    while choice != 6:
        choice = menu()


if __name__ == "__main__":
    menus()
