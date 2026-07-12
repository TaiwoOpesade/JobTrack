"""
favorites.py
Saves job listings the user wants to keep, so they survive between searches
and app restarts. Persists to a local JSON file.
"""

import json
import os
from datetime import date

DATA_FILE = os.path.join(os.path.dirname(__file__), "favorites.json")


def _load():
    """Load all saved listings from disk.

    Returns:
        dict: Mapping of job_id (str) to saved listing dict.
    """
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save(records):
    """Save all listings to disk.

    Args:
        records (dict): Mapping of job_id (str) to saved listing dict.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def save_listing(job):
    """
    Save a job listing so it can be revisited later.

    Args:
        job (dict): A job dict from api.search_jobs().

    Returns:
        None. No-op if this job id is already saved.
    """
    records = _load()
    job_id = str(job.get("id"))

    if job_id in records:
        return

    records[job_id] = {
        "id": job_id,
        "title": job.get("title"),
        "company": job.get("company"),
        "location": job.get("location"),
        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),
        "url": job.get("url"),
        "description": job.get("description"),
        "date_saved": date.today().isoformat(),
    }
    _save(records)


def unsave_listing(job_id):
    """
    Remove a saved job listing.

    Args:
        job_id: The id of the listing to remove.

    Returns:
        None. No-op if this job id isn't saved.
    """
    records = _load()
    job_id = str(job_id)

    if job_id in records:
        del records[job_id]
        _save(records)


def load_favorites():
    """
    Load all saved job listings.

    Returns:
        list[dict]: All saved listings, most recently saved last.
    """
    records = _load()
    return list(records.values())


def is_saved(job_id):
    """
    Check whether a job listing is already saved.

    Args:
        job_id: The id of the listing to check.

    Returns:
        bool: True if this job id is saved.
    """
    records = _load()
    return str(job_id) in records
