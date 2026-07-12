"""
contacts.py
Tracks employers you've decided to reach out to about a job listing.
Persists outreach records to a local JSON file between runs.
"""

import json
import os
from datetime import date

DATA_FILE = os.path.join(os.path.dirname(__file__), "outreach.json")

VALID_STATUSES = ["not contacted", "emailed", "replied", "rejected"]


def _load():
    """Load all outreach records from disk.

    Returns:
        dict: Mapping of job_id (str) to outreach record dict.
    """
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save(records):
    """Save all outreach records to disk.

    Args:
        records (dict): Mapping of job_id (str) to outreach record dict.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def track_employer(job):
    """
    Start tracking outreach for an employer behind a job listing.

    Args:
        job (dict): A job dict from api.search_jobs(), with at least
                     id, company, title and url keys.

    Returns:
        None. No-op if this job id is already tracked.
    """
    records = _load()
    job_id = str(job.get("id"))

    if job_id in records:
        return

    records[job_id] = {
        "job_id": job_id,
        "company": job.get("company"),
        "job_title": job.get("title"),
        "job_url": job.get("url"),
        "contact_email": "",
        "status": "not contacted",
        "date_contacted": "",
    }
    _save(records)


def untrack_employer(job_id):
    """
    Stop tracking outreach for a job listing.

    Args:
        job_id: The id of the job to stop tracking.

    Returns:
        None. No-op if this job id isn't tracked.
    """
    records = _load()
    job_id = str(job_id)

    if job_id in records:
        del records[job_id]
        _save(records)


def load_contacts():
    """
    Load all tracked outreach records.

    Returns:
        list[dict]: All outreach records currently being tracked.
    """
    records = _load()
    return list(records.values())


def is_tracked(job_id):
    """
    Check whether a job listing is already being tracked.

    Args:
        job_id: The id of the job to check.

    Returns:
        bool: True if this job id has an outreach record.
    """
    records = _load()
    return str(job_id) in records


def set_contact_email(job_id, email):
    """
    Set the contact email for a tracked employer.

    Args:
        job_id: The id of the job whose record should be updated.
        email (str): The contact email address, found manually by the user.

    Returns:
        None. No-op if this job id isn't tracked.
    """
    records = _load()
    job_id = str(job_id)

    if job_id in records:
        records[job_id]["contact_email"] = email
        _save(records)


def set_status(job_id, status):
    """
    Update the outreach status for a tracked employer.

    Args:
        job_id: The id of the job whose record should be updated.
        status (str): One of "not contacted", "emailed", "replied", "rejected".

    Returns:
        None. No-op if this job id isn't tracked.

    Raises:
        ValueError: If status isn't one of the recognised statuses.
    """
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")

    records = _load()
    job_id = str(job_id)

    if job_id not in records:
        return

    records[job_id]["status"] = status
    if status == "emailed":
        records[job_id]["date_contacted"] = date.today().isoformat()

    _save(records)
