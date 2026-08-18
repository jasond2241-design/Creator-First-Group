"""Subsector-routed revenue estimation.

- agency: revenue ~= headcount x net revenue per head
- software: revenue ~= customers x annual revenue per customer (ARPU)
- performance_marketing: revenue ~= managed ad spend x fee rate
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


def estimate_software_revenue(company: Company) -> RevenueEstimate:
    inputs = {
        "customers": company.customers,
        "arpu": company.arpu,
    }
    if company.customers is None or company.arpu is None:
        return RevenueEstimate(
            value=None,
            method=Subsector.SOFTWARE.value,
            inputs_used=inputs,
            confidence=Confidence.LOW,
            notes="Missing customers and/or arpu; cannot estimate.",
        )
    if company.customers <= 0 or company.arpu <= 0:
        return RevenueEstimate(
            value=None,
            method=Subsector.SOFTWARE.value,
            inputs_used=inputs,
            confidence=Confidence.LOW,
            notes="customers and arpu must be positive.",
        )

    value = company.customers * company.arpu
    return RevenueEstimate(
        value=value,
        method=Subsector.SOFTWARE.value,
        inputs_used=inputs,
        confidence=Confidence.HIGH,
        notes="revenue = customers x arpu",
    )


def estimate_performance_marketing_revenue(company: Company) -> RevenueEstimate:
    inputs = {
        "managed_ad_spend": company.managed_ad_spend,
        "fee_rate": company.fee_rate,
    }
    if company.managed_ad_spend is None or company.fee_rate is None:
        return RevenueEstimate(
            value=None,
            method=Subsector.PERFORMANCE_MARKETING.value,
            inputs_used=inputs,
            confidence=Confidence.LOW,
            notes="Missing managed_ad_spend and/or fee_rate; cannot estimate.",
        )
    if company.managed_ad_spend <= 0 or not (0 < company.fee_rate <= 1):
        return RevenueEstimate(
            value=None,
            method=Subsector.PERFORMANCE_MARKETING.value,
            inputs_used=inputs,
            confidence=Confidence.LOW,
            notes="managed_ad_spend must be positive and fee_rate must be in (0, 1].",
        )

    value = company.managed_ad_spend * company.fee_rate
    return RevenueEstimate(
        value=value,
        method=Subsector.PERFORMANCE_MARKETING.value,
        inputs_used=inputs,
        confidence=Confidence.HIGH,
        notes="revenue = managed_ad_spend x fee_rate",
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
    Subsector.SOFTWARE: estimate_software_revenue,
    Subsector.PERFORMANCE_MARKETING: estimate_performance_marketing_revenue,
    Subsector.TALENT_MANAGEMENT: estimate_talent_management_revenue,
}


def estimate_revenue(company: Company) -> RevenueEstimate:
    """Route to the correct model based on the company's subsector."""
    try:
        model = _ROUTES[company.subsector]
    except KeyError as exc:
        raise ValueError(f"No revenue model registered for subsector {company.subsector!r}") from exc
    return model(company)
