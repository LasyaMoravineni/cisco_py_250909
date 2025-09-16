import json

def test_create_patient(client):
    patient = {"id": 1, "name": "Alice Johnson", "age": 34, "disease": "Flu"}
    response = client.post("/patients", data=json.dumps(patient), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Alice Johnson"
    assert data["disease"] == "Flu"

def test_read_all_patients(client):
    patient = {"id": 2, "name": "Rahul Mehta", "age": 45, "disease": "Diabetes"}
    client.post("/patients", data=json.dumps(patient), content_type="application/json")

    response = client.get("/patients")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_update_patient(client):
    patient = {"id": 3, "name": "Sophia Lee", "age": 29, "disease": "Asthma"}
    client.post("/patients", data=json.dumps(patient), content_type="application/json")

    updated_patient = {"id": 3, "name": "Sophia Lee", "age": 30, "disease": "Asthma"}
    response = client.put("/patients/3", data=json.dumps(updated_patient), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert data["age"] == 30

def test_delete_patient(client):
    patient = {"id": 4, "name": "John Doe", "age": 50, "disease": "Heart Disease"}
    client.post("/patients", data=json.dumps(patient), content_type="application/json")

    response = client.delete("/patients/4")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Deleted Successfully"
