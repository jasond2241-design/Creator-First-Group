import pytest

from creator_tracker.models import Company, Confidence, Subsector


def test_subsector_from_str_normalizes():
    assert Subsector.from_str("Talent Management") == Subsector.TALENT_MANAGEMENT
    assert Subsector.from_str("agency") == Subsector.AGENCY
    with pytest.raises(ValueError):
        Subsector.from_str("nonsense")


def test_company_from_csv_row_requires_name_and_subsector():
    with pytest.raises(ValueError):
        Company.from_csv_row({"name": "", "subsector": "agency"})
    with pytest.raises(ValueError):
        Company.from_csv_row({"name": "Foo", "subsector": ""})


def test_company_from_csv_row_parses_numbers():
    row = {
        "name": "Foo",
        "subsector": "agency",
        "headcount": "150",
        "net_revenue_per_head": "$200,000",
    }
    company = Company.from_csv_row(row)
    assert company.headcount == 150
    assert company.net_revenue_per_head == 200_000


def test_confidence_weakest():
    assert Confidence.weakest(Confidence.HIGH, Confidence.LOW) == Confidence.LOW
    assert Confidence.weakest(Confidence.HIGH, Confidence.MEDIUM) == Confidence.MEDIUM
    assert Confidence.weakest(Confidence.HIGH, Confidence.HIGH) == Confidence.HIGH
