"""
api.py
Handles all communication with the Adzuna Job Search API.
Docs: https://developer.adzuna.com/overview
"""

import requests

BASE_URL = "https://api.adzuna.com/v1/api/jobs"


class AdzunaAPIError(Exception):
    """Raised when the Adzuna API returns an error or bad response."""
    pass


def search_jobs(app_id, app_key, keyword, location="", country="gb",
                 page=1, results_per_page=20, company="", distance=0):
    """
    Search Adzuna for job listings.

    Args:
        app_id (str): Your Adzuna App ID.
        app_key (str): Your Adzuna App Key.
        keyword (str): Search term, e.g. "python developer".
        location (str): Location filter - a place name or postcode,
            e.g. "london" or "LS1 4DY". Optional.
        country (str): Two-letter country code. Default "gb" (UK).
        page (int): Page number, starting at 1.
        results_per_page (int): Number of results per page (max 50).
        company (str): Only return listings from this employer. Optional.
        distance (int): Only return listings within this many kilometres of
            the location. 0 means no distance limit. Ignored when no
            location is given.

    Returns:
        list[dict]: A list of simplified job listing dictionaries with keys:
            id, title, company, location, salary_min, salary_max, url, description

    Raises:
        AdzunaAPIError: If the request fails or the API returns an error.
    """
    if not app_id or not app_key:
        raise AdzunaAPIError("Missing app_id or app_key. Get free credentials at "
                              "https://developer.adzuna.com/signup")

    url = f"{BASE_URL}/{country}/search/{page}"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": results_per_page,
        "content-type": "application/json",
    }
    if keyword:
        params["what"] = keyword
    if location:
        params["where"] = location
        if distance:
            params["distance"] = distance
    if company:
        params["company"] = company

    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.exceptions.RequestException as e:
        raise AdzunaAPIError(f"Network error contacting Adzuna: {e}")

    if response.status_code == 401:
        raise AdzunaAPIError("Invalid app_id or app_key. Double check your credentials.")
    if response.status_code != 200:
        raise AdzunaAPIError(f"Adzuna returned status {response.status_code}: {response.text[:200]}")

    data = response.json()
    results = data.get("results", [])

    jobs = []
    for job in results:
        title = job.get("title") or "Untitled"
        company = (job.get("company") or {}).get("display_name") or "Unknown company"
        location = (job.get("location") or {}).get("display_name") or "Unknown location"
        description = job.get("description") or ""

        jobs.append({
            "id": job.get("id"),
            "title": title.strip(),
            "company": company,
            "location": location,
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "url": job.get("redirect_url", ""),
            "description": description.strip(),
        })

    return jobs
