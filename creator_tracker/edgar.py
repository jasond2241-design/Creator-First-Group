"""SEC EDGAR full-text search client for flagging Form D (institutional
private-placement) filings against watchlist companies.

Uses the same backend the EDGAR full-text search UI
(https://www.sec.gov/edgar/search) calls under the hood:
https://efts.sec.gov/LATEST/search-index

SEC's fair-access policy requires a descriptive User-Agent with contact
info and asks for no more than ~10 requests/second; this client defaults
to a conservative delay between requests.
"""

from __future__ import annotations

import re
import time
import unicodedata
from datetime import date, datetime
from typing import List, Optional

import requests

from .models import Company, Confidence, FormDFiling, FundingCheck

FULL_TEXT_SEARCH_URL = "https://efts.sec.gov/LATEST/search-index"
DEFAULT_REQUEST_DELAY_SECONDS = 0.25
DEFAULT_YEARS_BACK = 8

_SUFFIX_RE = re.compile(
    r"\b(inc|incorporated|llc|l l c|corp|corporation|co|company|ltd|limited|"
    r"group|holdings?|plc)\b\.?",
    re.IGNORECASE,
)
_PUNCT_RE = re.compile(r"[^a-z0-9 ]+")
_CIK_SUFFIX_RE = re.compile(r"\s*\(CIK\s+\d+\)\s*$")


def normalize_name(name: str) -> str:
    """Lowercase, strip punctuation/legal suffixes for fuzzy comparison."""
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    name = name.lower()
    name = _PUNCT_RE.sub(" ", name)
    name = _SUFFIX_RE.sub(" ", name)
    return " ".join(name.split())


def _entity_name_from_display(display_name: str) -> str:
    """'Patreon, Inc.  (CIK 0001860300)' -> 'Patreon, Inc.'"""
    return _CIK_SUFFIX_RE.sub("", display_name).strip()


def _match_quality(target_norm: str, entity_norm: str) -> Optional[str]:
    """Compare normalized names token-by-token.

    Full-text search is a phrase match over the whole filing, so a plain
    substring check on the normalized names would let SPVs/funds named
    *after* the company through (e.g. "Network VC Syndicate Fund LLC Series
    Patreon" contains "patreon" but isn't Patreon). Requiring one name to be
    a whole-token prefix of the other allows legitimate variants (e.g.
    "Patreon" vs. "Patreon Holdings") while rejecting names where the
    company is merely referenced at the end or in the middle.

    A prefix match is only trusted when the shorter name has at least two
    tokens: single generic words ("Ghost", "Buffer", "Shine") are common
    enough as a first word that a prefix match alone is unreliable -- e.g.
    "Ghost" is a token-prefix of "Ghost Autonomy Inc." and "Ghost Locomotion
    Inc.", both unrelated companies. Single-token names still match, just
    only when the full normalized names are identical.
    """
    if not target_norm or not entity_norm:
        return None
    if entity_norm == target_norm:
        return "exact"
    target_tokens = target_norm.split()
    entity_tokens = entity_norm.split()
    if min(len(target_tokens), len(entity_tokens)) < 2:
        return None
    if (
        entity_tokens[: len(target_tokens)] == target_tokens
        or target_tokens[: len(entity_tokens)] == entity_tokens
    ):
        return "fuzzy"
    return None


class EdgarClient:
    def __init__(
        self,
        user_agent: str,
        session: Optional[requests.Session] = None,
        request_delay: float = DEFAULT_REQUEST_DELAY_SECONDS,
    ):
        if not user_agent or "@" not in user_agent:
            raise ValueError(
                "SEC EDGAR requires a descriptive User-Agent with contact info, "
                "e.g. 'Creator Economy Tracker research@example.com'"
            )
        self.user_agent = user_agent
        self.session = session or requests.Session()
        self.request_delay = request_delay
        self._last_request_at = 0.0

    def _get(self, params: dict, retries: int = 2) -> dict:
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self.request_delay:
            time.sleep(self.request_delay - elapsed)
        resp = self.session.get(
            FULL_TEXT_SEARCH_URL,
            params=params,
            headers={"User-Agent": self.user_agent, "Accept": "application/json"},
            timeout=15,
        )
        self._last_request_at = time.monotonic()
        if resp.status_code >= 500 and retries > 0:
            time.sleep(self.request_delay * 2)
            return self._get(params, retries=retries - 1)
        resp.raise_for_status()
        return resp.json()

    def search_form_d(
        self, company_name: str, years_back: int = DEFAULT_YEARS_BACK
    ) -> List[FormDFiling]:
        """Search EDGAR full-text search for Form D filings mentioning
        `company_name`, then filter hits down to ones where the filer's
        entity name actually matches the company (full-text search is a
        phrase match over the whole filing, so co-mentions and SPVs named
        after the company otherwise leak into the results).
        """
        params = {"q": f'"{company_name}"', "forms": "D"}
        if years_back:
            end = date.today()
            try:
                start = end.replace(year=end.year - years_back)
            except ValueError:  # Feb 29 with no leap year at the target year
                start = end.replace(year=end.year - years_back, day=28)
            params["dateRange"] = "custom"
            params["startdt"] = start.isoformat()
            params["enddt"] = end.isoformat()

        data = self._get(params)
        hits = data.get("hits", {}).get("hits", [])
        target_norm = normalize_name(company_name)

        filings: List[FormDFiling] = []
        for hit in hits:
            src = hit.get("_source", {})
            display_names = src.get("display_names") or []
            if not display_names:
                continue

            raw_entity = _entity_name_from_display(display_names[0])
            entity_norm = normalize_name(raw_entity)
            match_quality = _match_quality(target_norm, entity_norm)
            if match_quality is None:
                # Filer name doesn't actually match the company -- e.g. a fund
                # or SPV whose filing merely references the company by name.
                continue

            ciks = src.get("ciks") or [""]
            cik = ciks[0] if ciks else ""
            adsh = src.get("adsh", "")
            file_date_str = src.get("file_date")
            try:
                file_date = (
                    datetime.strptime(file_date_str, "%Y-%m-%d").date()
                    if file_date_str
                    else None
                )
            except ValueError:
                file_date = None

            doc_id = hit.get("_id", "")
            filename = doc_id.split(":")[-1] if ":" in doc_id else doc_id
            accession_nodash = adsh.replace("-", "")
            url = (
                f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_nodash}/{filename}"
                if cik and filename
                else ""
            )

            filings.append(
                FormDFiling(
                    accession_number=adsh,
                    entity_name=raw_entity,
                    cik=cik,
                    file_date=file_date,
                    match_quality=match_quality,
                    url=url,
                )
            )

        filings.sort(key=lambda f: f.file_date or date.min, reverse=True)
        return filings

    def check_company(self, company: Company) -> FundingCheck:
        """Run the Form D check for one watchlist company."""
        try:
            filings = self.search_form_d(company.name)
        except requests.RequestException as exc:
            return FundingCheck(
                company_name=company.name,
                checked=False,
                error=str(exc),
                confidence=Confidence.LOW,
            )

        exact_matches = [f for f in filings if f.match_quality == "exact"]
        flagged = bool(filings)

        if exact_matches:
            confidence = Confidence.HIGH
        elif filings:
            # only fuzzy name matches -- worth a human glance before trusting it
            confidence = Confidence.MEDIUM
        else:
            # no matches on an 8-year window is a fairly confident "no Form D on record"
            confidence = Confidence.HIGH

        return FundingCheck(
            company_name=company.name,
            checked=True,
            form_d_filings=filings,
            flagged_institutional_funding=flagged,
            confidence=confidence,
        )

    def check_companies(self, companies: List[Company]) -> List[FundingCheck]:
        return [self.check_company(c) for c in companies]
