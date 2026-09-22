"""Fetch -> combine -> filter pipeline tying the Senate and executive-branch
clients together into one `TrackerResult`."""

from __future__ import annotations

from datetime import date
from typing import List, Optional

import requests

from .executive_oge import ExecutiveDisclosureClient
from .models import Trade, TrackerResult
from .senate_efd import SenateEFDClient


def run_pipeline(
    user_agent: str,
    since: Optional[date] = None,
    until: Optional[date] = None,
    skip_senate: bool = False,
    skip_executive: bool = False,
    senate_client: Optional[SenateEFDClient] = None,
    executive_client: Optional[ExecutiveDisclosureClient] = None,
) -> TrackerResult:
    """Runs both trackers and returns a combined, unfiltered result -- use
    `filter_trades` to narrow it down for display."""
    trades: List[Trade] = []
    senate_errors: List[str] = []
    if not skip_senate:
        client = senate_client or SenateEFDClient(user_agent=user_agent)
        try:
            trades, senate_errors = client.get_trades(since=since, until=until)
        except requests.RequestException as exc:
            senate_errors = [f"Senate eFD search failed: {exc}"]

    executive_filings = []
    executive_error = None
    if not skip_executive:
        client = executive_client or ExecutiveDisclosureClient(user_agent=user_agent)
        try:
            executive_filings = client.get_president_and_vp_filings()
        except requests.RequestException as exc:
            executive_error = str(exc)

    return TrackerResult(
        trades=trades,
        executive_filings=executive_filings,
        senate_errors=senate_errors,
        executive_error=executive_error,
    )


def filter_trades(
    trades: List[Trade],
    politician: Optional[str] = None,
    ticker: Optional[str] = None,
) -> List[Trade]:
    result = trades
    if politician:
        needle = politician.strip().lower()
        result = [t for t in result if needle in t.politician_name.lower()]
    if ticker:
        needle = ticker.strip().upper()
        result = [t for t in result if (t.ticker or "").upper() == needle]
    return result
