"""
history.py
Records every search the user runs, so the homepage can summarise their
job-hunting activity. Persists to a local JSON file.
"""

import json
import os
from datetime import date

DATA_FILE = os.path.join(os.path.dirname(__file__), "search_history.json")


def _load():
    """Load the search history from disk.

    Returns:
        list[dict]: All recorded searches, oldest first.
    """
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _save(entries):
    """Save the search history to disk.

    Args:
        entries (list[dict]): All recorded searches.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


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
    entries = _load()
    entries.append({
        "keyword": keyword,
        "location": location,
        "results_found": results_found,
        "new_found": new_found,
        "date": date.today().isoformat(),
    })
    _save(entries)


def load_history():
    """
    Load the full search history.

    Returns:
        list[dict]: All recorded searches, oldest first.
    """
    return _load()


def recent_searches(limit=5):
    """
    Get the most recent searches, newest first.

    Args:
        limit (int): Maximum number of searches to return.

    Returns:
        list[dict]: Up to `limit` recorded searches, newest first.
    """
    entries = _load()
    return list(reversed(entries[-limit:]))
