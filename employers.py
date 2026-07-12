"""
employers.py
Saves employers the user wants to follow, so their current listings can be
looked up on demand. Persists to a local JSON file.
"""

import json
import os
from datetime import date

DATA_FILE = os.path.join(os.path.dirname(__file__), "employers.json")


def _load():
    """Load all saved employers from disk.

    Returns:
        dict: Mapping of employer name (str) to saved employer dict.
    """
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save(records):
    """Save all employers to disk.

    Args:
        records (dict): Mapping of employer name (str) to saved employer dict.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def save_employer(name):
    """
    Save an employer to follow.

    Args:
        name (str): The employer's name, e.g. from a job dict's "company" key.

    Returns:
        None. No-op if the name is blank or already saved.
    """
    name = (name or "").strip()
    if not name:
        return

    records = _load()
    if name in records:
        return

    records[name] = {
        "name": name,
        "date_saved": date.today().isoformat(),
    }
    _save(records)


def remove_employer(name):
    """
    Stop following a saved employer.

    Args:
        name (str): The employer name to remove.

    Returns:
        None. No-op if the employer isn't saved.
    """
    records = _load()
    if name in records:
        del records[name]
        _save(records)


def load_employers():
    """
    Load all saved employers.

    Returns:
        list[dict]: All saved employers, each with name and date_saved keys.
    """
    records = _load()
    return list(records.values())


def is_saved_employer(name):
    """
    Check whether an employer is already saved.

    Args:
        name (str): The employer name to check.

    Returns:
        bool: True if this employer is saved.
    """
    records = _load()
    return (name or "").strip() in records
