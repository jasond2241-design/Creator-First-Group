"""Seed -> check -> estimate -> filter pipeline."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import List, Optional

from .ebitda import estimate_ebitda
from .edgar import EdgarClient
from .models import Company, CompanyReport, FundingCheck
from .revenue import estimate_revenue

REVENUE_QUALIFY_THRESHOLD = 5_000_000


def load_watchlist(csv_path: str | Path) -> List[Company]:
    path = Path(csv_path)
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [Company.from_csv_row(row) for row in reader if any((v or "").strip() for v in row.values())]


def build_report(company: Company, funding: FundingCheck) -> CompanyReport:
    revenue = estimate_revenue(company)
    ebitda = estimate_ebitda(company, revenue)
    qualifies = revenue.value is not None and revenue.value >= REVENUE_QUALIFY_THRESHOLD
    return CompanyReport(company=company, funding=funding, revenue=revenue, ebitda=ebitda, qualifies=qualifies)


def run_pipeline(
    csv_path: str | Path,
    user_agent: str,
    edgar_client: Optional[EdgarClient] = None,
    skip_edgar: bool = False,
) -> List[CompanyReport]:
    """Load the watchlist, run the Form D check, estimate revenue/EBITDA,
    and return reports for every company (unfiltered -- use
    `qualifying(reports)` to apply the $5M+ threshold).
    """
    companies = load_watchlist(csv_path)
    client = edgar_client or (None if skip_edgar else EdgarClient(user_agent=user_agent))

    reports = []
    for company in companies:
        if skip_edgar or client is None:
            funding = FundingCheck(company_name=company.name, checked=False, error="EDGAR check skipped")
        else:
            funding = client.check_company(company)
        reports.append(build_report(company, funding))
    return reports


def qualifying(reports: List[CompanyReport]) -> List[CompanyReport]:
    """Reports whose revenue estimate clears the $5M+ threshold."""
    return [r for r in reports if r.qualifies]
