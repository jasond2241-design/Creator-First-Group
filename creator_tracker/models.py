"""Data schema for the creator-economy tracker.

A `Company` is seeded from the watchlist CSV. Everything downstream
(`FundingCheck`, `RevenueEstimate`, `EBITDAEstimate`) is derived from it and
rolled up into a `CompanyReport`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional


class Subsector(str, Enum):
    """Routes which revenue model a company is estimated with."""

    AGENCY = "agency"
    TALENT_MANAGEMENT = "talent_management"

    @classmethod
    def from_str(cls, value: str) -> "Subsector":
        normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
        try:
            return cls(normalized)
        except ValueError as exc:
            valid = ", ".join(s.value for s in cls)
            raise ValueError(f"Unknown subsector {value!r}; expected one of: {valid}") from exc


class Confidence(str, Enum):
    """Qualitative confidence flag attached to every derived estimate."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    @classmethod
    def weakest(cls, *values: "Confidence") -> "Confidence":
        """The overall confidence of a chain is only as strong as its weakest link."""
        order = {cls.HIGH: 2, cls.MEDIUM: 1, cls.LOW: 0}
        return min(values, key=lambda v: order[v])


# CSV columns a watchlist row may define. `name` and `subsector` are required;
# everything else is optional and depends on which subsector model applies.
CSV_REQUIRED_FIELDS = ("name", "subsector")
CSV_OPTIONAL_FIELDS = (
    "website",
    "cik",
    "headcount",
    "net_revenue_per_head",
    "roster_gmv",
    "commission_rate",
    "ebitda_margin_low",
    "ebitda_margin_high",
    "notes",
)


def _parse_optional_float(raw: Optional[str]) -> Optional[float]:
    if raw is None:
        return None
    raw = raw.strip()
    if raw == "":
        return None
    return float(raw.replace(",", "").replace("$", "").replace("%", ""))


@dataclass
class Company:
    """A row from the seed watchlist."""

    name: str
    subsector: Subsector
    website: Optional[str] = None
    cik: Optional[str] = None

    # Agency model inputs: revenue ~= headcount * net_revenue_per_head
    headcount: Optional[float] = None
    net_revenue_per_head: Optional[float] = None

    # Talent management model inputs: revenue ~= roster_gmv * commission_rate
    roster_gmv: Optional[float] = None
    commission_rate: Optional[float] = None

    # Optional manual override for the EBITDA margin band, e.g. from a data room
    # or public comp set. If provided, used verbatim with high confidence.
    ebitda_margin_low: Optional[float] = None
    ebitda_margin_high: Optional[float] = None

    notes: str = ""

    @staticmethod
    def from_csv_row(row: dict) -> "Company":
        missing = [f for f in CSV_REQUIRED_FIELDS if not (row.get(f) or "").strip()]
        if missing:
            raise ValueError(f"Watchlist row missing required field(s): {', '.join(missing)}: {row}")
        return Company(
            name=row["name"].strip(),
            subsector=Subsector.from_str(row["subsector"]),
            website=(row.get("website") or "").strip() or None,
            cik=(row.get("cik") or "").strip() or None,
            headcount=_parse_optional_float(row.get("headcount")),
            net_revenue_per_head=_parse_optional_float(row.get("net_revenue_per_head")),
            roster_gmv=_parse_optional_float(row.get("roster_gmv")),
            commission_rate=_parse_optional_float(row.get("commission_rate")),
            ebitda_margin_low=_parse_optional_float(row.get("ebitda_margin_low")),
            ebitda_margin_high=_parse_optional_float(row.get("ebitda_margin_high")),
            notes=(row.get("notes") or "").strip(),
        )


@dataclass
class FormDFiling:
    """A single Form D filing matched to a company on EDGAR full-text search."""

    accession_number: str
    entity_name: str
    cik: str
    file_date: Optional[date]
    match_quality: str  # "exact" | "fuzzy"
    url: str


@dataclass
class FundingCheck:
    """Result of checking a company against EDGAR for Form D filings."""

    company_name: str
    checked: bool
    form_d_filings: list = field(default_factory=list)  # list[FormDFiling]
    flagged_institutional_funding: bool = False
    confidence: Confidence = Confidence.LOW
    error: Optional[str] = None


@dataclass
class RevenueEstimate:
    """Output of a subsector-routed revenue model."""

    value: Optional[float]
    method: str  # "agency" | "talent_management"
    inputs_used: dict
    confidence: Confidence
    notes: str = ""


@dataclass
class EBITDAEstimate:
    """EBITDA expressed as a margin band applied to the revenue estimate."""

    margin_low: float
    margin_high: float
    value_low: Optional[float]
    value_high: Optional[float]
    confidence: Confidence
    source: str  # "override" | "subsector_default"


@dataclass
class CompanyReport:
    """Full rollup for one company, ready for output/filtering."""

    company: Company
    funding: FundingCheck
    revenue: RevenueEstimate
    ebitda: EBITDAEstimate
    qualifies: bool  # revenue estimate clears the $5M+ threshold
