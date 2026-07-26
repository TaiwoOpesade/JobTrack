"""
storage.py
Tracks which job listings have already been seen, so we can flag new ones
on each search. Persists to the local SQLite database (jobtrack.db).
"""

import db


def flag_new_jobs(jobs):
    """
    Compare a fresh batch of job listings against previously seen ones.

    Args:
        jobs (list[dict]): Job listings from api.search_jobs(), each with an "id" key.

    Returns:
        list[dict]: The same job listings, each with an added "is_new" boolean key.
                     Also updates the stored record so these jobs count as
                     "seen" for the next search.
    """
    seen_ids = db.get_seen_ids()

    for job in jobs:
        job_id = str(job.get("id"))
        job["is_new"] = job_id not in seen_ids

    # Update seen list with all IDs from this batch
    db.add_seen_ids({str(job.get("id")) for job in jobs})

    return jobs


def count_seen_jobs():
    """
    Count how many distinct job listings have ever been seen.

    Returns:
        int: The number of unique job IDs recorded so far.
    """
    return db.count_seen_ids()


def reset_seen_jobs():
    """Clear the seen-jobs history (useful if you want everything to show as new again)."""
    db.clear_seen_ids()
