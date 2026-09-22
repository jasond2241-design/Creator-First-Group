"""Client for the Senate's Electronic Financial Disclosure (eFD) system.

This is the live, itemized, ticker-level source of senator stock trades:
Periodic Transaction Reports (PTRs), which the STOCK Act requires senators
to file within 30-45 days of a covered transaction.

The site (efdsearch.senate.gov) gates its search behind a one-time
"prohibition agreement" click that sets a session cookie, then serves
results from a Django/DataTables JSON endpoint. Flow:

1. GET  /search/home/           -> csrftoken cookie + csrfmiddlewaretoken
2. POST /search/home/           -> accept the agreement, sets sessionid
3. GET  /search/                -> fresh csrfmiddlewaretoken for the search form
4. POST /search/report/data/    -> DataTables JSON: rows of
                                    [first_name, last_name, office, report_link_html, filed_date]

Each PTR's own transactions live at /search/view/ptr/<id>/ as an HTML
table. Older filings that were submitted on paper are scanned images
instead (/search/view/paper/<id>/) and have no structured data to parse --
those are surfaced as `ParseStatus.UNSUPPORTED_FORMAT` rather than silently
dropped.
"""

from __future__ import annotations

import re
import time
from datetime import date, datetime
from html.parser import HTMLParser
from typing import List, Optional

import requests

from .models import (
    AmountRange,
    Chamber,
    FilingFetchResult,
    Owner,
    ParseStatus,
    Trade,
    TransactionType,
)

BASE_URL = "https://efdsearch.senate.gov"
HOME_URL = f"{BASE_URL}/search/home/"
SEARCH_URL = f"{BASE_URL}/search/"
DATA_URL = f"{BASE_URL}/search/report/data/"

REPORT_TYPE_PTR = 11

DEFAULT_REQUEST_DELAY_SECONDS = 0.5
DEFAULT_PAGE_LENGTH = 100
_AMOUNT_NUM_RE = re.compile(r"\$?([\d,]+(?:\.\d+)?)")
_CSRF_RE = re.compile(r'csrfmiddlewaretoken"\s+value="([^"]+)"')
_LINK_RE = re.compile(r'href="(/search/view/(ptr|paper)/[a-f0-9\-]+/)"')


def _parse_amount(raw: str) -> AmountRange:
    raw = (raw or "").strip()
    if not raw or raw == "--":
        return AmountRange(raw=raw)
    numbers = [float(n.replace(",", "")) for n in _AMOUNT_NUM_RE.findall(raw)]
    if not numbers:
        return AmountRange(raw=raw)
    if len(numbers) == 1:
        if "over" in raw.lower() or "+" in raw:
            return AmountRange(raw=raw, low=numbers[0], high=None)
        return AmountRange(raw=raw, low=numbers[0], high=numbers[0])
    return AmountRange(raw=raw, low=numbers[0], high=numbers[1])


def _parse_date(raw: str) -> Optional[date]:
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        return datetime.strptime(raw, "%m/%d/%Y").date()
    except ValueError:
        return None


class _TransactionTableParser(HTMLParser):
    """Pulls rows out of the PTR detail page's `<table class="table ...">`.

    Only the *direct* text of each `<td>` is kept as that cell's value --
    the Asset Name column nests extra `<div>`s with issuer location/
    description, and we only want the primary name, not that nested text
    glued on. `_cell_stack` tracks tags opened inside the current `<td>` so
    nested elements (however deep) don't get mistaken for the cell closing.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows: List[List[str]] = []
        self._in_table = False
        self._in_tbody = False
        self._table_depth = 0
        self._row: Optional[List[str]] = None
        self._cell_chunks: Optional[List[str]] = None
        self._cell_stack: List[str] = []
        # Stack depth (into _cell_stack) at which a "text-muted" element was
        # opened -- e.g. the Asset Name column's issuer-location/description
        # aside. None means we're not inside one. Text inside is skipped;
        # everything else in the cell (including e.g. an <a> wrapping a
        # ticker symbol) is captured regardless of nesting depth.
        self._muted_from: Optional[int] = None

    def handle_starttag(self, tag, attrs):
        if not self._in_table:
            if tag == "table" and "table" in dict(attrs).get("class", "").split():
                self._in_table = True
                self._table_depth = 1
            return
        if tag == "table":
            self._table_depth += 1
            return
        if tag == "tbody":
            self._in_tbody = True
            return
        if self._cell_chunks is not None:
            self._cell_stack.append(tag)
            if self._muted_from is None and "text-muted" in dict(attrs).get("class", "").split():
                self._muted_from = len(self._cell_stack)
            return
        if self._in_tbody and tag == "tr" and self._row is None:
            self._row = []
            return
        if self._row is not None and tag == "td":
            self._cell_chunks = []
            self._cell_stack = []
            self._muted_from = None

    def handle_endtag(self, tag):
        if not self._in_table:
            return
        if tag == "table":
            self._table_depth -= 1
            if self._table_depth <= 0:
                self._in_table = False
            return
        if tag == "tbody":
            self._in_tbody = False
            return
        if self._cell_chunks is not None:
            if self._cell_stack:
                self._cell_stack.pop()
                if self._muted_from is not None and len(self._cell_stack) < self._muted_from:
                    self._muted_from = None
                return
            if tag == "td":
                text = " ".join("".join(self._cell_chunks).split())
                self._row.append(text)
                self._cell_chunks = None
            return
        if tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None

    def handle_data(self, data):
        if self._cell_chunks is not None and self._muted_from is None:
            self._cell_chunks.append(data)


def parse_transactions_table(html: str) -> List[List[str]]:
    """Returns raw table rows: each a list of 9 cell strings in column order
    (#, Transaction Date, Owner, Ticker, Asset Name, Asset Type, Type,
    Amount, Comment)."""
    parser = _TransactionTableParser()
    parser.feed(html)
    return [row for row in parser.rows if len(row) >= 9]


class SenateEFDClient:
    def __init__(
        self,
        user_agent: str,
        session: Optional[requests.Session] = None,
        request_delay: float = DEFAULT_REQUEST_DELAY_SECONDS,
        timeout: float = 20.0,
    ):
        if not user_agent or "@" not in user_agent:
            raise ValueError(
                "The Senate eFD site expects a descriptive User-Agent with contact info, "
                "e.g. 'Trade Tracker research@example.com'"
            )
        self.user_agent = user_agent
        self.session = session or requests.Session()
        self.request_delay = request_delay
        self.timeout = timeout
        self._last_request_at = 0.0
        self._agreed = False

    def _throttle(self):
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self.request_delay:
            time.sleep(self.request_delay - elapsed)

    def _get(self, url: str, **kwargs) -> requests.Response:
        self._throttle()
        resp = self.session.get(
            url, headers={"User-Agent": self.user_agent}, timeout=self.timeout, **kwargs
        )
        self._last_request_at = time.monotonic()
        resp.raise_for_status()
        return resp

    def _post(self, url: str, data: dict, **kwargs) -> requests.Response:
        self._throttle()
        resp = self.session.post(
            url,
            data=data,
            headers={"User-Agent": self.user_agent, "Referer": url},
            timeout=self.timeout,
            **kwargs,
        )
        self._last_request_at = time.monotonic()
        resp.raise_for_status()
        return resp

    def ensure_agreement(self) -> None:
        """Accept the site's one-time search agreement, then load the
        search page for a fresh CSRF token. No-op after the first call."""
        if self._agreed:
            return
        home_resp = self._get(HOME_URL)
        match = _CSRF_RE.search(home_resp.text)
        if not match:
            raise RuntimeError("Could not find csrfmiddlewaretoken on the eFD home page")
        self._post(
            HOME_URL, data={"csrfmiddlewaretoken": match.group(1), "prohibition_agreement": "1"}
        )
        self._agreed = True

    def _search_csrf_token(self) -> str:
        resp = self._get(SEARCH_URL)
        match = _CSRF_RE.search(resp.text)
        if not match:
            raise RuntimeError("Could not find csrfmiddlewaretoken on the eFD search page")
        return match.group(1)

    def search_ptr_filings(
        self,
        since: Optional[date] = None,
        until: Optional[date] = None,
        page_length: int = DEFAULT_PAGE_LENGTH,
        max_pages: int = 50,
    ) -> List[dict]:
        """Returns filing metadata dicts: politician_name, office,
        filing_id, filing_url, filing_date. Pages through all results in
        the date range (or all time if `since`/`until` are omitted)."""
        self.ensure_agreement()
        token = self._search_csrf_token()

        all_rows: List[dict] = []
        start = 0
        for _ in range(max_pages):
            data = {
                "draw": "1",
                "columns[0][data]": "0",
                "columns[1][data]": "1",
                "columns[2][data]": "2",
                "columns[3][data]": "3",
                "columns[4][data]": "4",
                "order[0][column]": "4",
                "order[0][dir]": "desc",
                "start": str(start),
                "length": str(page_length),
                "report_types": f"[{REPORT_TYPE_PTR}]",
                "filer_types": "[]",
                "submitted_start_date": since.strftime("%m/%d/%Y 00:00:00") if since else "",
                "submitted_end_date": until.strftime("%m/%d/%Y 23:59:59") if until else "",
                "candidate_state": "",
                "senator_state": "",
                "office_id": "",
                "first_name": "",
                "last_name": "",
                "csrfmiddlewaretoken": token,
            }
            resp = self._post(DATA_URL, data=data)
            payload = resp.json()
            page_rows = payload.get("data", [])
            for row in page_rows:
                all_rows.append(self._parse_search_row(row))
            start += page_length
            if start >= payload.get("recordsFiltered", 0) or not page_rows:
                break
        return all_rows

    @staticmethod
    def _parse_search_row(row: List[str]) -> dict:
        first_name, last_name, office, report_link_html, filed_date_str = row[:5]
        link_match = _LINK_RE.search(report_link_html)
        filing_url_path, filing_kind = (link_match.group(1), link_match.group(2)) if link_match else ("", "")
        filing_id = filing_url_path.rstrip("/").split("/")[-1] if filing_url_path else ""
        return {
            "politician_name": f"{first_name} {last_name}".strip(),
            "office": office,
            "filing_id": filing_id,
            "filing_url": f"{BASE_URL}{filing_url_path}" if filing_url_path else "",
            "filing_kind": filing_kind,  # "ptr" (parseable HTML) or "paper" (scanned, unsupported)
            "filing_date": _parse_date(filed_date_str),
        }

    def fetch_filing_trades(self, filing_meta: dict) -> FilingFetchResult:
        """Fetch and parse one PTR filing's transactions."""
        filing_id = filing_meta["filing_id"]
        filing_url = filing_meta["filing_url"]

        if filing_meta.get("filing_kind") != "ptr" or not filing_url:
            return FilingFetchResult(
                filing_id=filing_id,
                filing_url=filing_url,
                status=ParseStatus.UNSUPPORTED_FORMAT,
                error="Paper (scanned) filing -- no structured transaction data available",
            )

        try:
            resp = self._get(filing_url)
        except requests.RequestException as exc:
            return FilingFetchResult(
                filing_id=filing_id, filing_url=filing_url, status=ParseStatus.ERROR, error=str(exc)
            )

        rows = parse_transactions_table(resp.text)
        trades = []
        for row in rows:
            # [#, Transaction Date, Owner, Ticker, Asset Name, Asset Type, Type, Amount, Comment]
            _, tx_date, owner, ticker, asset_name, asset_type, tx_type, amount, comment = row[:9]
            trades.append(
                Trade(
                    politician_name=filing_meta["politician_name"],
                    chamber=Chamber.SENATE,
                    office=filing_meta["office"],
                    owner=Owner.from_raw(owner),
                    transaction_date=_parse_date(tx_date),
                    ticker=ticker if ticker and ticker != "--" else None,
                    asset_name=asset_name,
                    asset_type=asset_type,
                    transaction_type=TransactionType.from_raw(tx_type),
                    amount=_parse_amount(amount),
                    comment=comment if comment != "--" else "",
                    filing_id=filing_id,
                    filing_url=filing_url,
                    filing_date=filing_meta["filing_date"],
                )
            )
        return FilingFetchResult(
            filing_id=filing_id, filing_url=filing_url, status=ParseStatus.PARSED, trades=trades
        )

    def get_trades(
        self, since: Optional[date] = None, until: Optional[date] = None
    ) -> "tuple[List[Trade], List[str]]":
        """Full pipeline: search filings in the date range, fetch each
        one's transactions. Returns (trades, errors) -- errors are
        per-filing fetch failures, surfaced rather than dropped."""
        filings = self.search_ptr_filings(since=since, until=until)
        trades: List[Trade] = []
        errors: List[str] = []
        for filing_meta in filings:
            result = self.fetch_filing_trades(filing_meta)
            if result.status == ParseStatus.PARSED:
                trades.extend(result.trades)
            elif result.status == ParseStatus.ERROR:
                errors.append(f"{filing_meta['politician_name']} ({result.filing_url}): {result.error}")
            # UNSUPPORTED_FORMAT (paper filings) is expected and not an error.
        trades.sort(key=lambda t: t.transaction_date or date.min, reverse=True)
        return trades, errors
