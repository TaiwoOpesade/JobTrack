"""
db.py
Single SQLite database (jobtrack.db) backing all local persistence -
seen listings, saved favourites, saved employers, outreach contacts and
search history. Uses only Python's built-in sqlite3 module.

On first use, if jobtrack.db doesn't exist yet (or is missing rows) and
any of the legacy *.json data files are present beside the code, their
data is imported into the database once. The JSON files themselves are
never modified or deleted by this process.
"""

import json
import os
import sqlite3
from contextlib import contextmanager

DB_FILE = os.path.join(os.path.dirname(__file__), "jobtrack.db")

SEEN_JOBS_JSON = os.path.join(os.path.dirname(__file__), "seen_jobs.json")
FAVORITES_JSON = os.path.join(os.path.dirname(__file__), "favorites.json")
EMPLOYERS_JSON = os.path.join(os.path.dirname(__file__), "employers.json")
OUTREACH_JSON = os.path.join(os.path.dirname(__file__), "outreach.json")
HISTORY_JSON = os.path.join(os.path.dirname(__file__), "search_history.json")

SCHEMA = """
CREATE TABLE IF NOT EXISTS seen_jobs (
    job_id TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS favorites (
    job_id TEXT PRIMARY KEY,
    title TEXT,
    company TEXT,
    location TEXT,
    salary_min INTEGER,
    salary_max INTEGER,
    url TEXT,
    description TEXT,
    date_saved TEXT
);

CREATE TABLE IF NOT EXISTS employers (
    name TEXT PRIMARY KEY,
    date_saved TEXT
);

CREATE TABLE IF NOT EXISTS contacts (
    job_id TEXT PRIMARY KEY,
    company TEXT,
    job_title TEXT,
    job_url TEXT,
    contact_email TEXT,
    status TEXT,
    date_contacted TEXT
);

CREATE TABLE IF NOT EXISTS search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT,
    location TEXT,
    results_found INTEGER,
    new_found INTEGER,
    date TEXT
);

CREATE TABLE IF NOT EXISTS _migrations (
    source TEXT PRIMARY KEY,
    imported_at TEXT
);
"""

_initialized = False


@contextmanager
def _connect():
    """Open a connection to jobtrack.db with row access by column name."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _load_json(path):
    """Load a legacy JSON data file, returning None if missing/unreadable."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def _already_migrated(conn, source):
    row = conn.execute(
        "SELECT 1 FROM _migrations WHERE source = ?", (source,)
    ).fetchone()
    return row is not None


def _mark_migrated(conn, source):
    import datetime
    conn.execute(
        "INSERT OR IGNORE INTO _migrations (source, imported_at) VALUES (?, ?)",
        (source, datetime.datetime.now().isoformat()),
    )


def _migrate_seen_jobs(conn):
    if _already_migrated(conn, "seen_jobs.json"):
        return
    data = _load_json(SEEN_JOBS_JSON)
    if data:
        seen_ids = data.get("seen_ids", [])
        conn.executemany(
            "INSERT OR IGNORE INTO seen_jobs (job_id) VALUES (?)",
            [(str(job_id),) for job_id in seen_ids],
        )
    _mark_migrated(conn, "seen_jobs.json")


def _migrate_favorites(conn):
    if _already_migrated(conn, "favorites.json"):
        return
    data = _load_json(FAVORITES_JSON)
    if data:
        for job_id, record in data.items():
            conn.execute(
                """INSERT OR IGNORE INTO favorites
                   (job_id, title, company, location, salary_min, salary_max,
                    url, description, date_saved)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    str(job_id),
                    record.get("title"),
                    record.get("company"),
                    record.get("location"),
                    record.get("salary_min"),
                    record.get("salary_max"),
                    record.get("url"),
                    record.get("description"),
                    record.get("date_saved"),
                ),
            )
    _mark_migrated(conn, "favorites.json")


def _migrate_employers(conn):
    if _already_migrated(conn, "employers.json"):
        return
    data = _load_json(EMPLOYERS_JSON)
    if data:
        for name, record in data.items():
            conn.execute(
                "INSERT OR IGNORE INTO employers (name, date_saved) VALUES (?, ?)",
                (name, record.get("date_saved")),
            )
    _mark_migrated(conn, "employers.json")


def _migrate_contacts(conn):
    if _already_migrated(conn, "outreach.json"):
        return
    data = _load_json(OUTREACH_JSON)
    if data:
        for job_id, record in data.items():
            conn.execute(
                """INSERT OR IGNORE INTO contacts
                   (job_id, company, job_title, job_url, contact_email,
                    status, date_contacted)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    str(job_id),
                    record.get("company"),
                    record.get("job_title"),
                    record.get("job_url"),
                    record.get("contact_email", ""),
                    record.get("status", "not contacted"),
                    record.get("date_contacted", ""),
                ),
            )
    _mark_migrated(conn, "outreach.json")


def _migrate_history(conn):
    if _already_migrated(conn, "search_history.json"):
        return
    data = _load_json(HISTORY_JSON)
    if data:
        conn.executemany(
            """INSERT INTO search_history
               (keyword, location, results_found, new_found, date)
               VALUES (?, ?, ?, ?, ?)""",
            [
                (
                    entry.get("keyword"),
                    entry.get("location"),
                    entry.get("results_found"),
                    entry.get("new_found"),
                    entry.get("date"),
                )
                for entry in data
            ],
        )
    _mark_migrated(conn, "search_history.json")


def init_db():
    """
    Create jobtrack.db and its tables if they don't already exist, then
    import any legacy JSON data files exactly once. Safe to call many
    times - subsequent calls are no-ops once migration has run.
    """
    global _initialized
    if _initialized:
        return
    with _connect() as conn:
        conn.executescript(SCHEMA)
        _migrate_seen_jobs(conn)
        _migrate_favorites(conn)
        _migrate_employers(conn)
        _migrate_contacts(conn)
        _migrate_history(conn)
    _initialized = True


def _ensure_ready():
    if not _initialized:
        init_db()


# ---------------------------------------------------------------------------
# Seen jobs
# ---------------------------------------------------------------------------

def get_seen_ids():
    """Return the set of previously seen job IDs (str)."""
    _ensure_ready()
    with _connect() as conn:
        rows = conn.execute("SELECT job_id FROM seen_jobs").fetchall()
        return {row["job_id"] for row in rows}


def add_seen_ids(job_ids):
    """Record a batch of job IDs as seen (no-op for ones already recorded)."""
    _ensure_ready()
    with _connect() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO seen_jobs (job_id) VALUES (?)",
            [(str(job_id),) for job_id in job_ids],
        )


def count_seen_ids():
    """Return how many distinct job IDs have ever been seen."""
    _ensure_ready()
    with _connect() as conn:
        row = conn.execute("SELECT COUNT(*) AS c FROM seen_jobs").fetchone()
        return row["c"]


def clear_seen_ids():
    """Delete all seen-job records."""
    _ensure_ready()
    with _connect() as conn:
        conn.execute("DELETE FROM seen_jobs")


# ---------------------------------------------------------------------------
# Favorites
# ---------------------------------------------------------------------------

def get_favorite(job_id):
    """Return the saved favourite record for job_id, or None."""
    _ensure_ready()
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM favorites WHERE job_id = ?", (str(job_id),)
        ).fetchone()
        return dict(row) if row else None


def add_favorite(record):
    """Insert a favourite record (dict with job_id/title/... keys). No-op if it exists."""
    _ensure_ready()
    with _connect() as conn:
        conn.execute(
            """INSERT OR IGNORE INTO favorites
               (job_id, title, company, location, salary_min, salary_max,
                url, description, date_saved)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                str(record.get("id")),
                record.get("title"),
                record.get("company"),
                record.get("location"),
                record.get("salary_min"),
                record.get("salary_max"),
                record.get("url"),
                record.get("description"),
                record.get("date_saved"),
            ),
        )


def remove_favorite(job_id):
    """Delete a favourite record by job_id."""
    _ensure_ready()
    with _connect() as conn:
        conn.execute("DELETE FROM favorites WHERE job_id = ?", (str(job_id),))


def get_all_favorites():
    """Return all favourite records, in insertion (rowid) order."""
    _ensure_ready()
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM favorites ORDER BY rowid").fetchall()
        return [dict(row) for row in rows]


# ---------------------------------------------------------------------------
# Employers
# ---------------------------------------------------------------------------

def get_employer(name):
    """Return the saved employer record for name, or None."""
    _ensure_ready()
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM employers WHERE name = ?", (name,)
        ).fetchone()
        return dict(row) if row else None


def add_employer(name, date_saved):
    """Insert a saved employer. No-op if already saved."""
    _ensure_ready()
    with _connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO employers (name, date_saved) VALUES (?, ?)",
            (name, date_saved),
        )


def remove_employer(name):
    """Delete a saved employer by name."""
    _ensure_ready()
    with _connect() as conn:
        conn.execute("DELETE FROM employers WHERE name = ?", (name,))


def get_all_employers():
    """Return all saved employer records, in insertion (rowid) order."""
    _ensure_ready()
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM employers ORDER BY rowid").fetchall()
        return [dict(row) for row in rows]


# ---------------------------------------------------------------------------
# Contacts (outreach)
# ---------------------------------------------------------------------------

def get_contact(job_id):
    """Return the outreach record for job_id, or None."""
    _ensure_ready()
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM contacts WHERE job_id = ?", (str(job_id),)
        ).fetchone()
        return dict(row) if row else None


def add_contact(record):
    """Insert an outreach record (dict with job_id/company/... keys). No-op if it exists."""
    _ensure_ready()
    with _connect() as conn:
        conn.execute(
            """INSERT OR IGNORE INTO contacts
               (job_id, company, job_title, job_url, contact_email,
                status, date_contacted)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                str(record.get("job_id")),
                record.get("company"),
                record.get("job_title"),
                record.get("job_url"),
                record.get("contact_email", ""),
                record.get("status", "not contacted"),
                record.get("date_contacted", ""),
            ),
        )


def remove_contact(job_id):
    """Delete an outreach record by job_id."""
    _ensure_ready()
    with _connect() as conn:
        conn.execute("DELETE FROM contacts WHERE job_id = ?", (str(job_id),))


def get_all_contacts():
    """Return all outreach records, in insertion (rowid) order."""
    _ensure_ready()
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM contacts ORDER BY rowid").fetchall()
        return [dict(row) for row in rows]


def update_contact_email(job_id, email):
    """Set the contact_email for a tracked outreach record."""
    _ensure_ready()
    with _connect() as conn:
        conn.execute(
            "UPDATE contacts SET contact_email = ? WHERE job_id = ?",
            (email, str(job_id)),
        )


def update_contact_status(job_id, status, date_contacted=None):
    """Set the status (and optionally date_contacted) for an outreach record."""
    _ensure_ready()
    with _connect() as conn:
        if date_contacted is not None:
            conn.execute(
                "UPDATE contacts SET status = ?, date_contacted = ? WHERE job_id = ?",
                (status, date_contacted, str(job_id)),
            )
        else:
            conn.execute(
                "UPDATE contacts SET status = ? WHERE job_id = ?",
                (status, str(job_id)),
            )


# ---------------------------------------------------------------------------
# Search history
# ---------------------------------------------------------------------------

def add_search(keyword, location, results_found, new_found, entry_date):
    """Append one search-history entry."""
    _ensure_ready()
    with _connect() as conn:
        conn.execute(
            """INSERT INTO search_history
               (keyword, location, results_found, new_found, date)
               VALUES (?, ?, ?, ?, ?)""",
            (keyword, location, results_found, new_found, entry_date),
        )


def get_all_searches():
    """Return all search-history entries, oldest first."""
    _ensure_ready()
    with _connect() as conn:
        rows = conn.execute(
            "SELECT keyword, location, results_found, new_found, date "
            "FROM search_history ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]
