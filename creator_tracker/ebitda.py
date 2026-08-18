"""EBITDA estimation, expressed as a margin band applied to estimated revenue.

Without underlying financials, EBITDA can't be pinned to a point estimate --
it's expressed as [low, high] by applying a margin band to the revenue
estimate. The band comes from a per-company override in the watchlist CSV if
one was supplied (data-room figure, comp set, etc.), otherwise it falls back
to a subsector default. Either way the result is capped at "medium"
confidence, since a margin band is a heuristic, not a measurement -- "high"
is reserved for cases with an explicit override AND a high-confidence
revenue estimate.
"""

from __future__ import annotations

from .models import Company, Confidence, EBITDAEstimate, RevenueEstimate, Subsector

# (margin_low, margin_high) applied to revenue when no company-specific
# override is supplied. Rough bootstrapped-company benchmarks:
# agencies run leaner-margin/labor-heavy books; talent management is a
# commission pass-through model with less delivery cost, so it skews higher.
SUBSECTOR_MARGIN_BANDS = {
    Subsector.AGENCY: (0.12, 0.22),
    Subsector.TALENT_MANAGEMENT: (0.20, 0.35),
}


def estimate_ebitda(company: Company, revenue: RevenueEstimate) -> EBITDAEstimate:
    if company.ebitda_margin_low is not None and company.ebitda_margin_high is not None:
        margin_low, margin_high = company.ebitda_margin_low, company.ebitda_margin_high
        source = "override"
    else:
        margin_low, margin_high = SUBSECTOR_MARGIN_BANDS[company.subsector]
        source = "subsector_default"

    if revenue.value is None:
        return EBITDAEstimate(
            margin_low=margin_low,
            margin_high=margin_high,
            value_low=None,
            value_high=None,
            confidence=Confidence.LOW,
            source=source,
        )

    value_low = revenue.value * margin_low
    value_high = revenue.value * margin_high

    if source == "override" and revenue.confidence == Confidence.HIGH:
        confidence = Confidence.HIGH
    elif revenue.confidence == Confidence.LOW:
        confidence = Confidence.LOW
    else:
        confidence = Confidence.MEDIUM

    return EBITDAEstimate(
        margin_low=margin_low,
        margin_high=margin_high,
        value_low=value_low,
        value_high=value_high,
        confidence=confidence,
        source=source,
    )
