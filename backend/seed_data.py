from datetime import datetime
from .models import Memory

SEED_MEMORIES: list[Memory] = [
    # ── SUCCESSES ────────────────────────────────────────────────────────────────

    Memory(
        id="mem_s001",
        title="Developer-First GTM Won 12 Community Banks on Real-Time Payments",
        description="Leading with sandbox access and a dedicated Slack channel converted 12 community banks in 6 months vs. zero via the standard deck-and-demo motion.",
        content=(
            "Community banks were skeptical after two failed core-banking migrations. "
            "We repositioned away from feature comparisons and led with a free 30-day sandbox, "
            "API docs in plain English, and a dedicated Slack channel with our engineers. "
            "The decision maker was always CTO-adjacent. "
            "Won 12 banks at 2.1× average ACV versus the prior enterprise motion."
        ),
        outcome_type="success",
        merchant_segment="community banks",
        pdlc_phase="launch",
        product_category="real-time payments",
        lessons=[
            "Community bank CTOs distrust marketing decks — lead with working code and sandbox",
            "Sandbox-first GTM compresses sales cycle by ~40% for technical buyers",
            "Published integration scorecards create internal champions in IT teams",
            "Slack channel access during eval is a hard differentiator against FIS and Fiserv legacy",
        ],
        competitor_context=(
            "FIS and legacy Fiserv led with compliance slides. "
            "Stripe had no banking-grade real-time rails. "
            "We won purely on developer experience."
        ),
        timestamp="2024-03-15T09:00:00",
        source="win_loss_analysis",
    ),

    Memory(
        id="mem_s002",
        title="Embedded Finance Bundle Slashed Deal Cycle 40% for Property-Management SaaS",
        description="White-labeling the full payments + disbursements stack as a single SKU for vertical SaaS platforms eliminated procurement friction and cut time-to-signed by 40%.",
        content=(
            "Property-management SaaS buyers had no appetite to evaluate payments and "
            "disbursements separately — two RFPs, two security reviews. "
            "We bundled into one 'Embedded Finance Suite' SKU with a single MSA. "
            "The anchor message: 'Your landlords get paid same day, your platform looks like a bank.' "
            "Closed 7 enterprise logos in Q3, avg deal size $480K ARR."
        ),
        outcome_type="success",
        merchant_segment="vertical SaaS — property management",
        pdlc_phase="launch",
        product_category="embedded finance",
        lessons=[
            "Vertical SaaS buyers hate multi-vendor procurement; bundle aggressively",
            "Anchor GTM message on the end-customer outcome ('landlords paid same day'), not our features",
            "Single MSA with unified pricing removes the #1 stall point in mid-market SaaS deals",
            "Reference customer in the same vertical closes the next 3 deals on its own",
        ],
        competitor_context=(
            "Stripe Treasury required significant custom dev. "
            "Adyen had no landlord-disbursement story. "
            "We were the only ones with an off-the-shelf bundle."
        ),
        timestamp="2023-10-22T11:30:00",
        source="win_loss_analysis",
    ),

    Memory(
        id="mem_s003",
        title="ROI Calculator in Discovery Call 3×'d Fraud API Conversion for Enterprise E-Commerce",
        description="Shifting from feature demos to a live ROI calculator in the first call increased enterprise e-commerce conversion from 18% to 54% in a single quarter.",
        content=(
            "Enterprise e-commerce fraud teams were drowning in vendor pitches all claiming '99% detection rates.' "
            "We changed the discovery call script: instead of a demo, we asked for last quarter's chargeback data "
            "and ran a live ROI calc showing dollar recovery. "
            "Average recovery projected: $2.3M annually. "
            "Deals closed at 2.3× typical ACV; one logo was Nordstrom Rack equivalent."
        ),
        outcome_type="success",
        merchant_segment="enterprise e-commerce",
        pdlc_phase="launch",
        product_category="fraud prevention",
        lessons=[
            "Lead with a live ROI calculator using the prospect's own data — not generic benchmarks",
            "Enterprise fraud buyers care about dollar recovery, not detection-rate percentages",
            "First-call value > feature demo: if they can't see ROI in 30 minutes, they don't come back",
            "Chargeback data request as a discovery question signals seriousness and disqualifies tire-kickers",
        ],
        competitor_context=(
            "Forter and Signifyd used generic detection-rate slides. "
            "We won by making the buyer feel the money before the contract."
        ),
        timestamp="2024-06-10T14:00:00",
        source="win_loss_analysis",
    ),

    Memory(
        id="mem_s004",
        title="Cost-Savings Anchor Drove 3× Conversion for Cross-Border FX Among Export SMBs",
        description="Repositioning from 'global payments infrastructure' to 'save $3,400/month in wire fees' tripled conversion among SMB exporters.",
        content=(
            "SMB exporters were hit with $3K–$8K monthly in wire fees and FX spread. "
            "Our previous GTM led with 'real-time global rails' — abstract and unconvincing. "
            "We built a fee-comparison calculator, ran LinkedIn ads targeting CFOs of $2M–$20M exporters, "
            "and changed the CTA from 'request a demo' to 'see your wire-fee savings in 60 seconds.' "
            "Inbound leads tripled; conversion from trial to paid hit 67%."
        ),
        outcome_type="success",
        merchant_segment="SMB exporters",
        pdlc_phase="launch",
        product_category="cross-border payments",
        lessons=[
            "SMB buyers buy on savings, not infrastructure — quantify the pain before pitching the product",
            "'See your savings in 60 seconds' is a better CTA than 'request a demo' for cost-conscious SMBs",
            "LinkedIn targeting of CFO + exporter title + company size outperformed search ads 4:1",
            "Trial-to-paid conversion is the real metric for SMB — optimize onboarding, not the sales call",
        ],
        competitor_context=(
            "Wise Business dominated brand awareness but had no enterprise-grade compliance. "
            "Airwallex was strong in APAC. "
            "Our edge was US compliance depth + FX cost transparency."
        ),
        timestamp="2023-07-05T10:00:00",
        source="post_mortem",
    ),

    Memory(
        id="mem_s005",
        title="Tap-to-Pay SDK for Regional Banks Won on Integration-Time Guarantee",
        description="Offering a contractual 30-day integration SLA — backed by a dedicated implementation pod — was the decisive factor over Stripe Terminal in 8 of 9 regional bank deals.",
        content=(
            "Regional banks evaluated Stripe Terminal and our Tap-to-Pay SDK head to head. "
            "Feature parity was roughly equal. "
            "We introduced a contractual '30-day integration or fee waived' guarantee backed by a "
            "4-person implementation pod. "
            "That removed the biggest risk in the minds of bank IT: a failed integration project. "
            "Won 8 of 9 competitive evaluations."
        ),
        outcome_type="success",
        merchant_segment="regional banks",
        pdlc_phase="launch",
        product_category="tap-to-pay SDK",
        lessons=[
            "When features are at parity, the GTM win comes from risk removal, not product differentiation",
            "A contractual integration SLA converts IT skeptics into internal champions",
            "Implementation pod as a GTM motion increases deal size AND win rate simultaneously",
            "Regional banks respond to 'fee waived if we fail' — it signals confidence and skin in the game",
        ],
        competitor_context=(
            "Stripe Terminal had a superior developer experience but no integration guarantee. "
            "We competed on risk, not technology."
        ),
        timestamp="2024-01-18T09:30:00",
        source="win_loss_analysis",
    ),

    # ── FAILURES ─────────────────────────────────────────────────────────────────

    Memory(
        id="mem_f001",
        title="BNPL for Micro-Merchants Failed — Unit Economics Broke Under $100K GMV",
        description="BNPL rollout to merchants under $100K GMV produced 78% churn in 90 days because fraud rate + interchange ate the margin.",
        content=(
            "We expanded BNPL to micro-merchants (<$100K annual GMV) after strong results in mid-market. "
            "Fraud rate was 3.8× higher in this segment (no fraud team, manual review). "
            "Interchange yield was insufficient to absorb losses. "
            "78% of micro-merchant cohort churned within 90 days. "
            "Cost of the campaign: $2.1M with net negative LTV per merchant."
        ),
        outcome_type="failure",
        merchant_segment="micro-merchants",
        pdlc_phase="launch",
        product_category="BNPL",
        lessons=[
            "Never expand a product to a lower-GMV segment without re-underwriting unit economics from scratch",
            "Fraud rate is a function of segment sophistication, not product — segment before pricing",
            "90-day churn in a new segment is a unit-economics failure, not a product failure",
            "Pilot with a cohort of 50 merchants before a full segment launch to validate LTV",
        ],
        competitor_context=(
            "Klarna and Afterpay both have GMV floors on merchant eligibility for this exact reason. "
            "We ignored a public signal that should have been a guardrail."
        ),
        timestamp="2023-11-30T16:00:00",
        source="post_mortem",
    ),

    Memory(
        id="mem_f002",
        title="Crypto Settlement for US Enterprise Retailers Stalled — Regulatory Uncertainty Killed 6 Deals",
        description="Six enterprise pipeline deals for crypto settlement stalled in legal review and never closed due to unresolved SAR and FinCEN guidance gaps.",
        content=(
            "We launched a crypto settlement product for enterprise US retailers in Q2 2023. "
            "Six deals progressed to contract stage. "
            "All six stalled when legal teams flagged unresolved SAR filing obligations and ambiguous FinCEN guidance on crypto receipts. "
            "Sales cycle stretched from 60 to 340+ days with no path to close. "
            "Total pipeline value written off: $4.8M ARR."
        ),
        outcome_type="failure",
        merchant_segment="enterprise US retailers",
        pdlc_phase="launch",
        product_category="crypto settlement",
        lessons=[
            "Never launch a product into a regulatory grey zone for enterprise buyers — legal review will kill the deal",
            "If the product can't get through the buyer's legal team in 60 days, it's not ready to sell",
            "Regulatory clarity is a GTM prerequisite for fintech enterprise sales, not a post-launch concern",
            "Map the buyer's legal review checklist before building, not after pipeline stalls",
        ],
        competitor_context=(
            "Stripe explicitly avoided US enterprise crypto settlement for this regulatory reason. "
            "We failed to treat that signal as a market read."
        ),
        timestamp="2023-09-14T13:00:00",
        source="post_mortem",
    ),

    Memory(
        id="mem_f003",
        title="Loyalty Rewards as Anchor Feature Bombed for Payment Terminal Launch",
        description="Anchoring terminal GTM on loyalty rewards confused buyers who cared exclusively about uptime and settlement speed — lost 4 of 5 competitive evals.",
        content=(
            "Product marketing led the payment terminal launch with loyalty rewards as the headline feature. "
            "In 5 competitive evaluations against Square and Clover, buyers consistently steered the conversation "
            "back to uptime SLAs and next-day settlement. "
            "Lost 4 of 5 evals. "
            "Exit interviews revealed loyalty was viewed as 'nice to have' — reliability was the purchase criterion."
        ),
        outcome_type="failure",
        merchant_segment="brick-and-mortar SMB retail",
        pdlc_phase="launch",
        product_category="payment terminals",
        lessons=[
            "Always validate anchor feature selection with buyer-priority research before campaign launch",
            "SMB brick-and-mortar terminal buyers rank reliability and settlement above any value-add feature",
            "Leading with secondary features signals product immaturity to experienced buyers",
            "Exit interviews after lost evals are mandatory — patterns emerge after the third loss",
        ],
        competitor_context=(
            "Square and Clover both lead on reliability + next-day settlement in all SMB materials. "
            "We anchored on a feature nobody was buying on."
        ),
        timestamp="2024-02-28T10:00:00",
        source="post_mortem",
    ),

    Memory(
        id="mem_f004",
        title="White-Label Digital Wallet for Insurance Companies — 18-Month Sales Cycle, Zero Closes",
        description="Insurance companies were too far from the core payments use case; procurement and compliance reviews stretched to 18 months with zero signed contracts.",
        content=(
            "We targeted P&C insurance companies as a new vertical for white-label digital wallets "
            "to disburse claims payouts. "
            "In theory, a natural fit. "
            "In practice, insurance procurement required 6 separate compliance reviews, "
            "a state insurance regulator sign-off, and a payments counsel opinion in each state. "
            "Average sales cycle reached 18 months. "
            "Zero contracts signed in 24 months of effort. "
            "Cost: 3 FTE sales engineers for 2 years."
        ),
        outcome_type="failure",
        merchant_segment="P&C insurance companies",
        pdlc_phase="launch",
        product_category="digital wallet",
        lessons=[
            "Regulated industries have layered procurement that compounds sales cycle — model it before entering",
            "A vertical can be a natural product fit but still be a terrible GTM segment due to procurement structure",
            "If a vertical requires regulator approval to buy your product, it is not a short-cycle segment",
            "Run a 90-day pilot deal with a single buyer before committing a full sales motion to a new vertical",
        ],
        competitor_context=None,
        timestamp="2023-05-12T09:00:00",
        source="post_mortem",
    ),

    Memory(
        id="mem_f005",
        title="Open Banking Aggregation for Credit Unions — Integration Complexity Caused 3 Failed Implementations",
        description="Credit unions lacked internal API capability to complete integrations; 3 of 4 pilots failed, generating P1s and destroying the reference pipeline.",
        content=(
            "Credit unions were targeted for our open banking aggregation product based on their "
            "stated interest in member data portability. "
            "What we underestimated: credit unions average 1.2 FTE developers. "
            "Integration required custom webhook handling and OAuth 2.0 configuration. "
            "3 of 4 pilot implementations failed mid-integration. "
            "Two generated P1 support tickets. "
            "The only reference logo we could have used went dark. "
            "The entire segment pipeline collapsed."
        ),
        outcome_type="failure",
        merchant_segment="credit unions",
        pdlc_phase="launch",
        product_category="open banking aggregation",
        lessons=[
            "Assess the buyer's internal technical capability before selling an integration-heavy product",
            "If the segment averages <2 FTE developers, include managed implementation in the base price",
            "Failed pilots are worse than no pilots — they destroy reference pipelines",
            "P1 tickets from a new segment kill the sales motion faster than any competitor",
        ],
        competitor_context=(
            "Plaid had already exited the credit union segment for this exact reason. "
            "We entered a market a sophisticated competitor had consciously abandoned."
        ),
        timestamp="2023-08-20T15:00:00",
        source="post_mortem",
    ),

    Memory(
        id="mem_f006",
        title="Adyen Competitor Loss: Mid-Market Restaurant Chain Chose Adyen on Global Consolidation Story",
        description="Lost a 200-location restaurant chain to Adyen because their single-platform story across US, UK, and EU resonated more than our domestic-strength pitch.",
        content=(
            "A 200-location casual dining chain with US, UK, and 3 EU markets evaluated us against Adyen. "
            "We led with domestic payment processing strength and POS integrations. "
            "Adyen framed the entire conversation as 'one platform, one reconciliation file, one support call "
            "for all 5 countries.' "
            "The CFO cited FX consolidation savings and reduced treasury complexity. "
            "We lost. "
            "The decision was made at CFO level, not the Head of IT we were pitching."
        ),
        outcome_type="failure",
        merchant_segment="mid-market multi-location restaurant chains",
        pdlc_phase="launch",
        product_category="payment processing",
        lessons=[
            "Multi-country restaurant chains buy on treasury simplification, not POS feature depth",
            "Identify the real economic buyer early — CFO beats Head of IT for multi-country deals",
            "When Adyen is in the deal, reframe to domestic depth + partnership vs. global consolidation",
            "Never pitch domestic strength to a buyer with active international expansion plans",
        ],
        competitor_context=(
            "Adyen's global consolidation story wins CFO-level decisions in multi-country restaurant chains. "
            "Counter by leading with a CFO-level treasury complexity analysis, not IT features."
        ),
        timestamp="2024-04-08T11:00:00",
        source="win_loss_analysis",
    ),
]
