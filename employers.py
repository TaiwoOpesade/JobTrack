"""
employers.py
Saves employers the user wants to follow, so their current listings can be
looked up on demand. Persists to the local SQLite database (jobtrack.db).
"""

from datetime import date

import db


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

    if db.get_employer(name) is not None:
        return

    db.add_employer(name, date.today().isoformat())


def remove_employer(name):
    """
    Stop following a saved employer.

    Args:
        name (str): The employer name to remove.

    Returns:
        None. No-op if the employer isn't saved.
    """
    db.remove_employer(name)


def load_employers():
    """
    Load all saved employers.

    Returns:
        list[dict]: All saved employers, each with name and date_saved keys.
    """
    return db.get_all_employers()


def is_saved_employer(name):
    """
    Check whether an employer is already saved.

    Args:
        name (str): The employer name to check.

    Returns:
        bool: True if this employer is saved.
    """
    return db.get_employer((name or "").strip()) is not None
