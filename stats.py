"""
stats.py
Aggregates numbers from every local data file into a summary for the
homepage dashboard. Read-only: this module never writes anything.
"""

import storage
import contacts
import favorites
import employers
import history


def get_summary_stats():
    """
    Build the homepage summary of job-searching activity.

    Returns:
        dict: Counts with keys:
            searches_run, listings_seen, saved_listings, saved_employers,
            tracked_employers, emails_sent, replies
    """
    tracked = contacts.load_contacts()
    emails_sent = sum(1 for c in tracked if c["status"] in ("emailed", "replied"))
    replies = sum(1 for c in tracked if c["status"] == "replied")

    return {
        "searches_run": len(history.load_history()),
        "listings_seen": storage.count_seen_jobs(),
        "saved_listings": len(favorites.load_favorites()),
        "saved_employers": len(employers.load_employers()),
        "tracked_employers": len(tracked),
        "emails_sent": emails_sent,
        "replies": replies,
    }
