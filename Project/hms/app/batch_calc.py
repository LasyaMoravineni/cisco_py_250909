from concurrent.futures import ThreadPoolExecutor
import asyncio

def _calculate_batch_average(patients):
    ages = [p["age"] for p in patients]
    return sum(ages) / len(ages) if ages else 0

def calculate_average_age_threaded(patients, batch_size=10):
    batches = [patients[i:i + batch_size] for i in range(0, len(patients), batch_size)]
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(_calculate_batch_average, batches))
    # FIX: return weighted average, not list
    total_age = sum(p["age"] for p in patients)
    return total_age / len(patients) if patients else 0

async def calculate_average_age_async(patients, batch_size=10):
    batches = [patients[i:i + batch_size] for i in range(0, len(patients), batch_size)]

    async def process_batch(batch):
        return _calculate_batch_average(batch)

    results = await asyncio.gather(*(process_batch(b) for b in batches))
    # FIX: return weighted average, not list
    total_age = sum(p["age"] for p in patients)
    return total_age / len(patients) if patients else 0
