"""
favorites.py
Saves job listings the user wants to keep, so they survive between searches
and app restarts. Persists to the local SQLite database (jobtrack.db).
"""

from datetime import date

import db


def _to_public(record):
    """Map a favorites row (job_id column) to the public dict shape (id key)."""
    if record is None:
        return None
    public = dict(record)
    public["id"] = public.pop("job_id")
    return public


def save_listing(job):
    """
    Save a job listing so it can be revisited later.

    Args:
        job (dict): A job dict from api.search_jobs().

    Returns:
        None. No-op if this job id is already saved.
    """
    job_id = str(job.get("id"))

    if db.get_favorite(job_id) is not None:
        return

    db.add_favorite({
        "id": job_id,
        "title": job.get("title"),
        "company": job.get("company"),
        "location": job.get("location"),
        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),
        "url": job.get("url"),
        "description": job.get("description"),
        "date_saved": date.today().isoformat(),
    })


def unsave_listing(job_id):
    """
    Remove a saved job listing.

    Args:
        job_id: The id of the listing to remove.

    Returns:
        None. No-op if this job id isn't saved.
    """
    db.remove_favorite(job_id)


def load_favorites():
    """
    Load all saved job listings.

    Returns:
        list[dict]: All saved listings, most recently saved last.
    """
    return [_to_public(record) for record in db.get_all_favorites()]


def is_saved(job_id):
    """
    Check whether a job listing is already saved.

    Args:
        job_id: The id of the listing to check.

    Returns:
        bool: True if this job id is saved.
    """
    return db.get_favorite(job_id) is not None
