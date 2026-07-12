## Objective
Add an employer outreach tracker to my existing "Job Listing Tracker" Python desktop app: track which employers I've contacted about a job listing, and generate a personalised email draft I review and send MYSELF. This is a human-in-the-loop tool, not a bulk mailer.

## Context
Existing project (working, unit-tested, not yet run against the live API):
- job_tracker/main.py — CustomTkinter GUI, entry point, wiring only. Has JobTrackerApp class with run_search(), display_jobs(), add_job_card(), open_link().
- job_tracker/api.py — Adzuna API wrapper: search_jobs(app_id, app_key, keyword, location, country, page, results_per_page) returns list of dicts with keys: id, title, company, location, salary_min, salary_max, url, description. Raises AdzunaAPIError.
- job_tracker/storage.py — flag_new_jobs(jobs) adds an "is_new" bool to each job and persists seen IDs to seen_jobs.json. Also reset_seen_jobs().
- .env holds ADZUNA_APP_ID / ADZUNA_APP_KEY, loaded in main.py via python-dotenv. .env is gitignored. .gitignore already excludes .env, venv/, __pycache__, seen_jobs.json, search_history.json, favorites.json.

Stack is LOCKED: Python, CustomTkinter, requests, python-dotenv, local JSON files. No databases, no new third-party packages, no email-sending libraries.

Read main.py, api.py and storage.py in full before writing any code.

## Target State
1. Bug fix in api.py: title, description, company and location can come back as JSON null from Adzuna. Currently .strip() and .get() on those will raise AttributeError. Make the parsing null-safe without changing the returned dict's keys.

2. New file: contacts.py — persistence layer for outreach records, stored in outreach.json (same pattern as storage.py: module-level path, private _load/_save helpers, public functions with docstrings).
   Each record keys on the Adzuna job id and stores: job_id, company, job_title, job_url, contact_email (default ""), status (one of "not contacted", "emailed", "replied", "rejected" — default "not contacted"), date_contacted (default "").
   Public functions:
   - track_employer(job) — add a record from a job dict from api.search_jobs(); no-op if already tracked
   - untrack_employer(job_id)
   - load_contacts() — return all records
   - is_tracked(job_id)
   - set_contact_email(job_id, email)
   - set_status(job_id, status) — when status is set to "emailed", stamp date_contacted with today's date (YYYY-MM-DD)

3. New file: outreach.py — builds the email draft.
   - build_draft(contact, sender_name, background) — returns a dict with "subject" and "body" strings, personalised with the company name and job title. The body is a short, specific work-experience / application enquiry written as if from a UK sixth-form student. No placeholders left unfilled.
   - open_in_mail_client(contact, subject, body) — builds a mailto: URL (urllib.parse.quote for the subject and body) and opens it with webbrowser.open() so the message lands in my mail client as an UNSENT draft.
   - This module MUST NOT send email. No smtplib, no SMTP, no API sending, no automated loop over multiple contacts. One contact at a time, opened for manual review.

4. New file: export.py — export_contacts_csv(path) writes all outreach.json records to a CSV using the stdlib csv module (headers: company, job_title, status, contact_email, date_contacted, job_url).

5. main.py wiring only (no business logic in main.py):
   - Each job card gets a "Track employer" button that calls contacts.track_employer(job) and visually confirms (button text switches to "Tracked").
   - New "Outreach" button in the search bar that opens a CTkToplevel window listing tracked employers from contacts.load_contacts(), each row showing company, job title, status, and: an entry to type the contact email, a status dropdown (CTkOptionMenu with the four statuses), a "Draft email" button that calls outreach.build_draft() + open_in_mail_client(), and a "Remove" button.
   - The Outreach window has an "Export CSV" button calling export.export_contacts_csv().
   - "Draft email" must be disabled / show a message if contact_email is empty. I find contact emails MANUALLY from company careers pages — the app never scrapes or looks up email addresses.

6. Add outreach.json to .gitignore.

## Scope
- Work only in: job_tracker/api.py, job_tracker/main.py, and NEW files job_tracker/contacts.py, job_tracker/outreach.py, job_tracker/export.py, plus one line added to .gitignore.
- Do NOT touch: .env, .env.example, storage.py, seen_jobs.json.
- Do NOT modify search_jobs()'s signature or the keys of the dicts it returns.

## Constraints
- Match my existing code style exactly: module-level docstring at the top of each file, a docstring on every function (Args / Returns / Raises where relevant), NO type hints, clearly named variables, snake_case, same CustomTkinter patterns already used in main.py (.pack() layout, CTkFrame cards, ctk.CTkFont for headings).
- Stdlib only for the new modules (json, os, csv, datetime, urllib.parse, webbrowser). No new pip dependencies.
- Never hardcode credentials or write secrets into any committed file.
- Only make changes directly requested. Do not add features, abstractions, extra files, logging frameworks, or refactors beyond what is listed above.

## Hard prohibition
Do NOT build anything that sends email automatically, sends to multiple recipients, scrapes or enriches contact data, or integrates a contact database (Apollo.io or similar). Every email is drafted for one employer and sent by me by hand. If any instruction seems to require automated or bulk sending, stop and ask.

## Acceptance Criteria
- [ ] api.py parses a job payload with null title / description / company / location without raising
- [ ] contacts.py round-trips: track_employer() then load_contacts() returns the record; re-tracking the same job_id does not duplicate it
- [ ] set_status(job_id, "emailed") sets date_contacted to today's date
- [ ] outreach.py contains no smtplib import and no send call anywhere in the codebase (grep to confirm)
- [ ] build_draft() output contains the real company name and job title, no unfilled placeholders
- [ ] export.py produces a CSV with the six specified headers
- [ ] main.py imports contacts/outreach/export but contains no JSON, CSV, or email-body logic itself
- [ ] `python main.py` launches without error (a missing .env prints the existing startup error rather than crashing)

## Stop Conditions
Stop and ask before:
- Deleting any file
- Adding any pip dependency
- Editing .env, .env.example, or storage.py
- Changing the Adzuna API call or search_jobs() signature
- Writing anything that sends a message without my review

## Progress
After each completed step output: ✅ [what was done] — [file(s) affected]

## Session Strategy
New session. All the context you need is in this brief plus the three existing files — read them first.
