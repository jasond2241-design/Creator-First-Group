"""Best-effort client for executive-branch (President / Vice President)
financial disclosures via the U.S. Office of Government Ethics (OGE).

This is a fundamentally different data source than the Senate's, in ways
that matter for what this module can honestly promise:

- Executive-branch officials file an annual OGE Form 278e, not a 45-day
  Periodic Transaction Report -- the STOCK Act *does* technically require
  the President/VP to report covered transactions, but in practice their
  disclosed holdings are almost always widely-diversified funds or Treasury
  instruments that are exempt from that requirement, so there's often
  nothing itemized to find.
- OGE's document search (reachable at www.oge.gov) is a DataTables index
  backed by a REST API hosted on a legacy system, `extapps2.oge.gov`. That
  API returns filing *metadata* (filer name, title, filing type, agency,
  date, a document link) -- not structured line items. The underlying
  documents are PDFs, not parseable tables like the Senate's PTR pages.

So `search_filings` returns `Filing` index records (see `models.py`), not
`Trade` records: a pointer to "here's a disclosure, go read it," not
itemized trades. It should NOT be silently treated as feature-parity with
`senate_efd.py`.

`extapps2.oge.gov` is also known to be unreachable from some restricted
network environments (observed while building this tracker: the TLS
handshake itself is refused, well before any application-level response).
Callers should expect `requests.RequestException` and surface it rather
than assume an empty result means "no filings."
"""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import List, Optional

import requests

from .models import Filing

API_URL = "https://extapps2.oge.gov/201/Presiden.nsf/API.xsp/v2/rest"
DEFAULT_PAGE_LENGTH = 100

_EMBEDDED_HREF_RE = re.compile(r"href=['\"]([^'\"]+)['\"]")
_TAG_RE = re.compile(r"<[^>]+>")


def _strip_tags(value: str) -> str:
    return " ".join(_TAG_RE.sub(" ", value or "").split())


def _extract_document_url(type_field: str) -> Optional[str]:
    """OGE's own DataTables config for this endpoint flags that the `type`
    field sometimes carries a raw, un-stripped `<a href="...">` anchor
    pointing at the actual document -- pull it out if present."""
    match = _EMBEDDED_HREF_RE.search(type_field or "")
    return match.group(1) if match else None


def _parse_oge_date(raw) -> Optional[date]:
    if not raw:
        return None
    raw = str(raw).strip()
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%m/%d/%Y"):
        try:
            return datetime.strptime(raw[: len(fmt) + 2], fmt).date()
        except ValueError:
            continue
    return None


class ExecutiveDisclosureClient:
    def __init__(
        self,
        user_agent: str,
        session: Optional[requests.Session] = None,
        timeout: float = 20.0,
    ):
        if not user_agent or "@" not in user_agent:
            raise ValueError(
                "OGE's site expects a descriptive User-Agent with contact info, "
                "e.g. 'Trade Tracker research@example.com'"
            )
        self.user_agent = user_agent
        self.session = session or requests.Session()
        self.timeout = timeout

    def _fetch_page(self, start: int, length: int, search_value: str, draw: int) -> dict:
        params = {
            "draw": str(draw),
            "start": str(start),
            "length": str(length),
            "search[value]": search_value,
            "search[regex]": "false",
            "columns[0][data]": "docDate",
            "columns[1][data]": "title",
            "columns[2][data]": "type",
            "columns[3][data]": "name",
            "columns[4][data]": "agency",
            "columns[5][data]": "level",
            "order[0][column]": "0",
            "order[0][dir]": "desc",
        }
        resp = self.session.get(
            API_URL, params=params, headers={"User-Agent": self.user_agent}, timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    def search_filings(
        self,
        name_query: str = "",
        page_length: int = DEFAULT_PAGE_LENGTH,
        max_pages: int = 10,
    ) -> List[Filing]:
        """Search the OGE filing index. `name_query` filters by filer name
        (e.g. "President", "Vice President", or a specific name) -- pass ""
        to fetch everything OGE serves for this page size/page count.

        Raises `requests.RequestException` on failure rather than returning
        an empty list, since `extapps2.oge.gov` is known to be unreachable
        from some network environments and that shouldn't look like "OGE
        confirms there are no filings."
        """
        filings: List[Filing] = []
        start = 0
        for draw in range(1, max_pages + 1):
            payload = self._fetch_page(start, page_length, name_query, draw)
            rows = payload.get("data", [])
            for row in rows:
                type_field = row.get("type", "")
                filings.append(
                    Filing(
                        filer_name=row.get("name", ""),
                        title=row.get("title", ""),
                        doc_type=_strip_tags(type_field),
                        agency=row.get("agency", ""),
                        level=row.get("level", ""),
                        doc_date=_parse_oge_date(row.get("docDate")),
                        document_url=_extract_document_url(type_field),
                    )
                )
            start += page_length
            total = payload.get("recordsFiltered", len(rows))
            if start >= total or not rows:
                break
        return filings

    def get_president_and_vp_filings(self) -> List[Filing]:
        """Filings whose title/level mentions the President or Vice
        President. OGE's search is a name/title full-text filter, so this
        issues two targeted queries rather than paging the entire (15,000+
        document) index client-side."""
        seen_keys = set()
        combined: List[Filing] = []
        for query in ("President", "Vice President"):
            for filing in self.search_filings(name_query=query):
                key = (filing.filer_name, filing.title, filing.doc_date, filing.document_url)
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                combined.append(filing)
        combined.sort(key=lambda f: f.doc_date or date.min, reverse=True)
        return combined
