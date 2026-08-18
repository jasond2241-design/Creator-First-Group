from creator_tracker.models import Company, Confidence, Subsector
from creator_tracker.revenue import estimate_revenue


def test_agency_revenue_estimate():
    company = Company(
        name="Whalar", subsector=Subsector.AGENCY, headcount=180, net_revenue_per_head=220_000
    )
    result = estimate_revenue(company)
    assert result.value == 180 * 220_000
    assert result.confidence == Confidence.HIGH
    assert result.method == "agency"


def test_agency_revenue_missing_inputs():
    company = Company(name="Cameo", subsector=Subsector.AGENCY)
    result = estimate_revenue(company)
    assert result.value is None
    assert result.confidence == Confidence.LOW


def test_talent_management_revenue_estimate():
    company = Company(
        name="Underscore Talent",
        subsector=Subsector.TALENT_MANAGEMENT,
        roster_gmv=15_000_000,
        commission_rate=0.20,
    )
    result = estimate_revenue(company)
    assert result.value == 3_000_000
    assert result.confidence == Confidence.HIGH
    assert result.method == "talent_management"


def test_software_revenue_estimate():
    company = Company(
        name="Kit", subsector=Subsector.SOFTWARE, customers=40_000, arpu=300
    )
    result = estimate_revenue(company)
    assert result.value == 40_000 * 300
    assert result.confidence == Confidence.HIGH
    assert result.method == "software"


def test_software_revenue_missing_inputs():
    company = Company(name="Kit", subsector=Subsector.SOFTWARE)
    result = estimate_revenue(company)
    assert result.value is None
    assert result.confidence == Confidence.LOW


def test_performance_marketing_revenue_estimate():
    company = Company(
        name="Ubiquitous",
        subsector=Subsector.PERFORMANCE_MARKETING,
        managed_ad_spend=20_000_000,
        fee_rate=0.15,
    )
    result = estimate_revenue(company)
    assert result.value == 3_000_000
    assert result.confidence == Confidence.HIGH
    assert result.method == "performance_marketing"


def test_performance_marketing_invalid_fee_rate():
    company = Company(
        name="Bad Co",
        subsector=Subsector.PERFORMANCE_MARKETING,
        managed_ad_spend=1_000_000,
        fee_rate=1.5,
    )
    result = estimate_revenue(company)
    assert result.value is None
    assert result.confidence == Confidence.LOW


def test_talent_management_invalid_commission_rate():
    company = Company(
        name="Bad Co",
        subsector=Subsector.TALENT_MANAGEMENT,
        roster_gmv=1_000_000,
        commission_rate=1.5,
    )
    result = estimate_revenue(company)
    assert result.value is None
    assert result.confidence == Confidence.LOW
