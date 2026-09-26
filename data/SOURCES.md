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
- **NEI** (Lisbon, Portugal) — https://nei.agency — founded April 2021 by
  Nuna Martins, Erika Barra, and Ines Cunha. Launch coverage headline:
  "Independencia e palavra de ordem da nova agencia de marketing de
  influencia NEI" ("Independence is the watchword of the new influence
  marketing agency NEI") —
  https://marketeer.sapo.pt/independencia-e-palavra-de-ordem-da-nova-agencia-de-marketing-de-influencia-nei
  — no funding rounds found. NOT verified via a Portuguese company
  registry (no accessible free registry found); medium-high confidence
  based on explicit independence framing at launch plus absence-of-record.
  First Portugal entry.
- **The Social Shepherd** (Bath, UK) — https://thesocialshepherd.com —
  founded 2018 by married co-founders Jack Shepherd and Zoe Alexandra
  Margaret Stephenson. Verified via UK Companies House #11573646,
  persons-with-significant-control filing —
  https://find-and-update.company-information.service.gov.uk/company/11573646/persons-with-significant-control
  — confirms both founders as the only controllers, individuals each
  holding 25-50% of shares, no institutional/corporate entity listed.
- **The Good Influence** (London/Manchester) — https://www.thegoodinfluence.co.uk
  — founded 2021 by Sarah Crawley and Josh Harding. Verified via UK
  Companies House #13444864 (The Good Influence Group Limited),
  persons-with-significant-control filing —
  https://find-and-update.company-information.service.gov.uk/company/13444864/persons-with-significant-control
  — confirms both founders as the only controllers, individuals each
  holding 25-50% of shares, no institutional/corporate entity listed.
  (Note: a separate, more recently incorporated "Good Influence Holdings
  Limited" turned up in the same search with an unrelated individual as
  sole controller -- no connection to this agency was found, and it was
  not pursued further; flagged here only so a future run doesn't
  mistake the two for the same business.)
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
- **NØRR3** (Helsinki, Finland) — https://norr3.fi — branded "Finland's
  only independent full-service insight and media agency," explicitly
  employee-owned — https://norr3.fi/en/norr3/ — member of the
  "Independent Nordic Network" alongside HowCom (Sweden), Calibrate
  (Denmark), TRY Opt (Norway). Founded 2019; revenue grew 160%+ YoY,
  exceeding EUR10M in 2023, with ~60 employees -- net_revenue_per_head in
  the CSV is derived from that disclosed ratio, not a pure benchmark.
  Note: general digital/media agency, not creator-specific, but fits the
  agency subsector's existing scope (similar to Pulse Advertising's mix).
- **Faulhaber** (Toronto/Montreal/Vancouver, Canada) — https://faulhaber.agency
  — founded 2001 by Christine Faulhaber, self-described as "an
  independent, woman-owned" agency for 25 years —
  https://faulhaber.agency/about-us/ — founder identity corroborated via
  Forbes Agency Council — https://councils.forbes.com/profile/Christine-Faulhaber-Founder-CEO-Faulhaber/dd15b651-b6d2-4735-9130-a4c12847d176
  and Toronto Metropolitan University alumni recognition —
  https://www.torontomu.ca/trsm-alumni/alumni-recognition/alumni-awards/2024-award/christinefaulhaber/
  — no funding rounds found, but NOT verified via a Canadian company
  registry (Corporations Canada's online search tool did not return
  results for a GET-style query, and the entity may be provincially
  rather than federally incorporated) -- medium-high confidence based on
  sustained "independent" branding plus absence-of-record, one tier below
  the UK Companies House registry confirmations elsewhere in this file.
- **AIDEM Agency** (Amsterdam, Netherlands) — https://www.aidem-agency.com —
  full-service TikTok agency, registered as Aidem Agency B.V. (Dutch KVK
  #85557137, incorporated 2022) — https://us.kompass.com/c/aidem-agency-b-v/nlc9820910/
  — grew out of a YouTube content-production venture founded 2016 by Senna
  Kost and Oscar Mooy, formalized as an independent agency in 2021, joined
  by Marwan Guedamsi in 2020 — https://www.aidem-agency.com/about-us —
  second agency in Europe to get a TikTok for Business case study —
  https://ads.tiktok.com/business/en/inspiration/aidem-agency-tiktok-success-story
  — no funding rounds found on Crunchbase/Tracxn (no dedicated profile for
  the Amsterdam entity found at all). NOT verified via a registry-level
  ownership check (Dutch UBO/beneficial-ownership data is paywalled, same
  limitation as other EU jurisdictions) -- medium confidence based on
  consistently named co-founders plus absence-of-funding-record, same
  tier as Movement Strategy/Faulhaber. First Netherlands entry in the
  agency subsector (Scooperz already covers Netherlands under
  talent_management).
- **InHype** (Dubai, UAE) — https://www.inhype.social — creator/influencer
  marketing agency for beauty, retail, and FMCG brands across the UAE and
  Saudi Arabia; founded 2016/2017 by Nour Chaar (Founder & CEO) —
  https://campaignme.com/inhype-a-next-gen-influencer-agency-for-brands/
  — Tracxn: "has not raised any funding yet." Team named specifically as
  an "agency family of 20" (Jad Gosen, Devya Ghosn among named staff),
  though LinkedIn's broader band is 11-50. No UAE company-registry
  ownership check available (no free public equivalent to UK Companies
  House found for the UAE), so confidence rests on the Tracxn signal plus
  a consistently-named founder, same tier as Faulhaber/Movement Strategy.
  Third-party revenue estimates ($1-5M/yr, algorithmic) are not used.
  First Middle East/GCC entry.
- **Block Report** (London, UK) — https://www.blockreport.uk — AI-driven
  social PR/cultural-intelligence agency founded Dec 2024 by Jack
  Colchester (ex-Wonderhood) and Chris Grimwood (ex-Iris, since departed)
  — named one of Campaign's "Eight New Agencies to Watch in 2026" —
  https://www.campaignlive.co.uk/article/eight-media-agencies-watch-2025/1900928
  — verified via UK Companies House #16112510,
  persons-with-significant-control filing —
  https://find-and-update.company-information.service.gov.uk/company/16112510/persons-with-significant-control
  — confirms Colchester as the sole active controller, an individual
  holding 75%+ of shares and voting rights, no institutional/corporate
  entity listed.
- **IPLIX Media** (Gurugram, India) — https://iplixmedia.com — creator-economy
  company blending talent management, branded content, and creator-led
  ventures for top Indian influencers; founded 2019 by Neel Gogia,
  converted to IPLIX MEDIA LLP in 2020 with UK-based partner Jag Chima
  joining — https://yourstory.com/2022/01/iplix-media-connects-influencers-brands
  — explicit founder quote on funding: "We are in no need to raise capital
  right now, if in the future we need to then, we will enter the market to
  raise capital. We are happy where we are." — same article — corroborated
  by Tracxn: "has not raised any funding yet" —
  https://tracxn.com/d/companies/iplix/__6_VaYiDkv2X6RwllXCdOJgL6BAk1x9Ebs5Cx_YvFyHE
  — real disclosed revenue INR84 crore (~$10.1M) for FY2024-25, +95% YoY,
  163 employees, per trade press (Entrepreneur India profile —
  https://www.entrepreneur.com/en-in/social-media/behind-the-scenes-the-agency-behind-some-of-indias/432290
  ). NOT verified via India's MCA registry (LLP partner/ownership data is
  paywalled), but the explicit founder no-funding quote is the same
  evidentiary tier used for Kit/Nathan Barry and Systeme.io/Aurelien
  Amacker elsewhere in this file. net_revenue_per_head=$62,000 is derived
  from the real FY2024-25 figure divided by headcount, not a benchmark --
  notably lower than other agency entries' per-head figures, consistent
  with a larger-headcount creator-economy platform rather than a boutique
  creative agency. First India entry.
- **One Shot Group** (Milan, Italy) — https://www.oneshotgroup.it — digital
  talent/influencer marketing group (One Shot Agency manages 35+ digital
  creators, plus a streaming and a music-label unit); founded 2017 by
  Eugenio Scotto (CEO), Matteo Maffucci (Creative Director), and Benedetta
  Balestri (Managing Director), named consistently across two separate
  Forbes Italia profiles —
  https://forbes.it/2023/04/21/one-shot-group-agenzia-influencer-marketing
  and https://forbes.it/2023/11/14/benedetta-balestri-agenzia-one-shot-group-talenti-digitali
  — real disclosed revenue over EUR7M in 2022 (+30% YoY), ~40 employees
  plus the three founders, corroborated by trade press —
  https://www.adcgroup.it/adv-express/news/industry/industry/one-shot-group-chiude-il-2022-con-un-fatturato-di-oltre-7-milioni-di-euro-e-una-crescita-del-30-nello-stesso-anno-il-gruppo-si-consolida-in-quattro-unit-e-firma-la-sua-prima-joint-venture.html
  , https://www.engage.it/agenzie/one-shot-group-cresce-del-30-e-si-consolida-in-quattro-unit.aspx
  , https://www.touchpoint.news/2023/01/25/one-shot-chiude-il-2022-in-crescita-del-30-a-quota-7-milioni-di-fatturato/
  — no funding rounds or investors found in any source searched. NOT
  verified via the Italian company registry (Registro Imprese/Camera di
  Commercio ownership/shareholder data is paywalled -- same access issue
  as other Italian/French entities); confidence rests on convergent
  named-founder press coverage, same evidentiary tier as Side (Brazil) and
  NEI (Portugal). net_revenue_per_head=$175,000 in the CSV is derived from
  the real EUR7M/2022 figure divided by headcount, not a pure benchmark.
  First Italian entry.

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
bootstrapped as of that date), House of Marketers (London, UK TikTok
agency -- backed by private-equity investor Ethos Partners via a buy-out
funded with a seven-figure loan from Frontier Development Capital —
https://www.frontierdevelopmentcapital.com/news/fdc-backs-private-equity-buy-out-at-leading-tiktok-agency/
), Creative Converters (Melbourne, Australia UGC/TikTok agency founded
2020 by Noah Hunter Dorsey -- TMSPC Group (parent of Admosis Media Group)
acquired an 85% majority stake, per B&T and Campaign Brief trade coverage,
so no longer independent), Gushcloud International (Singapore -- pan-Asia
influencer/talent agency founded 2011 by Althea Lim and Vincent Ha;
Crunchbase/Tracxn show $14.5M raised over 6 rounds including a Series A,
with investors incl. YG Entertainment, Wavemaker Partners, and YDM --
checked as an APAC talent-agency candidate but funded, not bootstrapped),
Kingfluencers (Zurich, Switzerland -- Swiss market-leading influencer
agency founded 2015; Swiss Founders Fund invested, and the company was
acquired by Naoo on 14-Mar-2025 -- both funded and no longer independent),
Wowzi (Nairobi, Kenya -- creator/influencer marketplace founded 2019 by
Brian Mogeni, Mike Otieno, and Dr. Hassan Bashir; raised $3.2M total
across pre-seed and seed rounds led by 4DX Ventures, with To.org, Golden
Palm Investments, LoftyInc Capital, and others -- funded, not
bootstrapped; checked as an East Africa creator-platform candidate).

**Inconclusive, not added (needs further diligence before re-checking):**
Upeo Talent Agency (Nairobi, Kenya -- East African talent management and
creative consultancy founded 2016 by Mike Mutenyo, representing
musicians, actors, and content creators across 10+ African markets) -- no
funding, revenue, or headcount information found anywhere; genuinely
unknown funding status rather than confirmed bootstrapped. GO2JUMP
(Barcelona/Madrid, Spain -- general digital marketing agency, Google/
HubSpot/Meta partner, founded 2008) -- no founder name found to check
against any registry, and it reads as a generalist digital-marketing shop
(SEO/PPC/CRO/web analytics) rather than a creator-economy-specific
business, so it doesn't clearly fit this watchlist's scope even before
funding status is considered. Vibrander (Cordoba, Argentina -- performance/"brandformance" marketing
agency founded 2019 by Tatiana Morozovsky and Giuliano Flesler, ~22-25
people, 40-50+ clients, first Great Place to Work-certified performance
agency in Cordoba) -- no funding announcement found either way, and no
explicit founder no-VC statement; also no managed-ad-spend or revenue
figure disclosed anywhere, so even if bootstrapped status were confirmed
there's no real number to feed the performance_marketing model. Left out
on both evidentiary and data-availability grounds.

**Inconclusive, not added (needs further diligence before re-checking):**
Stride Social (Worthing, UK influencer agency co-founded by Alex Hendy and
Ollie Kitson) -- UK Companies House (#14198728) shows both founders held
PSC status only until 13 Oct 2025, when it was replaced by a filed
statement of "no registrable person"; critically, a Singapore entity,
"Stride Global Holdings Pte. Ltd.", held 75%+ control immediately before
that change. Unclear whether this Singapore holding company is itself
wholly founder-owned (a common tax-structuring move) or represents
outside/institutional capital -- no funding announcement was found either
way. Left out rather than guessed; a future run could try to trace
Stride Global Holdings Pte. Ltd.'s own ownership via Singapore's ACRA
(previously found to require paid access) or a founder interview that
addresses the Singapore entity directly. Minimalist Agency (Mexico City --
performance/influencer marketing agency founded 2015 by CEO Alexis
Soubran, described in press only as "one of Mexico's leading independent
digital agencies") -- "independent" here reads as ad-industry shorthand
for "not part of a holding network" (WPP/Omnicom/etc.) rather than a
funding claim, no explicit no-VC statement or revenue/headcount figure
found anywhere, and Tracxn's page returned 403/blocked -- left out for
insufficient evidence rather than guessed either way. Curve (Tromso/Oslo,
Norway -- performance marketing agency founded 2023 by Sivert Ridderseth
and Alex Andreessen, paid-per-performance model across Meta/Google/
Snapchat/TikTok for Scandinavian B2C brands) -- no funding confirmation
either way was found (Crunchbase/PitchBook/Dealroom pages didn't resolve
to usable content), and the company's own materials gave conflicting
managed-ad-spend figures across sources (one said "over 1.5 million EUR
monthly," another said "15 million EUR" -- a 10x discrepancy). Using the
more conservative, primary-source figure (EUR1.5M/month = EUR18M/year)
against a typical performance-marketing fee rate doesn't clearly clear
the $5M threshold either. Left out on both funding-ambiguity and
data-quality grounds; a future run could revisit once the company (very
new, founded 2023) has more third-party coverage.

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
- **Kunfupay** (Murcia, Spain, Delaware-incorporated) — https://www.kunfupay.com
  — founded 2022 by Ruben Romero; press quote: "ha crecido... de forma
  completamente organica, sin recurrir a financiacion externa" —
  https://ecosistemastartup.com/kunfupay-un-millon-al-mes-sin-inversion-externa/
  — ~EUR1M/month revenue, 2,000+ creators, though US funds have since
  shown interest — https://www.cantabriaeconomica.com/patrocinado/informacion-al-dia/kunfupay-la-startup-espanola-que-factura-un-millon-de-euros-al-mes-sin-inversion-capta-la-atencion-de-fondos-estadounidenses/
  — SEC EDGAR full-text search for "Kunfupay"/"Kunfu" (with Form D
  filter) returns zero hits, consistent with no US securities offering
  to date.
- **Senja** (London, UK) — https://senja.io — co-founded 2023 by Olly
  Meakings and Wilson Wilson, who met via X's #buildinpublic community —
  https://support.senja.io/who-created-senja-9kqxi — explicitly
  self-described as bootstrapped, $0 external funding and ~$800K ARR per
  https://getlatka.com/companies/senja.io — verified via UK Companies
  House (Senja Proof Ltd, #14609789), persons-with-significant-control
  filing —
  https://find-and-update.company-information.service.gov.uk/company/14609789/persons-with-significant-control
  — confirms Oliver Dominic Meakings and Nnani Wilson Wilson (ceased June
  2025) as the only controllers, both individuals, no institutional
  entity listed.
- **Subscribr** — https://subscribr.ai — AI scriptwriting/ideation
  platform built exclusively for YouTube creators; founder Gil Hildebrand
  ran it solo for ~1.5 years before a co-founder joined, explicitly chose
  "the path of not taking VC money," bootstrapped from $0 plus a $20K
  customer pre-launch presale (not equity) —
  https://startupfounderstories.com/stories/gil-hildebrand-subscribr-10k-mrr
  — reached $1M in annual revenue within 18 months of launch with 4,000+
  paying customers — https://www.thestartupstorys.com/2026/03/gil-hildebrands-subscribr-story.html
  — this tool's own SEC EDGAR full-text search for "Subscribr" returns
  zero Form D filings. customers=4,000 and arpu=$250 are both derived
  from the two independently disclosed figures above, not a benchmark
  guess. Likely below the $5M qualifying threshold at current scale, but
  included given the unusually clean, explicit-founder-quote sourcing.
- **Flodesk** — https://flodesk.com — founders rejected by YC, self-funded
  with ~$90k savings, now ~$36-37M ARR — https://www.inc.com/jennifer-conrad/she-was-rejected-by-y-combinator-bootstrapped-startup-36-million-arr-flodesk/91278173
  — growth detail — https://www.indiehackers.com/post/tech/growing-a-fully-bootstrapped-email-marketing-platform-to-37m-arr-yEzvbRhw1NFn0lHedTWu
- **Systeme.io** (France) — https://systeme.io — "has not raised any
  funding yet," founder Aurelien Amacker bootstrapped from personal course
  sales — https://yaro.blog/aurelien-amacker/ — $20.1M ARR (2024), up from
  $8M (2023) — https://getlatka.com/companies/systemeio
- **Subs (Subco Group)** (UK) — https://subs.com — creator subscription
  platform launched May 2025 by Tim Stokely, founder of OnlyFans —
  https://en.wikipedia.org/wiki/Subs.com — verified via UK Companies
  House #14818102: officers filing confirms Timothy Christopher Stokely
  and Guy Robert Stokely as directors —
  https://find-and-update.company-information.service.gov.uk/company/14818102/officers
  — persons-with-significant-control filing confirms Timothy Christopher
  Stokely as sole controller, an individual holding 75%+ of shares and
  voting rights, no institutional/corporate entity listed —
  https://find-and-update.company-information.service.gov.uk/company/14818102/persons-with-significant-control
- **Payhip** (London, UK) — https://payhip.com — digital-product storefront
  for creators (courses, downloads, memberships, 5%/2%/0% fee tiers by
  plan); founded 2012/2013 by brothers Abshir ("Abs") and Kahin Farah.
  Verified via UK Companies House: Payhip Ltd (#08386910)
  persons-with-significant-control filing —
  https://find-and-update.company-information.service.gov.uk/company/08386910/persons-with-significant-control
  — confirms both brothers as the only controllers, each an individual
  holding 25-50% of shares/voting rights; the related Payhip Holdings Ltd
  (#16772931) —
  https://find-and-update.company-information.service.gov.uk/company/16772931/persons-with-significant-control
  — is wholly controlled by Kahin Farah (75%+), no institutional/corporate
  PSC anywhere in the structure. Third-party aggregator revenue/headcount
  figures (~$14.2M revenue, 152-164 employees) conflict sharply with
  LinkedIn's own 2-10 employee count and are not disclosed by the company
  -- treated as unreliable, so customers/arpu left blank rather than
  guessed. Fourth UK software entry.

### Excluded (verified funded)
Circle.so (~$30.5M incl. Tiger Global Series A), Beacons.ai (~$29.8M incl.
a16z/YC seed), Hype/HypeKit (creator marketing and payments platform
founded 2016 -- Crunchbase shows a Series A with Bullpen Capital among
investors -- funded, not bootstrapped), Podia ($4.75M across 4 rounds), Stan Store ($5M seed,
Forerunner Ventures), ThriveCart ($35M investment from LTV SaaS Growth
Fund, Jan 2023, after being bootstrapped 2016-2023), Modash (Tallinn,
Estonia -- $14M raised over 3 rounds incl. a $12M Series A led by henQ VC
— https://www.eu-startups.com/2024/10/tallinn-based-modash-raises-e11-million-to-help-consumer-brands-scale-creator-partnerships/),
Typefully (Italian founders, bootstrapped to $1.6M ARR but took backing
from Twitter co-founder Evan Williams -- notable-investor-backed, not
bootstrapped), Bonjoro (Sydney, Australia -- raised ~$743K seed plus ~$1M
AUD from Equity Venture Partners, Grand Prix Capital, and Tidal Ventures
per Crunchbase; personal-video messaging tool used by creators/businesses,
checked as a software candidate but funded, not bootstrapped), Pillar
(San Francisco -- creator storefront/link-in-bio tool; raised a seed
round with Four Cities Capital per Crunchbase), SendOwl (UK -- founded by
George Palmer 2010, but acquired by Plotke in 2020, which then raised
$4.5M in seed funding backed by Stripe -- https://www.siliconrepublic.com/start-ups/sendowl-seed-funding-stripe
-- no longer independent), Beacons.ai (checked again 2026-09-11: also
raised a $23M Series A in Nov 2023 with a16z among prior investors,
confirming the earlier exclusion), Linktree (Melbourne, Australia --
link-in-bio pioneer, bootstrapped to $10M ARR by 2020 per company
retrospectives, but has since raised $165.7M total across Series B/C
rounds led by Index Ventures and Coatue at a $1.3B valuation -- no longer
bootstrapped, checked as an obvious Australian software candidate given
its founding story is often mis-cited as a pure-bootstrap success), Twigeo
(Stockholm, Sweden -- TikTok/app growth marketing agency; Crunchbase shows
$150K raised over 1 round, so not purely bootstrapped), Moongency
(Hamburg, Germany -- influencer/artist management agency founded 2022 by
Janet Pawelczyk; acquired by MYTY Group on Dec 18, 2024, no longer
independent), Agorapulse (Paris, France -- social media management tool
often cited as a French bootstrap success story, but Crunchbase shows
$18.3M raised across a seed round and a 2019 venture round led by Hi
Inov, with Cipio Partners and Starquest Capital also investors -- funded,
not bootstrapped), Sendible (London, UK -- founder Gavin Hammar
bootstrapped it from his spare bedroom in 2009 to ~GBP2M turnover by 2015
with no outside investment, but the company was acquired by Traject in
March 2021 -- no longer independent), TubeBuddy (bootstrapped YouTube
optimization tool per Tracxn/Latka, grew to $4.8M revenue with a 44-person
team, but acquired by Branded Entertainment Network on 29-Oct-2020 -- no
longer independent), vidIQ (YouTube optimization suite -- $7.3M raised
across 3 rounds per Crunchbase, backed by Mark Cuban and other angels --
funded, not bootstrapped), Fohr (New York -- influencer marketing
platform founded 2013 by James Nord; Crunchbase shows $1.76M raised from
Ataraxia Capital Partners, O'Reilly AlphaTech Ventures, Indie.vc, and
Joyance Partners -- funded, not bootstrapped), Skool (Las Vegas --
community-plus-course platform founded 2019 by Sam Ovens; raised $0 in
formal VC rounds, but Alex Hormozi's firm Acquisition.com became a
confirmed outside investor/partner in 2023, described by Ovens as "the
largest investment of his life" -- treated as notable-investor-backed
rather than bootstrapped, same standard applied to Typefully/Evan
Williams elsewhere in this file), Mighty Networks (community platform --
$66M raised across 3 rounds, most recently 2021 -- funded, not
bootstrapped).

**Inconclusive, not added (needs further diligence before re-checking):**
Boozt.io (Manila, Philippines -- creator-economy platform led by
co-founder/CEO Jason Deniega, mission to enable Filipino creators to earn
from their work) -- received a PHP4.1M (~$73K) DOST-PCIEERD government
startup grant, which is non-dilutive rather than VC equity, so doesn't
automatically disqualify it the way institutional funding would; but no
revenue, customer count, or other financial figure was found anywhere,
so there's nothing to feed the software model even if bootstrapped status
were otherwise confirmed. Left out on data-availability grounds. Nine
Agency (Sweden/Nordics -- influencer marketing agency founded 2018 by
Viktor Nylén and Jacob Boe as a continuation of Nouw.com, a Scandinavian
blogging platform sold off in 2022) -- the entity trail is genuinely
confusing: the original holding company (Nouw Media AB, renamed Nine & Co
Group AB) reported 32.1M SEK revenue in 2022 (~$3M), and a related entity
Collabri AB (board chaired by Jacob Boe) reported 30.5M SEK in 2025
(~$2.9M) with only 6 employees -- neither entity individually clears the
$5M threshold, and it's unclear how these relate to the wider "Nine
Agency" brand operating across Sweden/Norway/Denmark/Finland (possibly
separate national entities not surfaced here). Left out on both
threshold and entity-structure-clarity grounds rather than guessed at a
combined figure.

## Performance marketing

- **Hawke Media** — https://www.hawkemedia.com — founder Erik Huberman:
  self-funded growth, no outside investment — https://erikhuberman.com/posts/scaling-without-strings-the-power-of-self-funded-growth/
  — manages $500M+ in media spend (company-reported)
- **Positive Agency** (Lima, Peru) — https://www.positive.agency —
  performance/digital-media agency with distributed teams across Mexico,
  Colombia, Peru, and Chile (clients incl. Canon, Volvo Trucks, Sodimac);
  founded ~2009 by Miguel de la Roca and Hugo Rodriguez, who met as
  students at the University of Lima —
  https://www.latinpost.com/articles/166875/20260206/two-peruvian-marketing-visionaries-show-global-brands-how-intelligent-talent-distribution-creates.htm
  and https://www.techtimes.com/articles/314354/20260128/co-founders-miguel-de-la-roca-hugo-rodriguez-transform-how-international-companies-navigate-latin.htm
  — no funding rounds or investors found on Crunchbase for either the
  company or Miguel de la Roca's person profile. managed_ad_spend=$10M is
  a conservative floor from the company's own press materials ("manages
  over $10 million in digital media investment") -- treated as a floor,
  not a precise figure, so the true managed spend and implied revenue may
  be higher; fee_rate=15% is a benchmark, not disclosed. ~50 employees per
  one press source, not independently corroborated. NOT verified via a
  Peruvian company registry (SUNARP ownership data not freely accessible).
  First Peru entry.
- **KlientBoost** — https://www.klientboost.com — founder built on personal
  savings, chose agency model over VC-backed SaaS deliberately — https://pod.tomhunt.io/e/x816wj1n-bootstrapping-klientboost-to-1m-mrr-with-jonathan-dane-of-klientboost
- **UGC3** (UK) — https://ugc3.co.uk — founded by Ashley Chinyangarara,
  inspired by his own experience as a UGC creator —
  https://www.influme.io/blog/top-ugc-agencies-uk — verified via UK
  Companies House #16812965, persons-with-significant-control filing —
  https://find-and-update.company-information.service.gov.uk/company/16812965/persons-with-significant-control
  — confirms Chinyangarara as sole controller, an individual holding 75%+
  of shares and voting rights, no institutional/corporate entity listed.
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
- **UGCers** (Haslemere, UK) — https://www.ugcers.com — UK Companies House
  #15201857, incorporated Oct 2023 —
  https://find-and-update.company-information.service.gov.uk/company/15201857
  — persons-with-significant-control filing confirms co-founders Leanne
  Orr and Riina Stocker each hold 25-50% share ownership as individuals,
  with no institutional/corporate controller listed —
  https://find-and-update.company-information.service.gov.uk/company/15201857/persons-with-significant-control
  — first watchlist entry verified directly via a national company
  registry rather than a third-party funding tracker or press statement.
- **Another Concept** (Leeds, UK) — https://anotherconcept.co.uk —
  founded May 2023 by four ex-agency colleagues — https://www.yorkshirepost.co.uk/business/new-leeds-marketing-agency-hopes-to-redefine-the-agency-model-4383433
  — verified via UK Companies House #14873367,
  persons-with-significant-control filing —
  https://find-and-update.company-information.service.gov.uk/company/14873367/persons-with-significant-control
  — confirms Richard Hart, Marcus Hearn, Alexander Gregory, and Thomas
  Brook by name as the only controllers, each an individual holding
  25-50% of shares, no institutional/corporate entity listed.
- **TBAR Partners** (Los Angeles area) — https://tbarpartners.com —
  official TikTok Shop Partner agency launched June 2025 by Tyler
  Brechbiel and Alex Rudolph, college baseball teammates at Grace College,
  Indiana, who dropped out to run the agency full-time —
  https://www.netinfluencer.com/tbar-partners-built-a-tiktok-shop-agency-around-what-brands-get-wrong-about-the-channel/
  — this tool's own SEC EDGAR full-text search for "TBAR Partners" returns
  zero Form D filings. No explicit founder no-funding quote found, but
  also no funding round found anywhere. Manages $5M+/month in gross
  merchandise value (GMV, not company revenue) across 30+ brands. Very
  new (~15 months old at time of writing) -- likely still below the $5M
  threshold.

### Excluded (verified funded or acquired)
Ubiquitous ($5M seed; acquired by Humanz), Statusphere ($18M Series A),
Billo (€2.9M seed/pre-seed), The Shelf ($1.4M VC per Crunchbase), Common
Thread Collective (PE from The Acacia Group), Mavely (acquired, Nu Skin
then Later), Motion ($60M+ across Seed-Series C), Directive Consulting
(Serent Capital growth investment), Ignite Visibility (backed by
Mountaingate Capital), Trend.io (acquired by soona), Nqyer (Hamburg,
Germany -- raised $50K in 2016 from next media accelerator and SAP.io
Foundry Munich; also more of an influencer directory/platform than a
managed talent roster), Uptickk (TikTok Shop agency, one of four
agencies in TikTok Shop's early beta program -- backed by Caldicot
Capital, funded not bootstrapped).

**Inconclusive, not added (needs further diligence before re-checking):**
MomentIQ (Los Angeles -- TikTok Shop growth agency founded 2023 by Alex
Elsea, reports driving $130-150M+/year in client GMV -- not the agency's
own revenue) -- this tool's own SEC EDGAR search returns zero Form D
filings, but founder Alex Elsea's bio describes him as "known for driving
growth in venture-backed companies" and having "scaled a startup to a
$250M Series D valuation" (his past employers, not necessarily MomentIQ
itself), and "every full-time team member holds equity" hints at an
external-investor-style cap table without confirming one. No explicit
funding announcement found either way. Left out on ambiguity grounds
rather than guessed. The UGC Agency (Wembley, UK -- UGC marketing agency
founded by Aleks Velev, 3,000+ creator network across 11 ad platforms)
-- Tracxn: unfunded. Registered as THE UGC LONDON LIMITED (Companies
House #16071533), but only incorporated 11 Nov 2024 with first accounts
not due until 11 Aug 2026, so no revenue/headcount figures exist in the
public record yet. Left out purely on data-availability/company-age
grounds; worth re-checking once its first accounts are filed.

## Talent management

- **Underscore Talent** — https://www.underscoretalent.com — founded by
  ex-Studio71 execs, 2021 — https://deadline.com/2021/01/underscore-talent-management-agency-formed-michael-green-reza-izad-dan-weinstein-1234682202
- **Shine Talent Group** — https://shinetalentgroup.com — described as
  having "remained independent" — https://www.netinfluencer.com/shine-talent-groups-jess-hunichen-advocates-for-creator-value/
- **VRAI Digital** — https://vraidigital.com — solo-founded 2019 — https://shoutoutla.com/meet-molly-tracy-ceo-founder-of-vrai-digital-boutique-talent-management-agency/
- **86 Talent** (UK) — https://86talent.com — founded 2023 by Melissa
  Ritchie, a former influencer herself. Verified via UK Companies House
  (Eightysix Talent Ltd, #14445061), persons-with-significant-control
  filing —
  https://find-and-update.company-information.service.gov.uk/company/14445061/persons-with-significant-control
  — confirms Ritchie as sole controller, an individual holding 75%+ of
  shares and voting rights, no institutional/corporate entity listed.
- **AFK Creators** (London, UK) — https://www.thisisafk.com — gaming/esports
  talent management agency founded 2018 by Matt Woods, starting from his
  living room — https://theclick.news/afk-creators/ — explicit founder
  quote: "It was all self-revenue generation... we don't have a board to
  answer to" (same article). Verified via UK Companies House (AFK Creators
  Ltd, #11771069, incorporated Jan 2019),
  persons-with-significant-control filing —
  https://find-and-update.company-information.service.gov.uk/company/11771069/persons-with-significant-control
  — confirms Matthew Woods (50-75% of shares) and Haodong Zhang (25-50%)
  as the only controllers, both individuals, no institutional/corporate
  entity listed. IMPORTANT: several unrelated companies share the generic
  "AFK" name at Companies House (AFK Group Limited #11073561, PSC Alim
  Firoz Karmali; AFK Studios Group Ltd #12575969, PSC Earle Peter Brent
  Arney) -- both entirely unconnected to Woods. This entry cites only AFK
  Creators Ltd #11771069, the one actually matching Woods by name, after
  explicitly ruling the other two out -- a name-collision risk analogous
  to the "Ghost" Form D false-positive elsewhere in this file. Companies
  House lists 20 employees for this specific Ltd; press describes the
  wider "AFK Group" umbrella (which includes ventures beyond talent
  management) reaching 98 employees by 2026, but that figure isn't
  isolated to this entity so wasn't used. No company-specific revenue or
  roster GMV found.
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
- **Get Social With Lily** (UK) — https://www.getsocialwithlily.co.uk —
  founded 2024 by Lily Mae Herridge-Baker. UK Companies House #15990304,
  persons-with-significant-control filing —
  https://find-and-update.company-information.service.gov.uk/company/15990304/persons-with-significant-control
  — confirms Herridge-Baker as the sole controller, an individual holding
  75%+ of shares and voting rights, no institutional/corporate entity
  listed. Second watchlist entry verified directly via a national company
  registry (after UGCers).
- **Blinding Talent** (UK) — https://www.blindingtalent.com — independent
  music artist management/marketing consultancy founded 2021 by Mark
  Adams (28 years in music TV, ex-Channel 4/Bauer/Emap) and Scott Monks —
  https://musically.com/2026/08/13/from-the-box-to-blinding-talent-mark-adams-on-28-years-shaping-music-tv-and-artist-careers/
  — verified via UK Companies House #13246982,
  persons-with-significant-control filing —
  https://find-and-update.company-information.service.gov.uk/company/13246982/persons-with-significant-control
  — confirms Mark Steven Adams and Scott Anthony Monks by name as the
  only controllers, each an individual holding 25-50% of shares, no
  institutional/corporate entity listed.
- **L3TCRAFT** (Madrid, Spain) — https://www.l3tcraft.com — founded 2013
  by four YouTubers (Alexelcapo, Tonacho, Chincheto77, and Aitor
  "Milicua" Fernandez, confirmed founder/COO via LinkedIn) as the first
  YouTubers agency in Spain; LinkedIn lists it as "self-owned," 11-50
  employees; no funding rounds found. Not verified via a Spanish company
  registry (no accessible free registry found). First Spanish-speaking
  market entry in this subsector.
- **Side** (Sao Paulo, Brazil) — https://sideco.com.br — founded 2017 by
  Larissa Calheiros and Tatiane Medeiros, reportedly starting with R$400
  in capital —
  https://www.poder360.com.br/poder-empreendedor/empresarias-abrem-agencia-de-marketing-com-investimento-de-so-r-400/
  — Exame headline: "Sem investimento inicial, elas criaram agencia de
  marketing de influencia" —
  https://exame.com/negocios/sem-investimento-inicial-elas-criaram-agencia-de-marketing-de-influencia-e-miram-r-36-mi-em-2025/
  — real disclosed revenue R$32M (2025) per Forbes Brasil —
  https://forbes.com.br/forbes-mkt/2026/04/infomercial-side-co-uma-decada-moldando-a-creator-economy/
  — not verified via a Brazilian company registry; first Brazil/LATAM
  entry and first Portuguese-speaking market entry in this subsector.
- **Johnson & Laird** (Auckland, New Zealand) — https://johnsonlaird.com —
  talent agency (actors, voice artists, presenters, MCs, plus a dedicated
  content-creators/social-influencer division "J&L Creators"); founded
  2002 by Imogen Johnson, celebrating its 25th year in 2026 —
  https://www.nzherald.co.nz/lifestyle/society-insider-nz-talent-agency-johnson-laird-celebrates-25-years-imogen-johnson-shares-biggest-moments/premium/TGI4M5P3AFAD3IGWWPPAANPWNI/
  — verified via the New Zealand Companies Register (company #1168630) —
  https://app.companiesoffice.govt.nz/companies/app/ui/pages/companies/1168630/shareholdings
  — shareholder list: Imogen Johnson (92%+1%), Theresa Maria Healey (6%),
  Dennis Johnson (1%) -- all individuals, no institutional/corporate
  shareholder. First watchlist entry verified via New Zealand's company
  registry. Third-party sources cite $5.9M revenue (not a company
  disclosure, treated cautiously) and 16 staff per the NZ Herald profile
  (other sources cite 14 or 42 -- 16 used as the most recent primary
  source). No verified roster GMV or commission rate -- real revenue is
  cited for reference only, not fed into the model, same treatment as
  Side (Brazil). First New Zealand entry.
- **Liquorice** (Grey Lynn, Auckland, New Zealand) — https://www.liquorice.co.nz
  — influencer/talent agency founded 2020 by Gina Williams-Folau and
  Greer Bland, both previously at Undertow Media (Bland as founder,
  Williams-Folau as a long-time senior director) — Tracxn: unfunded.
  Verified via the New Zealand Companies Register (LIQUORICE LIMITED,
  company #8126798) —
  https://app.companiesoffice.govt.nz/companies/app/ui/pages/companies/8126798/shareholdings
  — shareholder list: Greer Elizabeth Bland (50%) and Gina Rae Williams
  (50%), both individuals, no institutional/corporate shareholder. Second
  New Zealand entry verified via that registry. Revenue is only a vague
  third-party range ($1-5M) and headcount only 5-9 (ZoomInfo/SignalHire),
  neither a reliable disclosed figure, so no roster GMV was computed;
  commission_rate=15% is a benchmark, not disclosed. Likely below the $5M
  threshold at current scale.

### Excluded (verified funded, acquired, or wrong category)
Vizz Agency (Barcelona, Spain -- Spain's leading YouTuber/streamer
representation agency, clients incl. Ibai Llanos, El Rubius, Willyrex;
acquired by Webedia in 2021), GG Talent Group (Naperville, Illinois --
raised a $20M Series A led by
Coral Tree Partners, spring 2022, then acquired by Loaded on Mar 12,
2024), Elusive Talent Agency (Montreal, Canada -- no funding rounds found, but
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
included in this watchlist under the agency subsector instead, see above),
Treasure Hunter (Seoul, South Korea -- South Korea's first independent
MCN, founded 2015 by Song Jae-yong -- but raised institutional capital
from SK Telecom ($4.3M), Industrial Bank of Korea, DSC Investment, and
Link2 Infotainment, and pursued a stock-exchange listing rather than
staying independent), SWAI (Warsaw/Berlin -- UGC/nano-influencer agency
founded by Oliwia Dumnicka; UK-registered SWAI LTD Companies House PSC
filing confirms Dumnicka as sole individual controller, no institutional
entity -- genuinely founder-owned, but only ~4 employees and no revenue
disclosed anywhere, clearly too small to approach the $5M+ threshold, so
left out on size grounds rather than a funding concern),
The Independents (Paris -- $400M raised, latest round Private Equity,
investors include Cathay Capital, TowerBrook Capital Partners, and FL
Entertainment per Crunchbase; grown via acquisitions of creative/PR
agencies), Prodigy Agency (esports talent representation, founded 2017 --
CB Insights shows $1.21M raised at Seed stage, so not bootstrapped),
The Right Fit (Darlinghurst, Australia -- talent/creator marketplace
co-founded 2016 by Taryn Williams and Aurelien Labonne -- raised $750K
seed from AirTree Ventures and SoGal Ventures per Crunchbase, then
exited to international acquirers in 2023 -- funded and acquired).

**Inconclusive, not added (needs further diligence before re-checking):**
AR Agency (Dublin, Ireland -- Ireland's first and largest influencer
talent agency, 150+ creators, founded by Andrea Roche in 2013 as a
branch of her Andrea Roche Model Agency, established 2010) -- press
reports "over EUR500,000" in one year's revenue back in 2014 and a
separate, undated "EUR850,000 in profits" figure with no clear source or
year; the operating legal entity (A.R Models Limited, Irish CRO #480816)
has accounts on file, but SoloCheck paywalls the actual figures and
ownership details (same access issue as other Irish-registry checks in
this file). Left out on data-reliability grounds -- the only free
figures are either too old or too vague to establish current scale or
funding status. Born Bred Talent (Sydney, Australia -- TikTok-first
talent agency founded 2017 by Clare Winterbourn, first to launch TikTok
talent representation in Australia/NZ, 250+ creators) -- Tracxn: "has
not raised any funding yet," 10-14 employees. No revenue figure found
anywhere, and ASIC's company register returned 403 (consistent with
Australia's registry requiring an authenticated session, no free
ownership lookup found). Also note: Winterbourn stepped away from
day-to-day operations in 2026 in favor of a new managing director and
head of finance, described in trade press as a normal founder succession
rather than an acquisition -- no ownership-change evidence found either
way. Left out on data-availability grounds (no revenue to model, no
registry confirmation) rather than any specific funding concern.

## Control cases (intentionally included, known-funded)

- **Patreon** (software) — CIK 0001860300, Form D on file — validates the
  EDGAR check flags a real institutionally-funded company correctly.
