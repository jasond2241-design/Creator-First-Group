from datetime import date
from unittest.mock import MagicMock

import pytest
import requests

from trade_tracker.executive_oge import (
    ExecutiveDisclosureClient,
    _extract_document_url,
    _parse_oge_date,
    _strip_tags,
)

PRESIDENT_PAGE = {
    "recordsFiltered": 1,
    "data": [
        {
            "docDate": "2026-05-15",
            "title": "President - Annual Report",
            "type": "New Filing <a href='https://extapps2.oge.gov/201/Presiden.nsf/201 Request?OpenForm&Filer=DOE'>view</a>",
            "name": "Doe, John",
            "agency": "The White House",
            "level": "President",
        }
    ],
}

VP_PAGE = {
    "recordsFiltered": 1,
    "data": [
        {
            "docDate": "2026-05-10",
            "title": "Vice President - Annual Report",
            "type": "New Filing",
            "name": "Roe, Jane",
            "agency": "Office of the Vice President",
            "level": "Vice President",
        }
    ],
}

EMPTY_PAGE = {"recordsFiltered": 0, "data": []}


def test_requires_contactable_user_agent():
    with pytest.raises(ValueError):
        ExecutiveDisclosureClient(user_agent="no-contact-info")


def test_strip_tags():
    assert _strip_tags("New Filing <a href='x'>view</a>") == "New Filing view"


def test_extract_document_url_present_and_absent():
    assert _extract_document_url("New Filing <a href='https://example.com/doc'>view</a>") == "https://example.com/doc"
    assert _extract_document_url("New Filing") is None


def test_parse_oge_date():
    assert _parse_oge_date("2026-05-15") == date(2026, 5, 15)
    assert _parse_oge_date(None) is None
    assert _parse_oge_date("garbage") is None


def _client_with_session():
    client = ExecutiveDisclosureClient(user_agent="Test test@example.com")
    client.session = MagicMock()
    return client


def test_search_filings_parses_rows_and_pulls_embedded_link():
    client = _client_with_session()
    resp = MagicMock()
    resp.json.return_value = PRESIDENT_PAGE
    resp.raise_for_status.return_value = None
    client.session.get.return_value = resp

    filings = client.search_filings(name_query="President")

    assert len(filings) == 1
    f = filings[0]
    assert f.filer_name == "Doe, John"
    assert f.level == "President"
    assert f.doc_date == date(2026, 5, 15)
    assert f.document_url == "https://extapps2.oge.gov/201/Presiden.nsf/201 Request?OpenForm&Filer=DOE"
    assert "New Filing" in f.doc_type
    assert "<a" not in f.doc_type


def test_get_president_and_vp_filings_dedupes_and_sorts_desc():
    client = _client_with_session()
    resp_president = MagicMock()
    resp_president.json.return_value = PRESIDENT_PAGE
    resp_president.raise_for_status.return_value = None
    resp_vp = MagicMock()
    resp_vp.json.return_value = VP_PAGE
    resp_vp.raise_for_status.return_value = None
    client.session.get.side_effect = [resp_president, resp_vp]

    filings = client.get_president_and_vp_filings()

    assert len(filings) == 2
    assert filings[0].doc_date == date(2026, 5, 15)  # newest first
    assert filings[1].doc_date == date(2026, 5, 10)


def test_search_filings_surfaces_request_errors_rather_than_hiding_them():
    client = _client_with_session()
    client.session.get.side_effect = requests.ConnectionError("connection reset by peer")

    with pytest.raises(requests.RequestException):
        client.search_filings()
