"""Data schema for the congressional & presidential trade tracker.

Two sources feed this tracker, and they don't have the same fidelity:

- **Senate**: Periodic Transaction Reports (PTRs) filed under the STOCK Act
  via the Senate's Electronic Financial Disclosure system
  (efdsearch.senate.gov). These are itemized, ticker-level, filed within 45
  days of a trade -- represented here as `Trade` records.
- **Executive branch (President / Vice President)**: OGE Form 278e
  disclosures. These are annual filings, not itemized 45-day PTRs, and
  OGE's document host doesn't expose the line items as structured data --
  only an index of filings (name, title, date, agency, a document link).
  Represented here as `Filing` records, deliberately a different shape from
  `Trade` so callers can't mistake an index entry for a parsed trade.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional


class Chamber(str, Enum):
    SENATE = "senate"
    EXECUTIVE = "executive"  # President / Vice President


class Owner(str, Enum):
    SELF = "self"
    SPOUSE = "spouse"
    JOINT = "joint"
    DEPENDENT_CHILD = "dependent_child"
    UNKNOWN = "unknown"

    @classmethod
    def from_raw(cls, raw: str) -> "Owner":
        normalized = (raw or "").strip().lower()
        return {
            "self": cls.SELF,
            "sp": cls.SPOUSE,
            "spouse": cls.SPOUSE,
            "jt": cls.JOINT,
            "joint": cls.JOINT,
            "dc": cls.DEPENDENT_CHILD,
            "dependent child": cls.DEPENDENT_CHILD,
        }.get(normalized, cls.UNKNOWN)


class TransactionType(str, Enum):
    PURCHASE = "purchase"
    SALE_FULL = "sale_full"
    SALE_PARTIAL = "sale_partial"
    EXCHANGE = "exchange"
    UNKNOWN = "unknown"

    @classmethod
    def from_raw(cls, raw: str) -> "TransactionType":
        normalized = (raw or "").strip().lower()
        if normalized.startswith("purchase"):
            return cls.PURCHASE
        if normalized.startswith("sale"):
            return cls.SALE_PARTIAL if "partial" in normalized else cls.SALE_FULL
        if normalized.startswith("exchange"):
            return cls.EXCHANGE
        return cls.UNKNOWN


class ParseStatus(str, Enum):
    """How much of a filing's content this tracker actually extracted."""

    PARSED = "parsed"
    UNSUPPORTED_FORMAT = "unsupported_format"  # e.g. a scanned paper PTR (image/PDF)
    ERROR = "error"


@dataclass
class AmountRange:
    """STOCK Act disclosures report a bracketed range, not an exact amount."""

    raw: str
    low: Optional[float] = None
    high: Optional[float] = None


@dataclass
class Trade:
    """One itemized transaction line from a Senate Periodic Transaction Report."""

    politician_name: str
    chamber: Chamber
    office: str  # e.g. "Senator"
    owner: Owner
    transaction_date: Optional[date]
    ticker: Optional[str]
    asset_name: str
    asset_type: str
    transaction_type: TransactionType
    amount: AmountRange
    comment: str
    filing_id: str
    filing_url: str
    filing_date: Optional[date]


@dataclass
class Filing:
    """An index entry for an executive-branch (President/VP) OGE disclosure.

    Not itemized -- see the module docstring. `document_url` points to the
    source document (usually a PDF) for manual review.
    """

    filer_name: str
    title: str
    doc_type: str
    agency: str
    level: str
    doc_date: Optional[date]
    document_url: Optional[str]


@dataclass
class FilingFetchResult:
    """Outcome of trying to pull transactions out of one Senate PTR filing."""

    filing_id: str
    filing_url: str
    status: ParseStatus
    trades: list = field(default_factory=list)  # list[Trade]
    error: Optional[str] = None


@dataclass
class TrackerResult:
    """Combined output of a tracker run."""

    trades: list  # list[Trade] -- itemized Senate PTR transactions
    executive_filings: list  # list[Filing] -- executive-branch disclosure index
    senate_errors: list = field(default_factory=list)  # list[str]
    executive_error: Optional[str] = None
