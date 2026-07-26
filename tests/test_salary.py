"""
Tests for salary.py - advertised-rate detection and annual-to-hourly estimation.
"""

import salary


# ---------------------------------------------------------------------------
# extract_advertised_hourly
# ---------------------------------------------------------------------------

def test_extract_single_rate_per_hour():
    assert salary.extract_advertised_hourly("Pay is £12.50 per hour, weekly") == (12.5, 12.5)


def test_extract_range_an_hour():
    assert salary.extract_advertised_hourly("£11 - £13 an hour") == (11.0, 13.0)


def test_extract_slash_hr():
    assert salary.extract_advertised_hourly("£12/hr for weekends") == (12.0, 12.0)


def test_extract_p_per_h():
    assert salary.extract_advertised_hourly("£11.44 p/h plus holiday pay") == (11.44, 11.44)


def test_extract_hourly_word():
    assert salary.extract_advertised_hourly("£12 hourly, immediate start") == (12.0, 12.0)


def test_extract_rate_of_phrase():
    assert salary.extract_advertised_hourly("Offering an hourly rate of £12.50 to start") == (12.5, 12.5)


def test_extract_en_dash_range():
    assert salary.extract_advertised_hourly("£11–£13 an hour") == (11.0, 13.0)


def test_extract_no_rate_present():
    assert salary.extract_advertised_hourly("Competitive annual salary, great benefits") is None


def test_extract_empty_string():
    assert salary.extract_advertised_hourly("") is None


def test_extract_none_input():
    assert salary.extract_advertised_hourly(None) is None


def test_extract_malformed_currency_ignored():
    # No pound sign / no hourly keyword - should not match
    assert salary.extract_advertised_hourly("12.50 per hour") is None
    assert salary.extract_advertised_hourly("£12.50 per day") is None


# ---------------------------------------------------------------------------
# annual_to_hourly / the 37.5-hour-week assumption
# ---------------------------------------------------------------------------

def test_hours_per_year_assumption():
    assert salary.HOURS_PER_WEEK == 37.5
    assert salary.WEEKS_PER_YEAR == 52
    assert salary.HOURS_PER_YEAR == 1950


def test_annual_to_hourly_exact_division():
    assert salary.annual_to_hourly(1950) == 1.0


def test_annual_to_hourly_matches_documented_example():
    # salary.py's own docstring example: 30000/1950 rounds to 15.38
    assert round(salary.annual_to_hourly(30000), 2) == 15.38


def test_annual_to_hourly_zero():
    assert salary.annual_to_hourly(0) == 0.0


# ---------------------------------------------------------------------------
# hourly_line
# ---------------------------------------------------------------------------

def test_hourly_line_advertised_single_rate_from_description():
    job = {"title": "Retail Assistant", "description": "Pay: £12.50 per hour.",
           "salary_min": 25000, "salary_max": 25000}
    assert salary.hourly_line(job) == "£12.50/hr (advertised)"


def test_hourly_line_advertised_range():
    job = {"title": "Retail Assistant", "description": "£11 - £13 an hour depending on experience.",
           "salary_min": None, "salary_max": None}
    assert salary.hourly_line(job) == "£11.00 - £13.00/hr (advertised)"


def test_hourly_line_estimated_single_value():
    job = {"title": "Warehouse Operative", "description": "Great team, no hourly rate mentioned.",
           "salary_min": 30000, "salary_max": 30000}
    assert salary.hourly_line(job) == "≈ £15.38/hr (est.)"


def test_hourly_line_estimated_range():
    job = {"title": "Sales Assistant", "description": "Join our team.",
           "salary_min": 28000, "salary_max": 32000}
    assert salary.hourly_line(job) == "≈ £14.36 - £16.41/hr (est.)"


def test_hourly_line_no_salary_information():
    job = {"title": "Mystery Role", "description": "No pay details given.",
           "salary_min": None, "salary_max": None}
    assert salary.hourly_line(job) == ""


def test_hourly_line_missing_title_and_description_keys():
    job = {"salary_min": 30000, "salary_max": 30000}
    assert salary.hourly_line(job) == "≈ £15.38/hr (est.)"


def test_hourly_line_missing_salary_keys_entirely():
    job = {"title": "No Salary Field", "description": "Nothing here."}
    assert salary.hourly_line(job) == ""


def test_hourly_line_advertised_rate_takes_priority_over_annual():
    # Even though salary_min/max are present, an advertised hourly rate wins.
    job = {"title": "Cafe Assistant", "description": "£10 an hour guaranteed.",
           "salary_min": 40000, "salary_max": 40000}
    assert salary.hourly_line(job) == "£10.00/hr (advertised)"


def test_hourly_line_small_annual_figures_treated_as_already_hourly():
    # Documents existing behaviour: any salary figure under £1000 is assumed
    # to already be an hourly rate, and is (mis)labelled "(advertised)" even
    # though it came from salary_min/salary_max, not listing text.
    job = {"title": "Odd Listing", "description": "No rate stated in text.",
           "salary_min": 12.5, "salary_max": 12.5}
    assert salary.hourly_line(job) == "£12.50/hr (advertised)"


def test_hourly_line_small_annual_figures_range_treated_as_hourly():
    job = {"title": "Odd Listing", "description": "No rate stated in text.",
           "salary_min": 9, "salary_max": 11}
    assert salary.hourly_line(job) == "£9.00 - £11.00/hr (advertised)"


def test_hourly_line_zero_salary_min_is_silently_dropped():
    # Documents existing behaviour: `if s` treats 0 as falsy, so a genuine
    # salary_min of 0 is excluded from `figures` just like None would be.
    job = {"title": "Odd Listing", "description": "No rate stated in text.",
           "salary_min": 0, "salary_max": None}
    assert salary.hourly_line(job) == ""
