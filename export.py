"""
export.py
Exports tracked outreach records to a CSV file for use outside the app.
"""

import csv

from contacts import load_contacts

FIELDNAMES = ["company", "job_title", "status", "contact_email", "date_contacted", "job_url"]


def export_contacts_csv(path):
    """
    Write all tracked outreach records to a CSV file.

    Args:
        path (str): Filesystem path to write the CSV file to.

    Returns:
        None. Writes a CSV with headers:
            company, job_title, status, contact_email, date_contacted, job_url
    """
    contacts = load_contacts()

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for contact in contacts:
            writer.writerow({field: contact.get(field, "") for field in FIELDNAMES})
