from concurrent.futures import ThreadPoolExecutor
import asyncio

def _average_age(patients):
    """Helper to compute average age of a list of patients"""
    if not patients:
        return 0
    return sum(p['age'] for p in patients) / len(patients)

def calculate_average_age_threaded(patients, batch_size=10):
    """
    Calculate average patient age in batches using ThreadPoolExecutor.
    
    :param patients: list of dicts with 'age' key
    :param batch_size: number of patients per batch
    :return: list of batch averages
    """
    batch_averages = []

    # Split patients into batches
    batches = [patients[i:i+batch_size] for i in range(0, len(patients), batch_size)]

    with ThreadPoolExecutor() as executor:
        results = executor.map(_average_age, batches)
        batch_averages.extend(results)

    return batch_averages


# ----------- Async version -----------
async def _async_average_age(batch):
    await asyncio.sleep(0)  # simulate async operation
    return _average_age(batch)

async def calculate_average_age_async(patients, batch_size=10):
    """
    Calculate average patient age in batches using asyncio coroutines.
    
    :param patients: list of dicts with 'age' key
    :param batch_size: number of patients per batch
    :return: list of batch averages
    """
    batch_averages = []

    batches = [patients[i:i+batch_size] for i in range(0, len(patients), batch_size)]
    tasks = [_async_average_age(batch) for batch in batches]
    results = await asyncio.gather(*tasks)
    batch_averages.extend(results)

    return batch_averages