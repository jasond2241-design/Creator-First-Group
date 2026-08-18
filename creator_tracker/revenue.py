"""Subsector-routed revenue estimation.

- agency: revenue ~= headcount x net revenue per head
- talent_management: revenue ~= roster GMV x commission rate
"""

from __future__ import annotations

from .models import Company, Confidence, RevenueEstimate, Subsector


def estimate_agency_revenue(company: Company) -> RevenueEstimate:
    inputs = {
        "headcount": company.headcount,
        "net_revenue_per_head": company.net_revenue_per_head,
    }
    if company.headcount is None or company.net_revenue_per_head is None:
        return RevenueEstimate(
            value=None,
            method=Subsector.AGENCY.value,
            inputs_used=inputs,
            confidence=Confidence.LOW,
            notes="Missing headcount and/or net_revenue_per_head; cannot estimate.",
        )
    if company.headcount <= 0 or company.net_revenue_per_head <= 0:
        return RevenueEstimate(
            value=None,
            method=Subsector.AGENCY.value,
            inputs_used=inputs,
            confidence=Confidence.LOW,
            notes="headcount and net_revenue_per_head must be positive.",
        )

    value = company.headcount * company.net_revenue_per_head
    return RevenueEstimate(
        value=value,
        method=Subsector.AGENCY.value,
        inputs_used=inputs,
        confidence=Confidence.HIGH,
        notes="revenue = headcount x net_revenue_per_head",
    )


def estimate_talent_management_revenue(company: Company) -> RevenueEstimate:
    inputs = {
        "roster_gmv": company.roster_gmv,
        "commission_rate": company.commission_rate,
    }
    if company.roster_gmv is None or company.commission_rate is None:
        return RevenueEstimate(
            value=None,
            method=Subsector.TALENT_MANAGEMENT.value,
            inputs_used=inputs,
            confidence=Confidence.LOW,
            notes="Missing roster_gmv and/or commission_rate; cannot estimate.",
        )
    if company.roster_gmv <= 0 or not (0 < company.commission_rate <= 1):
        return RevenueEstimate(
            value=None,
            method=Subsector.TALENT_MANAGEMENT.value,
            inputs_used=inputs,
            confidence=Confidence.LOW,
            notes="roster_gmv must be positive and commission_rate must be in (0, 1].",
        )

    value = company.roster_gmv * company.commission_rate
    return RevenueEstimate(
        value=value,
        method=Subsector.TALENT_MANAGEMENT.value,
        inputs_used=inputs,
        confidence=Confidence.HIGH,
        notes="revenue = roster_gmv x commission_rate",
    )


_ROUTES = {
    Subsector.AGENCY: estimate_agency_revenue,
    Subsector.TALENT_MANAGEMENT: estimate_talent_management_revenue,
}


def estimate_revenue(company: Company) -> RevenueEstimate:
    """Route to the correct model based on the company's subsector."""
    try:
        model = _ROUTES[company.subsector]
    except KeyError as exc:
        raise ValueError(f"No revenue model registered for subsector {company.subsector!r}") from exc
    return model(company)
