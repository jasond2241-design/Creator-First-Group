from pathlib import Path

from creator_tracker.models import Confidence, FundingCheck
from creator_tracker.pipeline import REVENUE_QUALIFY_THRESHOLD, build_report, load_watchlist, qualifying

FIXTURE_CSV = Path(__file__).parent / "fixtures" / "watchlist.csv"


def test_load_watchlist_parses_rows_and_types():
    companies = load_watchlist(FIXTURE_CSV)
    assert len(companies) == 3

    agency = next(c for c in companies if c.name == "Big Agency")
    assert agency.headcount == 200
    assert agency.net_revenue_per_head == 200_000

    talent = next(c for c in companies if c.name == "Small Talent Shop")
    assert talent.roster_gmv == 1_000_000
    assert talent.commission_rate == 0.2


def test_qualifying_filters_below_threshold():
    companies = load_watchlist(FIXTURE_CSV)
    funding = FundingCheck(company_name="x", checked=False)
    reports = [build_report(c, funding) for c in companies]

    result = qualifying(reports)

    names = {r.company.name for r in result}
    assert "Big Agency" in names  # 200 * 200,000 = $40M
    assert "Small Talent Shop" not in names  # 1,000,000 * 0.2 = $200k
    for r in result:
        assert r.revenue.value >= REVENUE_QUALIFY_THRESHOLD
