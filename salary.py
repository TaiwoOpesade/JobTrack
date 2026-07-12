"""
salary.py
Best-effort hourly-rate handling for job listings.

Adzuna normalises most advertised salaries to an annual figure and does not
say what period the pay was originally advertised in. So this module first
looks for an hourly rate quoted in the listing's own text (title +
description), and only estimates one from the annual salary when none is
advertised - clearly marked as an estimate.
"""

import re

# Standard UK full-time working year used for estimates
HOURS_PER_WEEK = 37.5
WEEKS_PER_YEAR = 52
HOURS_PER_YEAR = HOURS_PER_WEEK * WEEKS_PER_YEAR  # 1950

# "£12.50 per hour", "£11 - £13 an hour", "£12/hr", "£11.44 p/h", "£12 hourly"
_RATE_PATTERN = re.compile(
    r"£\s*(\d{1,3}(?:\.\d{1,2})?)"
    r"(?:\s*(?:-|–|to)\s*£?\s*(\d{1,3}(?:\.\d{1,2})?))?"
    r"\s*(?:per\s+hour|an\s+hour|/\s*hour|/\s*hr\b|p\s*/?\s*h\b|hourly|ph\b)",
    re.IGNORECASE,
)

# "hourly rate of £12.50" (amount comes after the words)
_RATE_OF_PATTERN = re.compile(
    r"hourly\s+rate\s+of\s+£\s*(\d{1,3}(?:\.\d{1,2})?)",
    re.IGNORECASE,
)


def extract_advertised_hourly(text):
    """
    Find an hourly rate quoted in a listing's text.

    Args:
        text (str): Any listing text, e.g. title + description.

    Returns:
        tuple or None: (low, high) floats if a rate was advertised, where
        high equals low for a single figure. None if no hourly rate found.
    """
    if not text:
        return None

    match = _RATE_PATTERN.search(text)
    if match:
        low = float(match.group(1))
        high = float(match.group(2)) if match.group(2) else low
        return (low, high)

    match = _RATE_OF_PATTERN.search(text)
    if match:
        rate = float(match.group(1))
        return (rate, rate)

    return None


def annual_to_hourly(annual):
    """
    Convert an annual salary to an estimated hourly rate.

    Args:
        annual (float): Annual salary in pounds.

    Returns:
        float: Estimated hourly rate assuming a 37.5-hour week, 52 weeks.
    """
    return annual / HOURS_PER_YEAR


def hourly_line(job):
    """
    Build the hourly-rate text for a job card.

    Checks whether the listing itself advertises an hourly rate; if not,
    estimates one from the annual salary figures.

    Args:
        job (dict): A job dict from api.search_jobs() (or a saved favourite),
                     with title, description, salary_min and salary_max keys.

    Returns:
        str: One of:
            "£12.50/hr (advertised)"          - rate quoted in the listing
            "£11.00 - £13.00/hr (advertised)" - advertised range
            "≈ £15.38/hr (est.)"              - estimated from annual salary
            ""                                 - no salary information at all
    """
    text = f"{job.get('title') or ''} {job.get('description') or ''}"
    advertised = extract_advertised_hourly(text)
    if advertised:
        low, high = advertised
        if low == high:
            return f"£{low:.2f}/hr (advertised)"
        return f"£{low:.2f} - £{high:.2f}/hr (advertised)"

    salary_min = job.get("salary_min")
    salary_max = job.get("salary_max")
    figures = [s for s in (salary_min, salary_max) if s]
    if not figures:
        return ""

    # A "yearly" figure this small is almost certainly already an hourly rate
    if max(figures) < 1000:
        low, high = min(figures), max(figures)
        if low == high:
            return f"£{low:.2f}/hr (advertised)"
        return f"£{low:.2f} - £{high:.2f}/hr (advertised)"

    low = annual_to_hourly(min(figures))
    high = annual_to_hourly(max(figures))
    if f"{low:.2f}" == f"{high:.2f}":
        return f"≈ £{low:.2f}/hr (est.)"
    return f"≈ £{low:.2f} - £{high:.2f}/hr (est.)"
