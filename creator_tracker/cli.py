"""Command-line entry point.

    python -m creator_tracker.cli data/watchlist.csv --user-agent "Your Name you@example.com"
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict

from .models import Confidence
from .pipeline import qualifying, run_pipeline


def _report_to_dict(report) -> dict:
    d = asdict(report)
    # dataclasses.asdict turns Enums into themselves, not their .value; and
    # date objects aren't JSON-serializable -- normalize both for output.
    d["company"]["subsector"] = report.company.subsector.value
    d["funding"]["confidence"] = report.funding.confidence.value
    for filing in d["funding"]["form_d_filings"]:
        if filing["file_date"] is not None:
            filing["file_date"] = filing["file_date"].isoformat()
    d["revenue"]["confidence"] = report.revenue.confidence.value
    d["ebitda"]["confidence"] = report.ebitda.confidence.value
    return d


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Track bootstrapped creator-economy companies.")
    parser.add_argument("csv_path", help="Path to the seed watchlist CSV.")
    parser.add_argument(
        "--user-agent",
        default="Creator Economy Tracker research@example.com",
        help="SEC EDGAR requires a descriptive User-Agent with contact info.",
    )
    parser.add_argument("--skip-edgar", action="store_true", help="Skip the live Form D check (e.g. offline runs).")
    parser.add_argument("--all", action="store_true", help="Include companies below the $5M+ revenue threshold too.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a text table.")
    args = parser.parse_args(argv)

    reports = run_pipeline(args.csv_path, user_agent=args.user_agent, skip_edgar=args.skip_edgar)
    output_reports = reports if args.all else qualifying(reports)

    if args.json:
        print(json.dumps([_report_to_dict(r) for r in output_reports], indent=2, default=str))
        return 0

    if not output_reports:
        print("No companies to report.")
        return 0

    for r in output_reports:
        c, f, rev, eb = r.company, r.funding, r.revenue, r.ebitda
        print(f"\n{c.name}  [{c.subsector.value}]")
        if rev.value is not None:
            print(f"  Revenue est.: ${rev.value:,.0f}  (method={rev.method}, confidence={rev.confidence.value})")
        else:
            print(f"  Revenue est.: n/a ({rev.notes})")
        if eb.value_low is not None:
            print(
                f"  EBITDA band: ${eb.value_low:,.0f} - ${eb.value_high:,.0f} "
                f"({eb.margin_low:.0%}-{eb.margin_high:.0%} margin, {eb.source}, "
                f"confidence={eb.confidence.value})"
            )
        else:
            print("  EBITDA band: n/a")
        if not f.checked:
            print(f"  Form D check: not run ({f.error})")
        elif f.flagged_institutional_funding:
            names = ", ".join(sorted({flt.entity_name for flt in f.form_d_filings}))
            latest = f.form_d_filings[0]
            print(
                f"  Form D: FLAGGED - institutional funding on record "
                f"(confidence={f.confidence.value}, latest={latest.file_date}, filer(s)={names})"
            )
        else:
            print(f"  Form D: none found (confidence={f.confidence.value}) -- consistent with bootstrapped")

    print(f"\n{len(output_reports)} companies shown" + ("" if args.all else " (>= $5M revenue estimate)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
