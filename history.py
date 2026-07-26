"""
history.py
Records every search the user runs, so the homepage can summarise their
job-hunting activity. Persists to the local SQLite database (jobtrack.db).
"""

from datetime import date

import db


def record_search(keyword, location, results_found, new_found):
    """
    Record one completed search.

    Args:
        keyword (str): The search keyword used.
        location (str): The location filter used ("" if none).
        results_found (int): How many listings the search returned.
        new_found (int): How many of those were new since the last search.

    Returns:
        None.
    """
    db.add_search(keyword, location, results_found, new_found, date.today().isoformat())


def load_history():
    """
    Load the full search history.

    Returns:
        list[dict]: All recorded searches, oldest first.
    """
    return db.get_all_searches()


def recent_searches(limit=5):
    """
    Get the most recent searches, newest first.

    Args:
        limit (int): Maximum number of searches to return.

    Returns:
        list[dict]: Up to `limit` recorded searches, newest first.
    """
    entries = db.get_all_searches()
    return list(reversed(entries[-limit:]))
