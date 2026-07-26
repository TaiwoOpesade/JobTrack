# JobTrack

A desktop job-hunting companion for students, built with Python and CustomTkinter.
JobTrack searches live UK job listings through the [Adzuna API](https://developer.adzuna.com),
keeps track of the listings and employers you care about, and helps you run a
polite, personal outreach campaign - every email is drafted for you to review
and send yourself, never sent automatically.

A minimal web version of the core loop (search, save favourites, track
outreach) is also available, built with FastAPI - see
[Web app](#web-app) below.

**Live demo:** https://jobtrack-j081.onrender.com

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
| Web app | [FastAPI](https://fastapi.tiangolo.com) + Jinja2 server-rendered HTML, no JS framework |
| HTTP | requests |
| Config | python-dotenv (`.env` file) |
| Job data | Adzuna Job Search API (free tier) |
| Persistence | local SQLite database (`jobtrack.db`), via Python's built-in `sqlite3` |

## Setup

1. **Install dependencies** (covers both the desktop app and the web app)

   ```
   pip install -r requirements.txt
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

## Web app

A minimal FastAPI front-end covers the same core loop - search, saved
listings, outreach tracking - as plain server-rendered HTML (Jinja2, no JS
framework). It reuses `api.py`, `salary.py` and `db.py` (via `favorites.py`
and `contacts.py`) unchanged; the desktop app keeps working exactly as before.

```
uvicorn web.main:app --reload
```

Then open `http://127.0.0.1:8000`. It reads `ADZUNA_APP_ID` / `ADZUNA_APP_KEY`
from the same `.env` file as the desktop app, and shares the same
`jobtrack.db` - a listing saved from the web app shows up in the desktop app
and vice versa.

### Deploy (Render)

`render.yaml` deploys the web app to [Render](https://render.com)'s free tier:

1. Push this repo to GitHub (already done) and create a new **Blueprint**
   in Render pointing at it - Render reads `render.yaml` automatically.
2. In the Render dashboard, set the `ADZUNA_APP_ID` and `ADZUNA_APP_KEY`
   environment variables on the service (they're declared with `sync: false`
   in `render.yaml`, so Render prompts for them and never stores them in
   the repo).
3. Deploy. Render runs `pip install -r requirements.txt` then
   `uvicorn web.main:app --host 0.0.0.0 --port $PORT`.

Note: Render's free tier has an ephemeral filesystem, so `jobtrack.db` is
reset on each redeploy or restart - fine for a demo, but not durable storage.
Add a persistent disk (a paid Render feature) if you need saved data to
survive restarts.

## Known limitations

- The deployed demo's SQLite database (`jobtrack.db`) lives on Render's
  ephemeral free-tier disk, so saved listings, employers and outreach data
  reset whenever the service redeploys or spins down after inactivity. A
  managed database (e.g. Render's own Postgres, or a persistent disk) would
  fix this if durable storage is needed.

## Project structure

| File | Role |
|---|---|
| `main.py` | CustomTkinter GUI - pages, wiring and animations only |
| `api.py` | Adzuna API wrapper (keyword / location / postcode / distance / company) |
| `db.py` | SQLite access layer (`jobtrack.db`) - schema, one-time JSON import, all queries |
| `storage.py` | Remembers seen listings so new ones can be flagged |
| `favorites.py` | Saved listings |
| `employers.py` | Saved employers |
| `contacts.py` | Outreach records |
| `outreach.py` | Email draft builder - opens `mailto:` drafts, never sends |
| `export.py` | CSV export of outreach records |
| `history.py` | Search history |
| `stats.py` | Aggregates everything for the home dashboard |
| `salary.py` | Hourly-rate detection and estimation |
| `web/main.py` | FastAPI web app - search / favourites / outreach routes |
| `web/templates/` | Jinja2 HTML templates for the web app |
| `render.yaml` | Render deploy config for the web app |

All local data (seen listings, saved listings/employers, outreach records,
search history) lives in a single SQLite database, `jobtrack.db`, stored
beside the code and ignored by git. All reads and writes go through `db.py`;
`storage.py`, `favorites.py`, `employers.py`, `contacts.py` and `history.py`
keep their original public functions and just call into it.

If you're upgrading from an older version of JobTrack that used JSON files
(`seen_jobs.json`, `favorites.json`, `outreach.json`, `employers.json`,
`search_history.json`), the first run automatically imports any of those
files it finds into `jobtrack.db`. This happens once; the JSON files are
left on disk untouched afterwards and are no longer read or written to.
