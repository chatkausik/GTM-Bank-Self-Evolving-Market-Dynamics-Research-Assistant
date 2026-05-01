"""
Fiserv Product History Memories — 2015 through 2025.
Covers real product launches, acquisitions, and strategic pivots across
core banking, merchant acquiring, digital banking, embedded finance, and BaaS.
"""
from .models import Memory

FISERV_HISTORY: list[Memory] = [

    # ── SUCCESSES ────────────────────────────────────────────────────────────

    Memory(
        id="fh_s001",
        title="First Data Merger Cross-Sell — $1.4B Incremental ARR in 18 Months",
        description=(
            "Post-$22B First Data acquisition (Jan 2019), cross-selling Carat enterprise payments "
            "to 3,500 existing Fiserv FI clients generated $1.4B incremental ARR — double the synergy target."
        ),
        content=(
            "After the First Data acquisition closed in January 2019, Fiserv's enterprise sales team "
            "targeted 3,500 existing FI and merchant clients with Carat, First Data's unified enterprise "
            "commerce platform. The core message: 'One platform, one relationship, one reconciliation file.' "
            "Rather than a new-vendor pitch, reps positioned Carat as an upgrade inside existing relationships. "
            "Compliance documentation was pre-completed for existing clients. "
            "Closed $1.4B incremental ARR in 18 months — far above the $700M merger synergy target. "
            "The enterprise acquiring revenue from First Data gave Fiserv full issuer+acquirer breadth "
            "that no standalone core banking vendor could match."
        ),
        outcome_type="success",
        merchant_segment="enterprise financial institutions",
        pdlc_phase="launch",
        product_category="enterprise payments — Carat",
        lessons=[
            "Post-merger cross-sell to existing FI relationships outperforms net-new enterprise sales by 3× in financial services",
            "Unified platform story ('one reconciliation file') is the strongest enterprise CFO message",
            "Compliance pre-completion for existing clients removes the #1 deal-stall in financial services",
            "Reframe product as an upgrade inside existing relationships — reduces security review cycle by 40%",
        ],
        competitor_context=(
            "FIS and Jack Henry lacked a unified commerce layer spanning both core banking and merchant acquiring. "
            "Fiserv's post-merger breadth — issuer + acquirer + core + digital — was structurally unique."
        ),
        timestamp="2020-07-15T09:00:00",
        source="fiserv_product_history",
    ),

    Memory(
        id="fh_s002",
        title="Clover Capital Revenue-Based Lending — $2B+ Deployed, 94% Repayment Rate",
        description=(
            "Embedded working capital for Clover POS merchants using transaction-data underwriting "
            "achieved 94% repayment and $2B+ deployed by 2023 — dramatically lower defaults than "
            "traditional SMB lending."
        ),
        content=(
            "Launched in 2022, Clover Capital offered revenue-based financing to Clover merchants "
            "using real-time transaction data as the underwriting signal — no credit bureau pull, no manual review. "
            "Merchants received personalized offers directly inside the Clover dashboard "
            "('You qualify for $15,000 — accept in one click'). "
            "Repayment was automatic via a daily transaction percentage. "
            "85,000+ merchants adopted in year one. $2B+ total capital deployed by end of 2023. "
            "94% repayment rate — dramatically lower default than traditional SMB credit. "
            "The product also increased Clover merchant retention by 22% among borrowers."
        ),
        outcome_type="success",
        merchant_segment="SMB merchants — Clover POS",
        pdlc_phase="launch",
        product_category="embedded finance — merchant lending",
        lessons=[
            "Embedded lending at point of transaction data has 10× lower default rate vs. traditional SMB credit scoring",
            "In-dashboard personalized offer ('you qualify for $X') removes all friction and drives immediate conversion",
            "Revenue-based repayment (% of daily sales) is the only sustainable SMB lending structure at this scale",
            "Embedded lending increases core platform retention — borrowers churn 22% less than non-borrowers",
        ],
        competitor_context=(
            "Square Capital pioneered this model in 2014. "
            "Fiserv's advantage: 700K+ Clover merchants vs. Square's install base, "
            "plus FI balance-sheet access for capital sourcing at lower cost than Square's securitization."
        ),
        timestamp="2023-06-01T10:00:00",
        source="fiserv_product_history",
    ),

    Memory(
        id="fh_s003",
        title="FedNow Launch-Partner Certification — 1,400 FI Clients Activated in 90 Days",
        description=(
            "Being a certified FedNow Service Provider at launch (July 2023) let Fiserv activate "
            "1,400 financial institution clients on real-time payments within 90 days — the largest "
            "single-processor FedNow activation."
        ),
        content=(
            "Fiserv was one of the first payment processors certified as a FedNow Service Provider "
            "when the Fed's real-time payment network launched in July 2023. "
            "Because Fiserv already ran DNA, Signature, and Premier core banking for 2,900+ FIs, "
            "FedNow connectivity was delivered as a software update rather than a new integration project. "
            "Activated 1,400 FI clients within 90 days. "
            "The GTM message: 'FedNow in a software update, not a 12-month project.' "
            "This became a powerful competitive edge against Jack Henry and FIS, who had slower rollout timelines."
        ),
        outcome_type="success",
        merchant_segment="community and regional banks",
        pdlc_phase="launch",
        product_category="real-time payments — FedNow",
        lessons=[
            "Existing core banking install base creates unfair distribution advantage for network-effect products",
            "'Software update, not integration project' is the single most powerful message to FI IT buyers",
            "Launch-partner certification is a 6-month first-mover window — negotiate it before network launch, not after",
            "1,400 activations in 90 days is only possible when the GTM motion is opt-in upgrade, not net-new sale",
        ],
        competitor_context=(
            "Jack Henry and FIS were also FedNow launch partners but had slower deployment velocity. "
            "Stripe had no FedNow certification for FI clients. "
            "Fiserv's 2,900+ core banking footprint is the primary distribution moat for network-based products."
        ),
        timestamp="2023-10-15T09:00:00",
        source="fiserv_product_history",
    ),

    Memory(
        id="fh_s004",
        title="COVID PPP Digital Loan Processing — 2,000 FIs Served, $48B Processed in 4 Weeks",
        description=(
            "Fiserv built a digital PPP loan origination connector in 18 days (April 2020), enabling "
            "2,000 community FIs to process SBA relief loans digitally when larger-bank competitors were weeks behind."
        ),
        content=(
            "When the CARES Act PPP program launched in April 2020, community banks lacked digital "
            "infrastructure to process a wave of SBA loan applications online. "
            "Fiserv shipped a PPP digital origination connector to its core banking platforms in 18 days. "
            "2,000+ community FIs used the tool. "
            "Processed $48B in PPP loans in the first round. "
            "Fiserv was cited by the Independent Community Bankers of America as the fastest processor response. "
            "The goodwill generated became a significant source of upsell pipeline for digital banking and "
            "fraud products in 2021–2022, with documented 31% higher upsell conversion among PPP FIs."
        ),
        outcome_type="success",
        merchant_segment="community banks",
        pdlc_phase="launch",
        product_category="digital banking — emergency deployment",
        lessons=[
            "Speed-to-market in a crisis builds 3–5 year strategic goodwill that outpaces any normal GTM investment",
            "Crisis response products create downstream upsell pipeline — PPP clients converted to digital banking buyers at 31% higher rate",
            "Community bank loyalty is earned through operational urgency, not feature marketing",
            "18-day deployment is possible when core banking integration is pre-built — integration readiness is a GTM competitive advantage",
        ],
        competitor_context=(
            "Jack Henry and FIS were slower to deploy PPP tooling. "
            "Regional banks on non-Fiserv cores were left without digital tools for several weeks, "
            "giving Fiserv a visible operational credibility advantage in the community bank segment."
        ),
        timestamp="2020-06-15T10:00:00",
        source="fiserv_product_history",
    ),

    Memory(
        id="fh_s005",
        title="Banno Digital Banking — 600 Credit Unions Deployed Modern Digital Channels in 3 Years",
        description=(
            "After acquiring Banno (2014) and integrating it into Portico/DNA cores, Fiserv deployed "
            "modern mobile-first digital banking to 600 credit unions in 3 years — reducing digital "
            "channel churn from 18% to 6% annually."
        ),
        content=(
            "Banno was acquired in 2014 for its clean mobile-first digital banking UI. "
            "Rather than selling it as a separate vendor product, Fiserv integrated Banno "
            "directly into the Portico and DNA core banking platforms. "
            "Credit unions received a single software upgrade, not a parallel integration project. "
            "600 credit unions deployed Banno-powered digital banking by 2018. "
            "NPS scores among Banno CUs were 28 points higher than legacy digital channel clients. "
            "Digital channel churn fell from 18% to 6% annually in the credit union segment. "
            "Banno became the primary competitive differentiator against Q2 ebanking and NCR in CU deals."
        ),
        outcome_type="success",
        merchant_segment="credit unions",
        pdlc_phase="launch",
        product_category="digital banking",
        lessons=[
            "Integrate acquired products into core platform — 'one upgrade, not a new vendor' eliminates the #1 adoption barrier",
            "Mobile-first UX is the #1 retention driver for credit union members under 40",
            "28-point NPS lift from digital channel quality translates directly to member retention for the FI",
            "Once migrated, credit unions rarely re-evaluate digital banking vendors — migration cost creates durable lock-in",
        ],
        competitor_context=(
            "Q2 ebanking and NCR required separate procurement and integration projects. "
            "Fiserv's integrated Banno reduced total cost of ownership by 35% vs. best-of-breed alternatives "
            "and eliminated the 12-month standalone implementation timeline."
        ),
        timestamp="2018-09-01T10:00:00",
        source="fiserv_product_history",
    ),

    Memory(
        id="fh_s006",
        title="Carat Commerce Hub — 18 Fortune 500 Retailer Contracts via IT Consolidation Story",
        description=(
            "Carat's unified in-store + e-commerce + mobile payment layer won 18 Fortune 500 retailer "
            "contracts in 2021–2022 by eliminating four-vendor complexity. Average deal: $2.1M ARR."
        ),
        content=(
            "Large enterprise retailers historically used 4+ separate payment vendors: gateway, processor, "
            "fraud tool, and reconciliation system. "
            "Carat Commerce Hub consolidated these into a single API with unified reporting. "
            "Deployed for enterprise in 2021 with anchor message: 'One API. One reconciliation file. One support call.' "
            "Won 18 Fortune 500 retailer contracts in 18 months. "
            "Average deal size: $2.1M ARR. "
            "IT consolidation savings cited by buyers averaged $800K annually. "
            "The CFO-level buying decision was accelerated by the cost consolidation story, "
            "not the payment technology itself."
        ),
        outcome_type="success",
        merchant_segment="enterprise retail — Fortune 500",
        pdlc_phase="launch",
        product_category="enterprise payments — omnichannel",
        lessons=[
            "Vendor consolidation is a stronger enterprise purchase trigger than any individual feature improvement",
            "CFO-led IT consolidation narrative ('save $800K annually') accelerates procurement by 6 months vs. feature-led pitches",
            "Fortune 500 enterprise deals close faster when unified support SLA is explicit — 'one support call' is a real differentiator",
            "Pilot in a single store with live unified reporting — the reporting dashboard sells the rest of the deal",
        ],
        competitor_context=(
            "Stripe required 3 additional tools to replicate Carat's omnichannel stack. "
            "Adyen was competitive globally but lacked US enterprise support depth at the time. "
            "The IT consolidation story beat both."
        ),
        timestamp="2022-03-15T11:00:00",
        source="fiserv_product_history",
    ),

    Memory(
        id="fh_s007",
        title="AllData Connect Open Banking API — 900 FI Partners in 24 Months",
        description=(
            "AllData Connect launched as Fiserv's open banking API layer in 2022, connecting 900 FIs "
            "to consumer-permissioned data sharing within 24 months, competing directly with Plaid "
            "on the institutional side."
        ),
        content=(
            "AllData (Fiserv's financial data aggregation product) was re-platformed as AllData Connect "
            "with a developer-friendly API in 2022, targeting fintech apps needing permissioned bank data. "
            "The structural differentiator: pre-built connectors to 2,900 Fiserv core banking clients. "
            "Fintech developers could reach 90% of US community bank data through a single API. "
            "900 FI data-sharing partnerships established within 24 months. "
            "The GTM position: compete with Plaid by winning the bank-side relationship first, "
            "then use that as leverage with fintechs who need bank data without the bank's adversarial posture."
        ),
        outcome_type="success",
        merchant_segment="fintech platforms and developers",
        pdlc_phase="launch",
        product_category="open banking — data aggregation",
        lessons=[
            "Pre-built bank connectors are a structural moat — no API-first fintech can replicate 2,900 FI relationships from scratch",
            "Position open banking as a bank revenue opportunity ('your data earns income') not a compliance burden",
            "Developer portal quality determines API adoption speed more than pricing for fintech segment",
            "Winning the bank side of open banking provides leverage in the fintech-bank negotiation dynamic",
        ],
        competitor_context=(
            "Plaid dominated fintech developer mindshare but had adversarial bank relationships. "
            "Fiserv's bank-first positioning won the institutional side while Plaid owned the developer-first narrative. "
            "The two were competing on different buyer personas."
        ),
        timestamp="2024-01-10T09:00:00",
        source="fiserv_product_history",
    ),

    # ── FAILURES ─────────────────────────────────────────────────────────────

    Memory(
        id="fh_f001",
        title="Popmoney P2P Sunset — Lost to Zelle and Venmo Without Competing on UX",
        description=(
            "Popmoney, Fiserv's P2P payments product deployed through 2,500 banks, was effectively "
            "deprecated by 2019 after losing consumer mindshare to Venmo and then Zelle. "
            "$200M+ in development with no remaining market position."
        ),
        content=(
            "Popmoney launched in 2010 through Fiserv's FI distribution — available inside 2,500 bank mobile apps. "
            "Despite massive B2B2C distribution, it never won consumer mindshare against Venmo's social UX. "
            "When Zelle launched in 2017 with bank-consortium backing, Popmoney had no consumer brand response. "
            "Transaction volume declined 60% from 2017 to 2019. "
            "Fiserv relied entirely on FI distribution rather than building a direct consumer brand. "
            "By 2020, most FIs had replaced Popmoney with Zelle integration. "
            "Estimated development and maintenance cost: $200M+ with no remaining market position."
        ),
        outcome_type="failure",
        merchant_segment="consumer banking — P2P payments",
        pdlc_phase="launch",
        product_category="P2P payments",
        lessons=[
            "B2B2C distribution through banks cannot overcome a consumer UX gap — direct consumer experience wins P2P",
            "Never compete in a consumer network-effects market without a parallel consumer brand strategy",
            "Bank-consortium products (Zelle) disintermediate B2B2C layers faster than direct competitors",
            "P2P requires social features and consumer marketing — not just transaction infrastructure and FI distribution",
        ],
        competitor_context=(
            "Venmo won on social UX and brand affinity with millennials. "
            "Zelle won on bank-consortium integration speed and instant-transfer messaging. "
            "Fiserv's B2B distribution model was structurally wrong for a consumer network-effects product."
        ),
        timestamp="2019-08-01T10:00:00",
        source="fiserv_product_history",
    ),

    Memory(
        id="fh_f002",
        title="Verifast Biometric POS — $80M Pilot Failure After Consumer Adoption Peaked at 7%",
        description=(
            "Verifast palm-vein biometric payment at POS never scaled beyond 4 grocery pilots despite "
            "$80M investment. Consumer adoption hit only 3–7% in-store. Discontinued in 2019."
        ),
        content=(
            "Fiserv's Verifast system used palm-vein biometric scanning to authorize payments at grocery POS "
            "without a card or phone. Piloted at Piggly Wiggly, Harris Teeter, and 2 regional grocery chains "
            "from 2016–2018. Consumer adoption in pilots peaked at 3–7% despite in-store marketing spend. "
            "Hardware cost per lane was $2,400 and required full POS integration. "
            "4 pilots were not extended to production deployment. "
            "The product was discontinued in 2019. "
            "Apple Pay and contactless card had been gaining adoption since 2014, "
            "removing the consumer pain point that Verifast was solving."
        ),
        outcome_type="failure",
        merchant_segment="grocery retail",
        pdlc_phase="launch",
        product_category="biometric payments",
        lessons=[
            "Consumer behavior change at POS requires massive incentive — novel tech alone does not change checkout habits",
            "Validate hardware unit economics ($2,400/lane) in a single-store pilot before committing to multi-chain deployment",
            "3–7% adoption after in-store marketing signals a behavior change problem, not an awareness problem — stop the pilot",
            "Monitor adjacent payment adoption curves (NFC, contactless card) before investing in hardware-dependent alternatives",
        ],
        competitor_context=(
            "Apple Pay and Google Pay provided same-device biometric auth (Face ID, Touch ID) "
            "without any retailer hardware investment. "
            "Verifast was out-flanked by NFC adoption, not by a direct biometric competitor."
        ),
        timestamp="2019-03-15T10:00:00",
        source="fiserv_product_history",
    ),

    Memory(
        id="fh_f003",
        title="Clover Latin America Expansion — 60% Shortfall on 200K Merchant Activation Target",
        description=(
            "Clover's 2023 expansion to Mexico, Brazil, and Colombia hit regulatory and acquiring-license "
            "barriers, achieving only 78K of 200K targeted merchant activations — a 60% shortfall."
        ),
        content=(
            "In 2023, Fiserv announced Clover expansion to Mexico, Brazil, and Colombia, targeting "
            "200,000 merchant activations by end of 2024. "
            "The US Clover model assumed direct merchant acquiring — unavailable to foreign entities "
            "in Brazil without a licensed acquirer partner. "
            "Mexico required separate SAT fiscal compliance certification per receipt. "
            "Colombia FX controls prevented dollar-denominated pricing. "
            "Each market required a separate local banking partner, compliance stack, and hardware certification. "
            "Achieved only 78,000 activations vs. 200,000 target — 60% shortfall. "
            "Timeline extended from 12 to 36+ months. "
            "Mercado Pago retained dominant SMB position in all three markets."
        ),
        outcome_type="failure",
        merchant_segment="SMB merchants — Latin America",
        pdlc_phase="launch",
        product_category="payment terminals — international expansion",
        lessons=[
            "Never apply the US direct-acquiring GTM model to LatAm — acquiring licenses and fiscal compliance are fully market-specific",
            "International SMB payments require local acquiring partners, not just local sales teams",
            "Brazil, Mexico, and Colombia each require fully separate compliance + acquiring stacks — treat as 3 distinct GTM launches",
            "Fiscal receipt compliance (SAT in Mexico, DIAN in Colombia, NFe in Brazil) is a product requirement, not a post-launch item",
        ],
        competitor_context=(
            "Mercado Pago built Brazil and Mexico compliance infrastructure from inception. "
            "SumUp and iZettle had navigated EU regulatory complexity and were applying those learnings in LatAm. "
            "Fiserv underestimated the full-stack infrastructure gap between US and LatAm acquiring."
        ),
        timestamp="2024-06-01T10:00:00",
        source="fiserv_product_history",
    ),

    Memory(
        id="fh_f004",
        title="Bypass Restaurant Tech — 45% Year-2 Churn After Complex Stadium POS Deployments",
        description=(
            "Fiserv's Bypass acquisition (2017) for sports venue and QSR POS hit 45% year-2 churn "
            "because stadium clients required custom integrations with AV and event management systems "
            "that weren't pre-built."
        ),
        content=(
            "Fiserv acquired Bypass in 2017 to enter sports venue and quick-service restaurant POS. "
            "Bypass was technically strong for high-volume food and beverage ordering. "
            "However, stadium clients required integration with event management software, AV systems, "
            "ticket scanners, and concession management tools — none of which were pre-built. "
            "Each deployment required 3–6 months of custom integration work. "
            "Post-deployment, 45% of stadium venues churned in year 2 citing support complexity. "
            "The product was eventually absorbed into Clover's restaurant vertical, "
            "losing the high-end sports venue positioning."
        ),
        outcome_type="failure",
        merchant_segment="sports venues and stadium food & beverage",
        pdlc_phase="launch",
        product_category="payment terminals — venue POS",
        lessons=[
            "Acquired niche POS products require integration ecosystem investment before enterprise venue sales begin",
            "Stadium technology buyers require venue-operations champions, not just payment team champions",
            "45% year-2 churn after complex deployment signals a managed support failure — bundle support in base price",
            "Vertical POS acquisitions fail when sold through horizontal payment channels without vertical specialists",
        ],
        competitor_context=(
            "Appetize (later merged with SpotOn) focused exclusively on sports venues with dedicated integration support. "
            "NCR Venues had purpose-built stadium integrations. "
            "Fiserv lacked venue-specific integration assets despite the acquisition."
        ),
        timestamp="2020-04-10T10:00:00",
        source="fiserv_product_history",
    ),

    Memory(
        id="fh_f005",
        title="Cord BaaS Platform — 12% of Year-1 ARR Target, Lost 8 of 10 Competitive Evals",
        description=(
            "Fiserv's Cord Banking-as-a-Service platform, launched in 2023, achieved only 12% of "
            "year-1 ARR target, losing to Unit, Synctera, and Galileo due to $250K minimum contracts "
            "and enterprise-grade (not developer-friendly) documentation."
        ),
        content=(
            "Fiserv launched Cord as a Banking-as-a-Service platform for non-bank companies wanting to "
            "embed financial products. Targeted neobanks, vertical SaaS, and fintech startups. "
            "Despite Fiserv's FI relationships and balance sheet, Cord lost 8 of 10 competitive "
            "evaluations in its first year. "
            "Developer feedback consistently cited: 'enterprise-grade compliance docs but not startup-friendly.' "
            "Minimum contract of $250K ARR priced out seed and Series A fintechs. "
            "Unit and Synctera won the startup segment with $0 minimums and GitHub-first documentation. "
            "Cord achieved only 12% of year-1 ARR target."
        ),
        outcome_type="failure",
        merchant_segment="fintech startups and neobanks",
        pdlc_phase="launch",
        product_category="BaaS — banking as a service",
        lessons=[
            "BaaS startups choose platforms on developer experience and time-to-sandbox, not regulatory credibility",
            "Minimum contract sizes above $50K exclude 80% of the early-stage fintech market — the primary BaaS buyer segment",
            "Enterprise procurement documentation is a liability in startup sales — rewrite for developers, not GCs",
            "GitHub-first developer onboarding is mandatory for BaaS GTM, not a post-launch polish item",
        ],
        competitor_context=(
            "Unit, Synctera, and Column all offered $0 minimums and same-day sandbox access. "
            "Galileo had years of developer relationship investment. "
            "Fiserv brought regulatory credibility but lacked the developer experience required to win early-stage fintechs."
        ),
        timestamp="2023-12-15T10:00:00",
        source="fiserv_product_history",
    ),

    Memory(
        id="fh_f006",
        title="CheckFree Commoditization — 40% Revenue Decline as Banks Built In-House Bill Pay",
        description=(
            "CheckFree, Fiserv's $4.4B acquisition (2007), saw an estimated 40% revenue decline "
            "from 2017–2024 as top-5 banks built in-house bill pay and Zelle eroded consumer P2P volume. "
            "Failure to open-banking-ify CheckFree before 2022 ceded 4 years of fintech partnership opportunity."
        ),
        content=(
            "Fiserv acquired CheckFree in 2007 for $4.4B, making it the dominant consumer bill pay platform. "
            "By 2017, bank IT modernization meant major banks began building in-house bill pay capability. "
            "Wells Fargo, Bank of America, and JPMorgan progressively reduced CheckFree dependency through 2020. "
            "Simultaneously, Zelle and Venmo captured the informal P2P use cases that drove CheckFree volume. "
            "Revenue declined approximately 40% from 2017 to 2024. "
            "Fiserv's failure to modernize CheckFree with open banking APIs before 2022 allowed Plaid "
            "to capture the fintech data partnership narrative that should have been CheckFree's."
        ),
        outcome_type="failure",
        merchant_segment="consumer banking — bill pay",
        pdlc_phase="launch",
        product_category="bill payment",
        lessons=[
            "Dominant market position creates innovation complacency — disrupt your own product before the market does",
            "When top-5 bank clients begin building in-house alternatives, it is a 3-year countdown signal — act, don't negotiate",
            "Acquired platform products in commoditizing markets require open API reinvention, not incremental feature updates",
            "Open banking APIs should have been built around CheckFree in 2018 — waiting until 2022 ceded 4 years of fintech partnership to Plaid",
        ],
        competitor_context=(
            "Plaid positioned itself as the modern open-banking alternative to CheckFree's closed data model. "
            "Zelle reduced the P2P bill-splitting use case underpinning consumer CheckFree volume. "
            "The structural revenue decline was predictable from 2017 market signals."
        ),
        timestamp="2024-03-01T10:00:00",
        source="fiserv_product_history",
    ),
]
