"""
Tests for api.py - Adzuna request building and response parsing.

No real network calls are made: requests.get is always mocked.
"""

import pytest
import requests

import api


class FakeResponse:
    """Minimal stand-in for requests.Response."""

    def __init__(self, status_code=200, json_data=None, text=""):
        self.status_code = status_code
        self._json_data = json_data if json_data is not None else {}
        self.text = text

    def json(self):
        return self._json_data


SAMPLE_PAYLOAD = {
    "results": [
        {
            "id": "111",
            "title": "  Retail Assistant  ",
            "company": {"display_name": "Acme Ltd"},
            "location": {"display_name": "London, UK"},
            "salary_min": 20000,
            "salary_max": 24000,
            "redirect_url": "https://example.com/jobs/111",
            "description": "  Great role.  ",
        },
        {
            "id": "222",
            "title": "Warehouse Operative",
            "company": {"display_name": "Beta Co"},
            "location": {"display_name": "Leeds, UK"},
            "salary_min": 21000,
            "salary_max": 21000,
            "redirect_url": "https://example.com/jobs/222",
            "description": "Immediate start.",
        },
    ]
}


# ---------------------------------------------------------------------------
# Missing credentials - no HTTP call should ever happen
# ---------------------------------------------------------------------------

def test_missing_app_id_raises_without_calling_requests(mocker):
    mock_get = mocker.patch("api.requests.get")
    with pytest.raises(api.AdzunaAPIError):
        api.search_jobs("", "key", "python")
    mock_get.assert_not_called()


def test_missing_app_key_raises_without_calling_requests(mocker):
    mock_get = mocker.patch("api.requests.get")
    with pytest.raises(api.AdzunaAPIError):
        api.search_jobs("id", "", "python")
    mock_get.assert_not_called()


# ---------------------------------------------------------------------------
# Query parameter / URL assembly
# ---------------------------------------------------------------------------

def test_keyword_only_builds_expected_params(mocker):
    mock_get = mocker.patch("api.requests.get", return_value=FakeResponse(json_data={"results": []}))
    api.search_jobs("app_id", "app_key", "python developer")

    args, kwargs = mock_get.call_args
    assert args[0] == "https://api.adzuna.com/v1/api/jobs/gb/search/1"
    params = kwargs["params"]
    assert params["app_id"] == "app_id"
    assert params["app_key"] == "app_key"
    assert params["results_per_page"] == 20
    assert params["content-type"] == "application/json"
    assert params["what"] == "python developer"
    assert "where" not in params
    assert "distance" not in params
    assert "company" not in params


def test_location_without_distance_omits_distance_param(mocker):
    mock_get = mocker.patch("api.requests.get", return_value=FakeResponse(json_data={"results": []}))
    api.search_jobs("app_id", "app_key", "chef", location="london")

    params = mock_get.call_args.kwargs["params"]
    assert params["where"] == "london"
    assert "distance" not in params


def test_location_with_distance_includes_both(mocker):
    mock_get = mocker.patch("api.requests.get", return_value=FakeResponse(json_data={"results": []}))
    api.search_jobs("app_id", "app_key", "chef", location="london", distance=15)

    params = mock_get.call_args.kwargs["params"]
    assert params["where"] == "london"
    assert params["distance"] == 15


def test_postcode_location_passed_through_verbatim(mocker):
    mock_get = mocker.patch("api.requests.get", return_value=FakeResponse(json_data={"results": []}))
    api.search_jobs("app_id", "app_key", "chef", location="LS1 4DY", distance=10)

    params = mock_get.call_args.kwargs["params"]
    assert params["where"] == "LS1 4DY"
    assert params["distance"] == 10


def test_distance_ignored_when_no_location(mocker):
    mock_get = mocker.patch("api.requests.get", return_value=FakeResponse(json_data={"results": []}))
    api.search_jobs("app_id", "app_key", "chef", location="", distance=10)

    params = mock_get.call_args.kwargs["params"]
    assert "where" not in params
    assert "distance" not in params


def test_company_filter_included(mocker):
    mock_get = mocker.patch("api.requests.get", return_value=FakeResponse(json_data={"results": []}))
    api.search_jobs("app_id", "app_key", "", company="Tesco")

    params = mock_get.call_args.kwargs["params"]
    assert params["company"] == "Tesco"
    assert "what" not in params


def test_page_and_country_build_correct_url(mocker):
    mock_get = mocker.patch("api.requests.get", return_value=FakeResponse(json_data={"results": []}))
    api.search_jobs("app_id", "app_key", "chef", country="us", page=3)

    args, _ = mock_get.call_args
    assert args[0] == "https://api.adzuna.com/v1/api/jobs/us/search/3"


def test_custom_results_per_page(mocker):
    mock_get = mocker.patch("api.requests.get", return_value=FakeResponse(json_data={"results": []}))
    api.search_jobs("app_id", "app_key", "chef", results_per_page=50)

    params = mock_get.call_args.kwargs["params"]
    assert params["results_per_page"] == 50


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

def test_parses_sample_payload_into_expected_structure(mocker):
    mocker.patch("api.requests.get", return_value=FakeResponse(json_data=SAMPLE_PAYLOAD))

    jobs = api.search_jobs("app_id", "app_key", "retail")

    assert jobs == [
        {
            "id": "111",
            "title": "Retail Assistant",
            "company": "Acme Ltd",
            "location": "London, UK",
            "salary_min": 20000,
            "salary_max": 24000,
            "url": "https://example.com/jobs/111",
            "description": "Great role.",
        },
        {
            "id": "222",
            "title": "Warehouse Operative",
            "company": "Beta Co",
            "location": "Leeds, UK",
            "salary_min": 21000,
            "salary_max": 21000,
            "url": "https://example.com/jobs/222",
            "description": "Immediate start.",
        },
    ]


def test_parses_missing_optional_fields_with_fallbacks(mocker):
    payload = {
        "results": [
            {
                "id": "333",
                # title missing entirely
                # company missing entirely
                # location missing entirely
                # description missing entirely
                "salary_min": None,
                "salary_max": None,
                # redirect_url missing entirely
            }
        ]
    }
    mocker.patch("api.requests.get", return_value=FakeResponse(json_data=payload))

    jobs = api.search_jobs("app_id", "app_key", "anything")

    assert jobs == [
        {
            "id": "333",
            "title": "Untitled",
            "company": "Unknown company",
            "location": "Unknown location",
            "salary_min": None,
            "salary_max": None,
            "url": "",
            "description": "",
        }
    ]


def test_empty_results_payload_returns_empty_list(mocker):
    mocker.patch("api.requests.get", return_value=FakeResponse(json_data={"results": []}))
    assert api.search_jobs("app_id", "app_key", "no matches for this") == []


def test_missing_results_key_returns_empty_list(mocker):
    mocker.patch("api.requests.get", return_value=FakeResponse(json_data={}))
    assert api.search_jobs("app_id", "app_key", "anything") == []


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

def test_non_200_response_raises_with_status_and_body(mocker):
    mocker.patch("api.requests.get", return_value=FakeResponse(status_code=500, text="Internal Server Error"))

    with pytest.raises(api.AdzunaAPIError) as excinfo:
        api.search_jobs("app_id", "app_key", "chef")

    assert "500" in str(excinfo.value)
    assert "Internal Server Error" in str(excinfo.value)


def test_401_response_raises_invalid_credentials_message(mocker):
    mocker.patch("api.requests.get", return_value=FakeResponse(status_code=401, text="Unauthorized"))

    with pytest.raises(api.AdzunaAPIError) as excinfo:
        api.search_jobs("app_id", "app_key", "chef")

    assert "Invalid app_id or app_key" in str(excinfo.value)


def test_network_error_raises_adzuna_api_error(mocker):
    mocker.patch("api.requests.get", side_effect=requests.exceptions.ConnectionError("boom"))

    with pytest.raises(api.AdzunaAPIError) as excinfo:
        api.search_jobs("app_id", "app_key", "chef")

    assert "Network error contacting Adzuna" in str(excinfo.value)
