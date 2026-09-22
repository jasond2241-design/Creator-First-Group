"""Fetch newly disclosed trades/filings and merge them into the persistent
data files under `data/`. Meant to run on a schedule (see
`.github/workflows/trade-tracker.yml`) -- safe to re-run any time, since
merges are deduped by content rather than by "did we already run today."

    python -m trade_tracker.update_data --user-agent "Your Name you@example.com"
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, List

from .pipeline import run_pipeline

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
TRADES_PATH = DATA_DIR / "senate_trades.json"
EXECUTIVE_PATH = DATA_DIR / "executive_filings.json"
STATE_PATH = DATA_DIR / "tracker_state.json"

# First run with no prior state backfills this many days; every later run
# only asks for filings since the last watermark (with OVERLAP_DAYS of
# re-check slack, since a filing can post a day or two after its nominal
# date and dedup makes re-fetching it harmless).
DEFAULT_BACKFILL_DAYS = 270
OVERLAP_DAYS = 5


def _trade_to_dict(t) -> dict:
    d = asdict(t)
    d["chamber"] = t.chamber.value
    d["owner"] = t.owner.value
    d["transaction_type"] = t.transaction_type.value
    d["transaction_date"] = t.transaction_date.isoformat() if t.transaction_date else None
    d["filing_date"] = t.filing_date.isoformat() if t.filing_date else None
    return d


def _filing_to_dict(f) -> dict:
    d = asdict(f)
    d["doc_date"] = f.doc_date.isoformat() if f.doc_date else None
    return d


def _trade_key(d: dict) -> tuple:
    return (
        d["filing_id"],
        d["ticker"],
        d["transaction_date"],
        d["transaction_type"],
        d["amount"]["raw"],
        d["owner"],
        d["comment"],
    )


def _filing_key(d: dict) -> tuple:
    return (d["filer_name"], d["title"], d["doc_date"], d["document_url"])


def _load_json(path: Path) -> list:
    if not path.exists():
        return []
    return json.loads(path.read_text())


def _dump_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def _merge(existing: List[dict], new: List[dict], key_fn, sort_key: str) -> "tuple[List[dict], List[dict]]":
    existing_keys = {key_fn(row) for row in existing}
    added = [row for row in new if key_fn(row) not in existing_keys]
    merged = existing + added
    merged.sort(key=lambda row: row.get(sort_key) or "", reverse=True)
    return merged, added


def run(user_agent: str) -> dict:
    state = _load_json(STATE_PATH) if STATE_PATH.exists() else {}
    if isinstance(state, list):  # defensive -- STATE_PATH should always hold a dict
        state = {}

    last_date_str = state.get("senate_last_filing_date")
    since = (
        datetime.strptime(last_date_str, "%Y-%m-%d").date() - timedelta(days=OVERLAP_DAYS)
        if last_date_str
        else date.today() - timedelta(days=DEFAULT_BACKFILL_DAYS)
    )

    result = run_pipeline(user_agent=user_agent, since=since)

    all_trades, added_trades = _merge(
        _load_json(TRADES_PATH),
        [_trade_to_dict(t) for t in result.trades],
        _trade_key,
        "transaction_date",
    )
    _dump_json(TRADES_PATH, all_trades)

    added_filings: List[dict] = []
    if result.executive_filings:
        all_filings, added_filings = _merge(
            _load_json(EXECUTIVE_PATH),
            [_filing_to_dict(f) for f in result.executive_filings],
            _filing_key,
            "doc_date",
        )
        _dump_json(EXECUTIVE_PATH, all_filings)

    state.update(
        {
            "senate_last_filing_date": date.today().isoformat(),
            "last_run_at": datetime.utcnow().isoformat() + "Z",
            "senate_errors": result.senate_errors,
            "executive_error": result.executive_error,
        }
    )
    _dump_json(STATE_PATH, state)

    return {
        "added_trades": len(added_trades),
        "added_executive_filings": len(added_filings),
        "total_trades": len(all_trades),
        "senate_errors": result.senate_errors,
        "executive_error": result.executive_error,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Fetch new trades/filings and merge into data/.")
    parser.add_argument(
        "--user-agent",
        required=True,
        help="Descriptive User-Agent with contact info, required by both source sites.",
    )
    args = parser.parse_args(argv)

    summary = run(args.user_agent)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
