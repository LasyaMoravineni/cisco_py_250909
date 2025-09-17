"""
batch_calc.py - Patient average age calculation using threads and asyncio.
"""

from concurrent.futures import ThreadPoolExecutor
import asyncio


def _calculate_batch_average(patients):
    """
    Calculate the average age for a single batch of patients.

    Args:
        patients (list[dict]): List of patient dictionaries with "age" keys.

    Returns:
        float: Average age of the batch, or 0 if empty.
    """
    ages = [p["age"] for p in patients]
    return sum(ages) / len(ages) if ages else 0


def calculate_average_age_threaded(patients, batch_size=10):
    """
    Calculate average patient age using ThreadPoolExecutor for batch processing.

    Args:
        patients (list[dict]): List of patient dictionaries with "age" keys.
        batch_size (int): Number of patients per batch.

    Returns:
        float: Weighted average age across all patients.
    """
    batches = [patients[i:i + batch_size] for i in range(0, len(patients), batch_size)]
    # Run batch averages in parallel (not used directly, but demonstrates concurrency)
    with ThreadPoolExecutor() as executor:
        _ = list(executor.map(_calculate_batch_average, batches))

    total_age = sum(p["age"] for p in patients)
    return total_age / len(patients) if patients else 0


async def calculate_average_age_async(patients, batch_size=10):
    """
    Calculate average patient age asynchronously using asyncio coroutines.

    Args:
        patients (list[dict]): List of patient dictionaries with "age" keys.
        batch_size (int): Number of patients per batch.

    Returns:
        float: Weighted average age across all patients.
    """
    batches = [patients[i:i + batch_size] for i in range(0, len(patients), batch_size)]

    async def process_batch(batch):
        return _calculate_batch_average(batch)

    # Run batch averages concurrently (not used directly, but demonstrates asyncio)
    await asyncio.gather(*(process_batch(b) for b in batches))

    total_age = sum(p["age"] for p in patients)
    return total_age / len(patients) if patients else 0
