"""
contacts.py
Tracks employers you've decided to reach out to about a job listing.
Persists outreach records to the local SQLite database (jobtrack.db).
"""

from datetime import date

import db

VALID_STATUSES = ["not contacted", "emailed", "replied", "rejected"]


def track_employer(job):
    """
    Start tracking outreach for an employer behind a job listing.

    Args:
        job (dict): A job dict from api.search_jobs(), with at least
                     id, company, title and url keys.

    Returns:
        None. No-op if this job id is already tracked.
    """
    job_id = str(job.get("id"))

    if db.get_contact(job_id) is not None:
        return

    db.add_contact({
        "job_id": job_id,
        "company": job.get("company"),
        "job_title": job.get("title"),
        "job_url": job.get("url"),
        "contact_email": "",
        "status": "not contacted",
        "date_contacted": "",
    })


def untrack_employer(job_id):
    """
    Stop tracking outreach for a job listing.

    Args:
        job_id: The id of the job to stop tracking.

    Returns:
        None. No-op if this job id isn't tracked.
    """
    db.remove_contact(job_id)


def load_contacts():
    """
    Load all tracked outreach records.

    Returns:
        list[dict]: All outreach records currently being tracked.
    """
    return db.get_all_contacts()


def is_tracked(job_id):
    """
    Check whether a job listing is already being tracked.

    Args:
        job_id: The id of the job to check.

    Returns:
        bool: True if this job id has an outreach record.
    """
    return db.get_contact(job_id) is not None


def set_contact_email(job_id, email):
    """
    Set the contact email for a tracked employer.

    Args:
        job_id: The id of the job whose record should be updated.
        email (str): The contact email address, found manually by the user.

    Returns:
        None. No-op if this job id isn't tracked.
    """
    if db.get_contact(job_id) is None:
        return
    db.update_contact_email(job_id, email)


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

    if db.get_contact(job_id) is None:
        return

    date_contacted = date.today().isoformat() if status == "emailed" else None
    db.update_contact_status(job_id, status, date_contacted)
