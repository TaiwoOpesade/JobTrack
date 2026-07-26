"""
web/main.py
Minimal FastAPI web front-end for JobTrack's core loop: search Adzuna
listings, save favourites, track outreach. Reuses the existing api.py,
salary.py and db.py (via favorites.py / contacts.py) logic unchanged -
this module only adds routes and server-rendered HTML on top of them.

Adzuna credentials are read from environment variables (ADZUNA_APP_ID,
ADZUNA_APP_KEY), loaded from a local .env file if present. Never commit
a real .env - in production (e.g. Render) these are set as environment
variables in the dashboard instead.
"""

import os
import sys

# Make the project root (parent of this web/ package) importable, so this
# app can reuse api.py / salary.py / favorites.py / contacts.py / db.py
# regardless of the working directory uvicorn is started from.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import salary
from api import AdzunaAPIError, search_jobs
import contacts
import favorites

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

WEB_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="JobTrack")
app.mount("/static", StaticFiles(directory=os.path.join(WEB_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(WEB_DIR, "templates"))


@app.get("/")
def index():
    return RedirectResponse(url="/search")


@app.get("/search")
def search_page(request: Request, keyword: str = "", location: str = "", distance: int = 0):
    context = {
        "request": request,
        "active_page": "search",
        "keyword": keyword,
        "location": location,
        "distance": distance,
        "jobs": [],
        "saved_ids": set(),
        "tracked_ids": set(),
        "summary": None,
        "error": None,
    }

    if not keyword:
        return templates.TemplateResponse(request, "search.html", context)

    if not APP_ID or not APP_KEY:
        context["error"] = ("Missing ADZUNA_APP_ID / ADZUNA_APP_KEY. Set them as environment "
                             "variables (see README) before searching.")
        return templates.TemplateResponse(request, "search.html", context)

    if distance and not location:
        context["error"] = "Enter a location to filter by distance."
        return templates.TemplateResponse(request, "search.html", context)

    try:
        jobs = search_jobs(APP_ID, APP_KEY, keyword, location, distance=distance)
    except AdzunaAPIError as e:
        context["error"] = f"Error: {e}"
        return templates.TemplateResponse(request, "search.html", context)

    for job in jobs:
        job["hourly"] = salary.hourly_line(job)

    context["jobs"] = jobs
    context["saved_ids"] = {job["id"] for job in jobs if favorites.is_saved(job["id"])}
    context["tracked_ids"] = {job["id"] for job in jobs if contacts.is_tracked(job["id"])}
    context["summary"] = f"Found {len(jobs)} listings."
    if distance and location:
        context["summary"] = f"Found {len(jobs)} listings within {distance} km of {location}."

    return templates.TemplateResponse(request, "search.html", context)


@app.get("/favorites")
def favorites_page(request: Request):
    favs = favorites.load_favorites()
    for job in favs:
        job["hourly"] = salary.hourly_line(job)
    tracked_ids = {job["id"] for job in favs if contacts.is_tracked(job["id"])}

    return templates.TemplateResponse(request, "favorites.html", {
        "active_page": "favorites",
        "favorites": favs,
        "tracked_ids": tracked_ids,
        "error": None,
        "info": None,
    })


@app.post("/favorites")
def save_favorite(
    id: str = Form(...),
    title: str = Form(""),
    company: str = Form(""),
    location: str = Form(""),
    salary_min: str = Form(""),
    salary_max: str = Form(""),
    url: str = Form(""),
    description: str = Form(""),
    redirect_to: str = Form("/search"),
):
    def to_number(value):
        try:
            return float(value) if value else None
        except ValueError:
            return None

    favorites.save_listing({
        "id": id,
        "title": title,
        "company": company,
        "location": location,
        "salary_min": to_number(salary_min),
        "salary_max": to_number(salary_max),
        "url": url,
        "description": description,
    })
    return RedirectResponse(url=redirect_to or "/search", status_code=303)


@app.post("/favorites/{job_id}/remove")
def remove_favorite(job_id: str, redirect_to: str = Form("/favorites")):
    favorites.unsave_listing(job_id)
    return RedirectResponse(url=redirect_to or "/favorites", status_code=303)


@app.get("/outreach")
def outreach_page(request: Request):
    return templates.TemplateResponse(request, "outreach.html", {
        "active_page": "outreach",
        "contacts": contacts.load_contacts(),
        "statuses": contacts.VALID_STATUSES,
        "error": None,
        "info": None,
    })


@app.post("/outreach/track")
def track_employer(
    id: str = Form(...),
    title: str = Form(""),
    company: str = Form(""),
    url: str = Form(""),
    redirect_to: str = Form("/search"),
):
    contacts.track_employer({"id": id, "title": title, "company": company, "url": url})
    return RedirectResponse(url=redirect_to or "/search", status_code=303)


@app.post("/outreach/{job_id}/untrack")
def untrack_employer(job_id: str):
    contacts.untrack_employer(job_id)
    return RedirectResponse(url="/outreach", status_code=303)


@app.post("/outreach/{job_id}/email")
def update_contact_email(job_id: str, email: str = Form("")):
    contacts.set_contact_email(job_id, email)
    return RedirectResponse(url="/outreach", status_code=303)


@app.post("/outreach/{job_id}/status")
def update_contact_status(job_id: str, status: str = Form(...)):
    contacts.set_status(job_id, status)
    return RedirectResponse(url="/outreach", status_code=303)
