"""
storage.py
Tracks which job listings have already been seen, so we can flag new ones
on each search. Persists to a local JSON file between runs.
"""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "seen_jobs.json")


def _load_seen_ids():
    """Load the set of previously seen job IDs from disk."""
    if not os.path.exists(DATA_FILE):
        return set()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("seen_ids", []))
    except (json.JSONDecodeError, IOError):
        return set()


def _save_seen_ids(seen_ids):
    """Save the full set of seen job IDs to disk."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"seen_ids": list(seen_ids)}, f, indent=2)


def flag_new_jobs(jobs):
    """
    Compare a fresh batch of job listings against previously seen ones.

    Args:
        jobs (list[dict]): Job listings from api.search_jobs(), each with an "id" key.

    Returns:
        list[dict]: The same job listings, each with an added "is_new" boolean key.
                     Also updates the on-disk record so these jobs count as
                     "seen" for the next search.
    """
    seen_ids = _load_seen_ids()

    for job in jobs:
        job_id = str(job.get("id"))
        job["is_new"] = job_id not in seen_ids

    # Update seen list with all IDs from this batch
    updated_ids = seen_ids | {str(job.get("id")) for job in jobs}
    _save_seen_ids(updated_ids)

    return jobs


def count_seen_jobs():
    """
    Count how many distinct job listings have ever been seen.

    Returns:
        int: The number of unique job IDs recorded so far.
    """
    return len(_load_seen_ids())


def reset_seen_jobs():
    """Clear the seen-jobs history (useful if you want everything to show as new again)."""
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
