# JobTrack

A desktop job-hunting companion for students, built with Python and CustomTkinter.
JobTrack searches live UK job listings through the [Adzuna API](https://developer.adzuna.com),
keeps track of the listings and employers you care about, and helps you run a
polite, personal outreach campaign - every email is drafted for you to review
and send yourself, never sent automatically.

## Features

- **Search** - live Adzuna listings by keyword, with a location filter that
  accepts a place name (`London`) or a postcode (`LS1 4DY`), plus a maximum
  distance filter (5-100 km) applied server-side around that location.
  New listings since your last search are flagged with a 🆕 badge.
- **Hourly rates** - every card shows an hourly rate: quoted verbatim when the
  listing advertises one (`£12.50/hr (advertised)`), otherwise estimated from
  the annual salary on a 37.5-hour week (`≈ £15.38/hr (est.)`).
- **Saved listings** - save any result with ♡ and revisit it later; the Saved
  page has its own filter bar over title, company and location.
- **Saved employers** - follow employers you like and load all their current
  listings in a chosen area with one click.
- **Outreach tracker** - track employers you want to contact, record a contact
  email and status (not contacted / emailed / replied / rejected), and export
  the lot to CSV. "Draft email" builds a personalised work-experience enquiry
  and opens it in your own mail client as an **unsent draft** - you review and
  press send yourself. The app contains no email-sending code at all.
- **Home dashboard** - animated stat tiles, outreach progress rings and your
  recent searches at a glance.

## Tech stack

| Layer | Choice |
|---|---|
| Language | Python 3 |
| GUI | [CustomTkinter](https://customtkinter.tomschimansky.com) (animated, dark themed) |
| HTTP | requests |
| Config | python-dotenv (`.env` file) |
| Job data | Adzuna Job Search API (free tier) |
| Persistence | local JSON files - no database |

## Setup

1. **Install dependencies**

   ```
   pip install customtkinter requests python-dotenv
   ```

2. **Get free Adzuna credentials** at
   [developer.adzuna.com/signup](https://developer.adzuna.com/signup) -
   the dashboard shows your Application ID and Application Key.

3. **Create your `.env`** - copy the template and fill in your own values:

   ```
   copy .env.example .env
   ```

   ```
   ADZUNA_APP_ID=your_app_id_here
   ADZUNA_APP_KEY=your_app_key_here
   ```

   `.env` is listed in `.gitignore` - never commit the real file.

## Run

```
python main.py
```

If the credentials are missing the app prints a setup reminder instead of
launching, so a missing `.env` never crashes it.

## Testing

Automated tests cover `salary.py` (hourly-rate detection and estimation) and
`api.py` (Adzuna request building and response parsing). All HTTP calls are
mocked - no real network access or credentials are needed to run them.

```
pip install -r requirements-dev.txt
pytest
```

## Project structure

| File | Role |
|---|---|
| `main.py` | CustomTkinter GUI - pages, wiring and animations only |
| `api.py` | Adzuna API wrapper (keyword / location / postcode / distance / company) |
| `storage.py` | Remembers seen listings so new ones can be flagged |
| `favorites.py` | Saved listings |
| `employers.py` | Saved employers |
| `contacts.py` | Outreach records |
| `outreach.py` | Email draft builder - opens `mailto:` drafts, never sends |
| `export.py` | CSV export of outreach records |
| `history.py` | Search history |
| `stats.py` | Aggregates everything for the home dashboard |
| `salary.py` | Hourly-rate detection and estimation |

All generated data (`seen_jobs.json`, `favorites.json`, `outreach.json`, etc.)
is stored beside the code and ignored by git.
