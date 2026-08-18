# Creator Economy Funding & Revenue Tracker

Tracks bootstrapped creator-economy companies across four subsectors --
brand/social agencies, software, performance marketing, and talent
management -- from a seed CSV watchlist. For each company it:

1. Checks SEC EDGAR full-text search for Form D filings to flag institutional
   funding (i.e. companies that may no longer be bootstrapped).
2. Estimates revenue with a subsector-routed model:
   - **agency**: `headcount x net_revenue_per_head`
   - **software**: `customers x arpu` (annual revenue per customer)
   - **performance_marketing**: `managed_ad_spend x fee_rate`
   - **talent_management**: `roster_gmv x commission_rate`
3. Estimates EBITDA as a margin band (`[low, high]`) applied to the revenue
   estimate, with a confidence flag.
4. Filters to companies with an estimated revenue of **$5M+**.

## Install

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m creator_tracker.cli data/watchlist.csv --user-agent "Your Name you@example.com"
```

SEC EDGAR requires a descriptive `User-Agent` header with contact info on
every request (its fair-access policy) -- pass your own via `--user-agent`.

Other flags:

- `--skip-edgar` -- skip the live Form D check (e.g. offline/CI runs)
- `--all` -- include companies below the $5M+ threshold too
- `--json` -- emit JSON instead of a text summary

## Watchlist CSV schema

| column | required | used by | notes |
|---|---|---|---|
| `name` | yes | all | company name, also used as the EDGAR search term |
| `subsector` | yes | revenue routing | `agency`, `software`, `performance_marketing`, or `talent_management` |
| `website` | no | reference | |
| `cik` | no | reference | not currently used for the EDGAR lookup, which matches by name |
| `headcount` | agency only | revenue | |
| `net_revenue_per_head` | agency only | revenue | |
| `roster_gmv` | talent_management only | revenue | |
| `commission_rate` | talent_management only | revenue | decimal, e.g. `0.20` |
| `customers` | software only | revenue | paying customer/account count |
| `arpu` | software only | revenue | annual revenue per customer |
| `managed_ad_spend` | performance_marketing only | revenue | annual ad spend the company manages for clients |
| `fee_rate` | performance_marketing only | revenue | decimal fee taken on managed spend, e.g. `0.15` |
| `ebitda_margin_low` / `ebitda_margin_high` | no | EBITDA | overrides the subsector default margin band when both are supplied |
| `notes` | no | reference | |

See `data/watchlist.csv` for a seed example.

## Form D check

`creator_tracker/edgar.py` queries the same backend as EDGAR's full-text
search UI (`https://efts.sec.gov/LATEST/search-index`) for Form D filings
mentioning the company name, then filters hits down to ones where the
*filer's* entity name actually matches the company -- full-text search is a
phrase match over the whole filing, so SPVs and funds named after a company
(e.g. "Network VC Syndicate Fund LLC Series Patreon") would otherwise leak
into the results as false positives.

- **Exact name match -> high confidence, flagged.**
- **Fuzzy/partial name match -> medium confidence, flagged** (worth a human
  glance).
- **No matches over an 8-year window -> high confidence, not flagged**
  (reasonably confident there's no Form D on record).
- **Request failure -> unchecked**, with the error surfaced rather than
  silently treated as "no filings."

## Confidence flags

Every estimate carries a `Confidence` (`high` / `medium` / `low`):

- **Revenue**: `high` when all required inputs for the subsector's model are
  present and valid; `low` when inputs are missing or invalid (no estimate
  is produced).
- **EBITDA**: `medium` by default, since the margin band is a heuristic
  subsector benchmark, not a measurement; `high` only when a company-specific
  margin override is supplied *and* the revenue estimate is itself `high`
  confidence; `low` when the underlying revenue estimate is missing/`low`.

## Tests

```bash
pytest
```

EDGAR tests run against mocked responses (no network access required).
