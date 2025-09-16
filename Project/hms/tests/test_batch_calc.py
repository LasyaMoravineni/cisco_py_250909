from hms.app import batch_calc

def test_threaded_avg_age():
    patients = [
        {"id": 1, "name": "Alice", "age": 34, "disease": "Flu"},
        {"id": 2, "name": "Rahul", "age": 45, "disease": "Diabetes"},
        {"id": 3, "name": "Sophia", "age": 29, "disease": "Asthma"},
    ]
    avg_age = batch_calc.calculate_average_age_threaded(patients, batch_size=2)
    assert round(avg_age, 2) == round((34 + 45 + 29) / 3, 2)

def test_async_avg_age(event_loop):
    patients = [
        {"id": 1, "name": "Alice", "age": 34, "disease": "Flu"},
        {"id": 2, "name": "Rahul", "age": 45, "disease": "Diabetes"},
        {"id": 3, "name": "Sophia", "age": 29, "disease": "Asthma"},
    ]
    avg_age = event_loop.run_until_complete(
        batch_calc.calculate_average_age_async(patients, batch_size=2)
    )
    assert round(avg_age, 2) == round((34 + 45 + 29) / 3, 2)
