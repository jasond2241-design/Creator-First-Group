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

See `data/watchlist.csv` for a seed example covering all four subsectors,
researched from company websites, press coverage, client/case-study pages,
and LinkedIn. See `data/SOURCES.md` for full citations, the benchmark-input
methodology, and the list of well-known creator-economy names that were
checked and excluded because they're actually VC/PE-backed or acquired.

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
  silently treated as "no filings" (transient 5xx responses get one retry
  before surfacing).

Single generic-word company names (e.g. "Ghost") are handled carefully: a
fuzzy prefix match is only trusted when the shorter of the two names has at
least two tokens, otherwise unrelated companies that happen to start with
the same word (e.g. "Ghost Autonomy Inc.") would incorrectly match. See
`tests/test_edgar.py::test_single_token_name_rejects_prefix_collisions`.

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

---

# Congressional & Presidential Trade Tracker

Tracks stock trades disclosed by U.S. Senators and by the President/Vice
President, pulled live from the two official disclosure systems as filings
land -- there is no seed CSV here, everything comes from the source.

## Usage

```bash
python -m trade_tracker.cli --user-agent "Your Name you@example.com"
python -m trade_tracker.cli --since 2026-01-01 --senator Booker --ticker NVDA --json
```

Other flags:

- `--since` / `--until` -- filter by filing submission date (`YYYY-MM-DD`)
- `--senator` -- filter to politicians whose name contains this substring
- `--ticker` -- filter to one ticker symbol
- `--skip-senate` / `--skip-executive` -- skip either source
- `--json` -- emit JSON instead of a text summary

Both source sites expect a descriptive `User-Agent` with contact info, same
as SEC EDGAR above -- pass yours via `--user-agent`.

## Two sources, two different levels of fidelity

**Senate** (`trade_tracker/senate_efd.py`): itemized, ticker-level Periodic
Transaction Reports (PTRs), which the STOCK Act requires senators to file
within 30-45 days of a trade. Pulled live from the Senate's Electronic
Financial Disclosure system (`efdsearch.senate.gov`) -- its search UI gates
on a one-time "prohibition agreement" click, then serves results from a
DataTables JSON endpoint; each filing's own transaction table is scraped
for ticker, transaction date, owner (self/spouse/joint/dependent child),
buy/sell type, and the disclosed dollar range. A small number of older
filings were submitted on paper (scanned images) and have no structured
data to parse -- those are surfaced as `unsupported_format`, not silently
dropped or miscounted as "no trades."

**Executive branch / President & Vice President**
(`trade_tracker/executive_oge.py`): fundamentally different, and worth
understanding before reading its output as equivalent to the Senate data:

- They file an annual OGE Form 278e, not a 45-day PTR. The STOCK Act
  technically extends the PTR requirement to the President/VP too, but in
  practice their disclosed holdings are almost always widely-diversified
  funds or Treasury instruments, which are *exempt* from that requirement
  -- so there is often nothing itemized to find, and that's expected, not
  a bug in this tool.
- The U.S. Office of Government Ethics (OGE) hosts a document *index*
  (name, title, filing type, agency, date, and a link) via a DataTables API
  at `extapps2.oge.gov` -- but the documents themselves are PDFs, not
  structured tables like the Senate's PTR pages. This client returns
  `Filing` index records, not itemized `Trade` records, on purpose: a
  pointer to "here's a disclosure, go read it," not parsed trade lines.
- `extapps2.oge.gov` was found to be unreachable from some restricted
  network environments during development (the TLS handshake itself gets
  reset). Failures are raised/surfaced rather than treated as "zero
  filings" -- if you see an executive-branch lookup error, check whether
  your environment can reach that host before assuming there's nothing to
  report.

## Tests

```bash
pytest
```

Both clients' tests run against mocked responses (no network access
required) -- fixtures were captured from real live responses during
development, including the nested HTML the Senate PTR page uses for its
Asset Name and Ticker columns.
