import pytest

from creator_tracker.ebitda import estimate_ebitda
from creator_tracker.models import Company, Confidence, RevenueEstimate, Subsector


def test_ebitda_uses_subsector_default_band():
    company = Company(name="Whalar", subsector=Subsector.AGENCY)
    revenue = RevenueEstimate(
        value=10_000_000, method="agency", inputs_used={}, confidence=Confidence.HIGH
    )
    result = estimate_ebitda(company, revenue)
    assert result.source == "subsector_default"
    assert result.value_low == pytest.approx(10_000_000 * 0.12)
    assert result.value_high == pytest.approx(10_000_000 * 0.22)
    assert result.confidence == Confidence.MEDIUM


def test_ebitda_uses_override_band_with_high_confidence():
    company = Company(
        name="Underscore Talent",
        subsector=Subsector.TALENT_MANAGEMENT,
        ebitda_margin_low=0.25,
        ebitda_margin_high=0.30,
    )
    revenue = RevenueEstimate(
        value=5_000_000, method="talent_management", inputs_used={}, confidence=Confidence.HIGH
    )
    result = estimate_ebitda(company, revenue)
    assert result.source == "override"
    assert result.value_low == 1_250_000
    assert result.value_high == 1_500_000
    assert result.confidence == Confidence.HIGH


def test_ebitda_low_confidence_when_revenue_missing():
    company = Company(name="Cameo", subsector=Subsector.AGENCY)
    revenue = RevenueEstimate(value=None, method="agency", inputs_used={}, confidence=Confidence.LOW)
    result = estimate_ebitda(company, revenue)
    assert result.value_low is None
    assert result.value_high is None
    assert result.confidence == Confidence.LOW
