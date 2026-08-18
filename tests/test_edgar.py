from datetime import date
from unittest.mock import MagicMock

import pytest

from creator_tracker.edgar import EdgarClient, normalize_name
from creator_tracker.models import Company, Confidence, Subsector

PATREON_RESPONSE = {
    "hits": {
        "hits": [
            {
                "_id": "0001739074-23-000007:primary_doc.xml",
                "_source": {
                    "ciks": ["0001860300"],
                    "display_names": ["Patreon, Inc.  (CIK 0001860300)"],
                    "file_date": "2023-10-31",
                    "adsh": "0001739074-23-000007",
                    "form": "D",
                },
            },
            {
                # A fund named after Patreon, not Patreon itself -- should be filtered out.
                "_id": "0002011405-24-000006:primary_doc.xml",
                "_source": {
                    "ciks": ["0002011463"],
                    "display_names": [
                        "Network VC Syndicate Fund LLC Series Patreon  (CIK 0002011463)"
                    ],
                    "file_date": "2024-03-18",
                    "adsh": "0002011405-24-000006",
                    "form": "D",
                },
            },
        ]
    }
}

GHOST_COLLISION_RESPONSE = {
    "hits": {
        "hits": [
            {
                # Unrelated companies that happen to start with the same
                # single generic word as the target -- must NOT match.
                "_id": "0001:primary_doc.xml",
                "_source": {
                    "ciks": ["0001111111"],
                    "display_names": ["Ghost Autonomy Inc.  (CIK 0001111111)"],
                    "file_date": "2024-01-01",
                    "adsh": "0001111111-24-000001",
                    "form": "D",
                },
            },
            {
                "_id": "0002:primary_doc.xml",
                "_source": {
                    "ciks": ["0002222222"],
                    "display_names": ["Ghost Locomotion Inc.  (CIK 0002222222)"],
                    "file_date": "2024-02-01",
                    "adsh": "0002222222-24-000001",
                    "form": "D",
                },
            },
        ]
    }
}

EMPTY_RESPONSE = {"hits": {"hits": []}}


def _client_with_response(payload: dict) -> EdgarClient:
    client = EdgarClient(user_agent="Test test@example.com", request_delay=0)
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = payload
    mock_resp.raise_for_status.return_value = None
    client.session.get = MagicMock(return_value=mock_resp)
    return client


def test_normalize_name_strips_suffixes_and_punctuation():
    assert normalize_name("Patreon, Inc.") == "patreon"
    assert normalize_name("Whalar Group LLC") == "whalar"


def test_requires_contactable_user_agent():
    with pytest.raises(ValueError):
        EdgarClient(user_agent="no-contact-info")


def test_search_form_d_filters_out_non_matching_filers():
    client = _client_with_response(PATREON_RESPONSE)
    filings = client.search_form_d("Patreon, Inc.")

    assert len(filings) == 1
    assert filings[0].entity_name == "Patreon, Inc."
    assert filings[0].match_quality == "exact"
    assert filings[0].file_date == date(2023, 10, 31)
    assert filings[0].cik == "0001860300"
    assert "1860300" in filings[0].url  # EDGAR archive URLs use the un-padded CIK


def test_check_company_flags_institutional_funding():
    client = _client_with_response(PATREON_RESPONSE)
    company = Company(name="Patreon, Inc.", subsector=Subsector.AGENCY)

    result = client.check_company(company)

    assert result.checked is True
    assert result.flagged_institutional_funding is True
    assert result.confidence == Confidence.HIGH
    assert len(result.form_d_filings) == 1


def test_single_token_name_rejects_prefix_collisions():
    """Regression test: 'Ghost' is a token-prefix of 'Ghost Autonomy Inc.'
    and 'Ghost Locomotion Inc.', both unrelated companies -- a single
    generic word shouldn't fuzzy-match against longer unrelated names.
    """
    client = _client_with_response(GHOST_COLLISION_RESPONSE)
    filings = client.search_form_d("Ghost")
    assert filings == []


def test_check_company_no_filings_found():
    client = _client_with_response(EMPTY_RESPONSE)
    company = Company(name="Chameleon Collective", subsector=Subsector.AGENCY)

    result = client.check_company(company)

    assert result.checked is True
    assert result.flagged_institutional_funding is False
    assert result.confidence == Confidence.HIGH
    assert result.form_d_filings == []


def test_get_retries_once_on_server_error():
    client = EdgarClient(user_agent="Test test@example.com", request_delay=0)
    error_resp = MagicMock()
    error_resp.status_code = 500
    ok_resp = MagicMock()
    ok_resp.status_code = 200
    ok_resp.json.return_value = EMPTY_RESPONSE
    ok_resp.raise_for_status.return_value = None
    client.session.get = MagicMock(side_effect=[error_resp, ok_resp])

    filings = client.search_form_d("Some Company")

    assert filings == []
    assert client.session.get.call_count == 2


def test_check_company_handles_request_errors():
    import requests

    client = EdgarClient(user_agent="Test test@example.com", request_delay=0)
    client.session.get = MagicMock(side_effect=requests.RequestException("boom"))
    company = Company(name="Whalar Group", subsector=Subsector.AGENCY)

    result = client.check_company(company)

    assert result.checked is False
    assert result.error == "boom"
