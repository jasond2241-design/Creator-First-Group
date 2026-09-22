"""Command-line entry point.

    python -m trade_tracker.cli --user-agent "Your Name you@example.com"
    python -m trade_tracker.cli --since 2026-01-01 --senator Booker --json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import date, datetime

from .pipeline import filter_trades, run_pipeline


def _parse_date(raw: str) -> date:
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Expected YYYY-MM-DD, got {raw!r}") from exc


def _trade_to_dict(trade) -> dict:
    d = asdict(trade)
    d["chamber"] = trade.chamber.value
    d["owner"] = trade.owner.value
    d["transaction_type"] = trade.transaction_type.value
    d["transaction_date"] = trade.transaction_date.isoformat() if trade.transaction_date else None
    d["filing_date"] = trade.filing_date.isoformat() if trade.filing_date else None
    return d


def _filing_to_dict(filing) -> dict:
    d = asdict(filing)
    d["doc_date"] = filing.doc_date.isoformat() if filing.doc_date else None
    return d


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Track Senate and presidential/executive-branch trade disclosures."
    )
    parser.add_argument(
        "--user-agent",
        default="Congressional Trade Tracker research@example.com",
        help="Descriptive User-Agent with contact info, required by both source sites.",
    )
    parser.add_argument("--since", type=_parse_date, help="Only filings submitted on/after this date (YYYY-MM-DD).")
    parser.add_argument("--until", type=_parse_date, help="Only filings submitted on/before this date (YYYY-MM-DD).")
    parser.add_argument("--senator", help="Filter trades to politicians whose name contains this substring.")
    parser.add_argument("--ticker", help="Filter trades to this ticker symbol.")
    parser.add_argument("--skip-senate", action="store_true", help="Skip the Senate PTR check.")
    parser.add_argument(
        "--skip-executive", action="store_true", help="Skip the executive-branch (President/VP) OGE check."
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a text summary.")
    args = parser.parse_args(argv)

    result = run_pipeline(
        user_agent=args.user_agent,
        since=args.since,
        until=args.until,
        skip_senate=args.skip_senate,
        skip_executive=args.skip_executive,
    )
    trades = filter_trades(result.trades, politician=args.senator, ticker=args.ticker)

    if args.json:
        print(
            json.dumps(
                {
                    "trades": [_trade_to_dict(t) for t in trades],
                    "executive_filings": [_filing_to_dict(f) for f in result.executive_filings],
                    "senate_errors": result.senate_errors,
                    "executive_error": result.executive_error,
                },
                indent=2,
                default=str,
            )
        )
        return 0

    if trades:
        print(f"=== Senate trades ({len(trades)}) ===")
        for t in trades:
            ticker = f"{t.ticker} - " if t.ticker else ""
            print(
                f"{t.transaction_date}  {t.politician_name:<28} {t.transaction_type.value:<13} "
                f"{ticker}{t.asset_name}  [{t.amount.raw}]  owner={t.owner.value}"
            )
    elif not args.skip_senate:
        print("=== Senate trades: none found for the given filters ===")

    if result.senate_errors:
        print("\nSenate eFD errors (some filings may be missing):")
        for err in result.senate_errors:
            print(f"  - {err}")

    if not args.skip_executive:
        print(f"\n=== Executive branch (President/VP) filings ({len(result.executive_filings)}) ===")
        print("(Index only -- annual OGE disclosures, not itemized 45-day trade reports.)")
        for f in result.executive_filings:
            print(f"{f.doc_date}  {f.filer_name:<20} {f.title}  ({f.doc_type or 'n/a'})  {f.document_url or ''}")
        if result.executive_error:
            print(f"\nExecutive-branch OGE lookup failed: {result.executive_error}")
            print("(extapps2.oge.gov is known to be unreachable from some restricted networks.)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
