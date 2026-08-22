# Watchlist sources

Research notes and citations for `watchlist.csv`, gathered via web search,
company websites, press coverage, and LinkedIn (August 2026). Full detail
lives here so the CSV's `notes` column can stay short; treat this file as
the provenance record for every non-obvious number in the watchlist.

## Methodology

- **Headcount** (agency subsector): pulled from each company's LinkedIn
  company page. LinkedIn shows a size band (e.g. "51-200") and often a more
  precise "Discover all N employees" count; where sources disagreed, the
  CSV uses a documented approximation, noted inline.
- **`net_revenue_per_head` / `fee_rate` / `commission_rate` benchmarks**:
  none of these companies publicly disclose a per-head revenue figure or
  exact fee/commission rate. Where the CSV supplies one, it's a documented
  industry-benchmark assumption applied consistently across the subsector
  (agency: $150k-$220k net revenue/head; performance marketing: 15% fee on
  managed spend; talent management: 15%, the midpoint of johanna b. voss's
  published 10-20% guidance) -- not a company-specific disclosed number.
  Revenue estimates built on these inputs should be read as "the arithmetic
  is right given the assumed rate," not "this is the company's actual
  reported revenue."
- **`customers` / `arpu` (software subsector)**: used only where both a
  customer count AND a revenue figure were independently disclosed by the
  company or credible reporting, so `arpu` is a derived figure from two real
  data points rather than a guess. Where only one side was available (e.g.
  revenue but no customer count), both fields are left blank rather than
  filling in a fabricated number -- see each company's note for the
  known-but-unmodeled revenue figure.
- Companies verified to have raised institutional/VC/PE funding, or that
  were acquired, are excluded from the "bootstrapped" set entirely (list
  below), except for one intentional control case (Patreon) kept in the
  watchlist specifically to validate that the Form D check flags it
  correctly.

## Brand/social agencies

- **Billion Dollar Boy** — https://www.billiondollarboy.com — "grown as an
  independent, cash-generative business without a full institutional
  venture-capital track" — https://everything-pr.com/billion-dollar-boy-the-independent-influencer-agency-category-leader
  — headcount via https://www.linkedin.com/company/billion-dollar-boy
- **The Influencer Marketing Factory** — https://theinfluencermarketingfactory.com
  — self-funded since 2018 per founders — https://www.inc.com/profile/the-influencer-marketing-factory
  — headcount via https://www.linkedin.com/company/the-influencer-marketing-factory
- **Movement Strategy** — https://www.movementstrategy.com — no funding
  rounds on Crunchbase/Tracxn — https://www.crunchbase.com/organization/movement-strategy
  — self-funded acquisition of Newfangled Studios — https://www.adweek.com/agencies/movement-strategy-acquires-newfangled-studios-to-create-a-social-marketing-powerhouse/
- **The Digital Fairy** — https://www.thedigitalfairy.co.uk — founder grew
  agency from a ~£16k personal loan to £3M turnover — https://daniellenewnham.medium.com/from-16-000-to-3-million-the-rise-or-eve-lee-and-the-digital-fairies-4f6716c776f6
- **Socially Powerful** — https://sociallypowerful.com — no funding rounds
  found; lower-confidence bootstrapped read (absence-of-record only, no
  explicit founder statement located)
- **The Exposure Co.** (Brisbane, Australia) — https://theexposure.co —
  Tracxn: unfunded, no institutional or angel investors —
  https://tracxn.com/d/companies/the-exposure-co/__ySgj-CQaWdRUN8Beaw7oR1YMFF-LY43Yl8HgJEScRWo
  — founded 2015 by Tara Kingi and Victoria Harrison —
  https://www.startupdaily.net/advice/exposure-co-crushfame-want-tap-influencer-marketing-industry/
  — headcount via https://au.linkedin.com/company/the-exposure-co-
- **Pulse Advertising** (Hamburg, Germany) — https://www.pulse-advertising.com
  — "has not raised any funding yet... does not have a single investor" —
  https://tracxn.com/d/companies/pulse-advertising/__FOZFUo1P0evEpnAH8W6RoGyDXgNm7kxq2zrCHvWhr2o
  — founded 2014 by Chris Kastenholz and Lara Daniel, origin story —
  https://www.linkedin.com/pulse/pulse-advertising-founder-lara-daniel-founding-multi-million-tausch
  — 125+ people across 11 global offices — https://influencermarketinghub.com/influencer-marketing-agencies/pulse-advertising/

### Excluded (verified funded or acquired)
Village Marketing (acquired, WPP), Movers+Shakers (acquired, Stagwell),
Obviously (acquired, WPP), Whalar (multiple seed rounds + 2025 round),
Viral Nation (~$198M PE, Eldridge/Maverix), Sixteenth (acquired by Whalar),
Fanbytes (VC-funded, acquired by Brainlabs), The Goat Agency (VC-funded,
acquired by WPP), Cashmere Agency (acquired, S4 Capital), Digital Voices
(acquired, PMG), Open Influence (Series A), Mediakix (acquired, Stadiumred),
Narrators (Singapore -- started with $2M initial funding per founder
Laurent Verrier's background; checked as an APAC influencer-agency
candidate but funded, not bootstrapped), Influency.me (Sao Paulo, Brazil --
2021 press release announced it "commences fundraising to accelerate
growth," so treated as funded/fundraising rather than bootstrapped),
FLUVIP (Bogota, Colombia -- $7.87M raised over 5 rounds, Series A in 2018,
per Crunchbase), AJ Marketing (Singapore/Seoul -- Crunchbase shows seed
funding round(s) on record), Arfadia (Jakarta, Indonesia -- founded 2008
"with zero investors" per its own site, but its company-profile page now
states a co-investor/advisor joined in 2024, so it's no longer purely
bootstrapped as of that date).

## Software

- **Kit (formerly ConvertKit)** — https://kit.com — founder Nathan Barry:
  never raised VC — https://yaro.blog/nathan-barry-vc10/ — revenue growth
  history — https://startupgtm.substack.com/p/convertkit-now-kit-growth-story-how
- **Buffer** — https://buffer.com — bought back all outside investor equity
  — https://buffer.com/resources/buying-out-investors/ — ~$22.7M ARR /
  67,000 customers (2025, aggregated from Tracxn/Buffer reporting)
- **Gumroad** — https://gumroad.com — founder described buying back investor
  equity, paying $5.34M shareholder dividend — https://sahillavingia.com/dividends
  — Q2 2023 revenue $5.29M/quarter — https://x.com/shl/status/1690330199055896576
  — **correction found by this tool's own Form D check**: EDGAR shows
  Gumroad, Inc. (CIK 1532978) filed a real equity Form D on 2024-03-04
  ($2,136,975 offering, fully sold, "Other Technology" industry group) and
  another on 2023-06-16 -- both post-dating the "bought back investors"
  narrative. Kept in the watchlist as a demonstration of the funding check
  catching something the qualitative research alone would have missed;
  should not be treated as a confirmed-bootstrapped company without further
  diligence on what those 2023/2024 raises were.
- **Ghost** — https://ghost.org — nonprofit Ghost Foundation, funded via
  2013 Kickstarter after 2x YC rejection; crossed $10M ARR per founder —
  https://x.com/JohnONolan/status/2029195753428758756
- **Flodesk** — https://flodesk.com — founders rejected by YC, self-funded
  with ~$90k savings, now ~$36-37M ARR — https://www.inc.com/jennifer-conrad/she-was-rejected-by-y-combinator-bootstrapped-startup-36-million-arr-flodesk/91278173
  — growth detail — https://www.indiehackers.com/post/tech/growing-a-fully-bootstrapped-email-marketing-platform-to-37m-arr-yEzvbRhw1NFn0lHedTWu
- **Systeme.io** (France) — https://systeme.io — "has not raised any
  funding yet," founder Aurelien Amacker bootstrapped from personal course
  sales — https://yaro.blog/aurelien-amacker/ — $20.1M ARR (2024), up from
  $8M (2023) — https://getlatka.com/companies/systemeio

### Excluded (verified funded)
Circle.so (~$30.5M incl. Tiger Global Series A), Beacons.ai (~$29.8M incl.
a16z/YC seed), Podia ($4.75M across 4 rounds), Stan Store ($5M seed,
Forerunner Ventures), ThriveCart ($35M investment from LTV SaaS Growth
Fund, Jan 2023, after being bootstrapped 2016-2023), Modash (Tallinn,
Estonia -- $14M raised over 3 rounds incl. a $12M Series A led by henQ VC
— https://www.eu-startups.com/2024/10/tallinn-based-modash-raises-e11-million-to-help-consumer-brands-scale-creator-partnerships/),
Typefully (Italian founders, bootstrapped to $1.6M ARR but took backing
from Twitter co-founder Evan Williams -- notable-investor-backed, not
bootstrapped).

## Performance marketing

- **Hawke Media** — https://www.hawkemedia.com — founder Erik Huberman:
  self-funded growth, no outside investment — https://erikhuberman.com/posts/scaling-without-strings-the-power-of-self-funded-growth/
  — manages $500M+ in media spend (company-reported)
- **KlientBoost** — https://www.klientboost.com — founder built on personal
  savings, chose agency model over VC-backed SaaS deliberately — https://pod.tomhunt.io/e/x816wj1n-bootstrapping-klientboost-to-1m-mrr-with-jonathan-dane-of-klientboost
- **Kynship** — https://www.kynship.co — no funding rounds found on
  Crunchbase/PitchBook/Tracxn
- **AdVenture Media Group** — https://adventuremedia.ai — no funding rounds
  found; founder retrospective — https://medium.com/@isaacrudansky/i-forfeited-760-560-in-revenue-last-year-f5f643670064
- **Brighter Click** — https://www.brighterclick.com — founded by a
  freelancer in 2019, no funding rounds found; pricing via https://themanifest.com/company/brighter-click
- **inBeat Agency** (Montreal, Canada) — https://inbeat.agency — Tracxn:
  unfunded, has not raised any funding —
  https://tracxn.com/d/companies/inbeat/__W8IJQ2QJdLl3MDSgaw9Jxz4qCOOnr8de_Mn28sEqGEM
  — co-founded 2019 by David Morneau —
  https://ca.linkedin.com/in/morneaudavid

### Excluded (verified funded or acquired)
Ubiquitous ($5M seed; acquired by Humanz), Statusphere ($18M Series A),
Billo (€2.9M seed/pre-seed), The Shelf ($1.4M VC per Crunchbase), Common
Thread Collective (PE from The Acacia Group), Mavely (acquired, Nu Skin
then Later), Motion ($60M+ across Seed-Series C), Directive Consulting
(Serent Capital growth investment), Ignite Visibility (backed by
Mountaingate Capital), Trend.io (acquired by soona), Nqyer (Hamburg,
Germany -- raised $50K in 2016 from next media accelerator and SAP.io
Foundry Munich; also more of an influencer directory/platform than a
managed talent roster).

## Talent management

- **Underscore Talent** — https://www.underscoretalent.com — founded by
  ex-Studio71 execs, 2021 — https://deadline.com/2021/01/underscore-talent-management-agency-formed-michael-green-reza-izad-dan-weinstein-1234682202
- **Shine Talent Group** — https://shinetalentgroup.com — described as
  having "remained independent" — https://www.netinfluencer.com/shine-talent-groups-jess-hunichen-advocates-for-creator-value/
- **VRAI Digital** — https://vraidigital.com — solo-founded 2019 — https://shoutoutla.com/meet-molly-tracy-ceo-founder-of-vrai-digital-boutique-talent-management-agency/
- **johanna b. voss Agency** — https://www.johannavoss.com — founder
  self-funded via consulting income — https://www.johannavoss.com/how-i-became-an-influencer-talent-manager-and-built-an-agency/
  — published commission-rate guidance — https://www.johannavoss.com/how-much-percentage-do-influencer-managers-take/
- **Insanity** (London/LA) — https://insanity.com — B Corp certified,
  founded 1997 by Andy Varley, who describes it as "a completely
  independent company with a positive balance sheet and zero debt" —
  https://www.managementtoday.co.uk/one-founder-launched-global-talent-agency-teenage-bedroom/interviews/article/1793974
  — B Corp status — https://www.bcorporation.net/en-us/find-a-b-corp/company/insanity-group/
  — headcount via LinkedIn (~136 employees, Aug 2025) — note: runs a record
  label as a partnership with Sony Music UK, a content joint venture rather
  than equity investment, flagged in the CSV note for transparency.
- **Scooperz** (Breda, Netherlands) — https://scooperz.com — described as
  "the largest and most successful independent social media and influencer
  agency in the Netherlands"; founded 2011 by Esther Goos. No funding
  rounds found on Crunchbase. First Netherlands entry in this subsector.

### Excluded (verified funded, acquired, or wrong category)
Elusive Talent Agency (Montreal, Canada -- no funding rounds found, but
acquired by Gameaddik on Jan 31, 2024, so no longer independent), L'AGENCY
(Amsterdam, Netherlands -- acquired by PCV Group on Nov 28, 2024), Night Media (raised $70M from StepStone Group, Founders Fund, House
Capital, K5 Global, PagsGroup, and runs its own $100M VC fund —
https://www.tubefilter.com/2026/02/17/night-70-million-funding-round/ —
removed 2026-08; previously kept as a control case, now dropped entirely
per user direction), Select Management Group (Artists First acquired a
minority stake in Feb 2020 — https://www.hollywoodreporter.com/business/business-news/artists-first-acquires-stake-influencers-management-firm-select-1279882/
, https://www.tubefilter.com/2020/02/19/artists-first-minority-stake-select-management-group/
— Artists First is majority-owned by Propagate, an institutionally-backed
media company; removed 2026-08 per user direction, superseding the earlier
"no institutional equity funding found" read, which predated this
ownership check), Fixated ($62.8M total incl. Eldridge Industries),
Digital Brand Architects (acquired by UTA), Symphony Talent Agency (wrong
category -- corporate recruitment marketing, PE-owned), Beckham Media
(wrong company -- a Pittsburgh PR firm), Amra & Elma (brand-side agency,
not a talent roster), The Digital Fairy [talent mgmt search] (couldn't
confirm it manages a roster rather than running brand campaigns -- it's
included in this watchlist under the agency subsector instead, see above).

## Control cases (intentionally included, known-funded)

- **Patreon** (software) — CIK 0001860300, Form D on file — validates the
  EDGAR check flags a real institutionally-funded company correctly.
