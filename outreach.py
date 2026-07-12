"""
outreach.py
Builds a personalised email draft for a tracked employer and hands it off
to your local mail client for manual review and sending. This module never
sends email itself - it only opens an unsent draft.
"""

import webbrowser
from urllib.parse import quote


def build_draft(contact, sender_name, background):
    """
    Build a personalised email draft for a tracked employer.

    Args:
        contact (dict): An outreach record from contacts.load_contacts(),
                         with at least company and job_title keys.
        sender_name (str): The name to sign the email with.
        background (str): A short line about the sender's background,
                            e.g. "a Year 12 student studying Maths, Physics and Computer Science".

    Returns:
        dict: A dict with "subject" and "body" string keys, fully
              personalised with no unfilled placeholders.
    """
    company = contact.get("company")
    job_title = contact.get("job_title")

    subject = f"Work experience enquiry - {job_title} at {company}"

    body = (
        f"Dear Hiring Team at {company},\n\n"
        f"My name is {sender_name} and I am {background}. "
        f"I recently came across your listing for the {job_title} role and it caught my interest, "
        f"so I wanted to reach out directly to ask whether {company} offers any work experience "
        f"placements or insight days for sixth-form students.\n\n"
        f"I would be very grateful for the opportunity to learn more about what the role involves "
        f"and how the team at {company} works day to day. I am happy to fit around whatever dates "
        f"or format would suit you best, even if that is just a short call or a few hours of shadowing.\n\n"
        f"Thank you for taking the time to read this - I would be happy to send over my CV if that "
        f"would be useful, and I look forward to hearing from you.\n\n"
        f"Kind regards,\n"
        f"{sender_name}"
    )

    return {"subject": subject, "body": body}


def open_in_mail_client(contact, subject, body):
    """
    Open a pre-filled, unsent email draft in the user's default mail client.

    Args:
        contact (dict): An outreach record from contacts.load_contacts(),
                         with a contact_email key to address the draft to.
        subject (str): The email subject line.
        body (str): The email body text.

    Returns:
        None. Opens a mailto: link via the OS default mail client; the
        message is never sent automatically and must be reviewed and sent
        by hand.
    """
    to_address = contact.get("contact_email", "")
    mailto_url = f"mailto:{to_address}?subject={quote(subject)}&body={quote(body)}"
    webbrowser.open(mailto_url)
