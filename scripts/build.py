#!/usr/bin/env python3
"""
Master build script for the Cannabisers website.

Generates ALL pages (homepage, categories, states, state+category,
city+category, listings, guides, static pages) and sitemap.xml + robots.txt.

Run: python3 scripts/build.py
"""

import os
import sys
import json
from datetime import datetime
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nav_config import (
    NAV_ITEMS, FOOTER_COLUMNS, SITE_NAME, SITE_URL,
    SITE_TAGLINE, COPYRIGHT_YEAR, CTA_HREF, CTA_LABEL,
)
from templates import (
    get_html_head, get_nav_html, get_footer_html,
    get_breadcrumb_schema, get_breadcrumb_html,
    generate_faq_html, generate_cta_section,
    generate_newsletter_signup, generate_claim_cta,
    generate_category_card, generate_state_card, generate_listing_card,
    generate_category_badge, generate_state_badge,
    generate_graph_schema, generate_local_business_schema,
    generate_article_schema, generate_related_links,
    get_page_wrapper, write_page, BASE_URL,
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.now().strftime("%Y-%m-%d")

# Track all generated paths for sitemap
ALL_PAGES = []


# =============================================================================
# LOAD DATA
# =============================================================================

def load_json(filename):
    """Load a JSON file from the data/ directory."""
    path = os.path.join(PROJECT_ROOT, "data", filename)
    with open(path, "r") as f:
        return json.load(f)


CATEGORIES = load_json("categories.json")
STATES = load_json("states.json")
LISTINGS = load_json("listings.json")

# Build lookups
CATEGORIES_BY_SLUG = {c["slug"]: c for c in CATEGORIES}
STATES_BY_SLUG = {s["slug"]: s for s in STATES}
STATES_BY_ABBREV = {s["abbrev"]: s for s in STATES}

LISTINGS_BY_STATE = defaultdict(list)
LISTINGS_BY_CATEGORY = defaultdict(list)
LISTINGS_BY_STATE_CATEGORY = defaultdict(list)
LISTINGS_BY_CITY_STATE_CATEGORY = defaultdict(list)

for listing in LISTINGS:
    st = listing.get("state", "")
    cat = listing.get("category", "")
    city = listing.get("city", "")
    LISTINGS_BY_STATE[st].append(listing)
    LISTINGS_BY_CATEGORY[cat].append(listing)
    LISTINGS_BY_STATE_CATEGORY[(st, cat)].append(listing)
    if city:
        city_key = f"{city.lower().replace(' ', '-')}-{st.lower()}"
        LISTINGS_BY_CITY_STATE_CATEGORY[(city_key, cat)].append(listing)
    # Also index by secondary categories
    for extra_cat in listing.get("categories", []):
        if extra_cat != cat:
            LISTINGS_BY_CATEGORY[extra_cat].append(listing)
            LISTINGS_BY_STATE_CATEGORY[(st, extra_cat)].append(listing)


# =============================================================================
# GUIDE DATA (inline for now, move to JSON later)
# =============================================================================

GUIDES = [
    {
        "title": "How to Choose a Cannabis Testing Lab",
        "slug": "how-to-choose-cannabis-testing-lab",
        "description": "A practical guide to evaluating cannabis testing labs by accreditation, turnaround time, pricing, and state compliance requirements.",
        "category": "testing-labs",
        "content": """
            <h2>Start with your state's approved lab list</h2>
            <p>Every legal state publishes a list of approved testing laboratories. Your lab must hold a current state license for your specific market. Using a non-approved lab means your test results won't be accepted by regulators, and your product can't legally reach shelves.</p>
            <p>Check your state cannabis authority's website for the current list. Labs gain and lose approval status regularly, so verify before every new engagement.</p>

            <h2>Verify ISO 17025 accreditation</h2>
            <p>ISO 17025 is the international standard for testing laboratory competence. While some states don't require it yet, accredited labs produce more reliable results. Ask for their certificate and verify it with the accrediting body. This matters because inconsistent test results can lead to failed batches, regulatory scrutiny, and lost revenue.</p>

            <h2>Compare turnaround times</h2>
            <p>Standard turnaround ranges from 3-7 business days for a full compliance panel. Rush services (1-2 days) typically cost 50-100% more. If you're running a high-volume operation, negotiate guaranteed turnaround times in your service agreement. Delays at the testing stage ripple through your entire supply chain.</p>

            <h2>Understand pricing structures</h2>
            <p>Labs price by the test or by the panel. A full compliance panel (potency, pesticides, heavy metals, microbials, residual solvents, terpenes) runs $150-400 per sample. Potency-only tests start at $50-75. Volume discounts kick in at 10+ samples per month. Get quotes from at least three labs before committing.</p>

            <h2>Ask about retest policies</h2>
            <p>Products fail tests. When they do, you need to know: Does the lab offer retesting at reduced cost? What's the process for challenging a result? How quickly can you resubmit? Labs with transparent retest policies save you money and time when failures happen.</p>

            <h2>Evaluate their reporting</h2>
            <p>You need Certificates of Analysis (COAs) that meet your state's requirements and are easy for your team to read. Ask for sample COAs before committing. Good labs also offer digital reporting that integrates with seed-to-sale tracking systems.</p>
        """,
        "faqs": [
            {"question": "How often should I switch cannabis testing labs?", "answer": "Most operators stick with one primary lab for consistency but maintain a relationship with a backup. Consider switching if turnaround times increase, pricing becomes uncompetitive, or you have concerns about result accuracy. Annual reviews of your lab relationship are good practice."},
            {"question": "Can I use a testing lab in a different state?", "answer": "No. Cannabis testing labs must be licensed in the state where the product was produced. Interstate commerce of cannabis is federally illegal, which means your samples can't cross state lines to reach an out-of-state lab."},
            {"question": "What's the difference between compliance testing and R&D testing?", "answer": "Compliance testing is mandatory and follows state-specific protocols to determine if your product meets legal requirements for sale. R&D testing is optional and helps you optimize your production process, test new strains, or troubleshoot quality issues. R&D tests are typically cheaper since they don't require the full regulatory panel."},
        ],
    },
    {
        "title": "Cannabis Insurance: What You Need and What It Costs",
        "slug": "cannabis-insurance-guide",
        "description": "A breakdown of the insurance policies every cannabis business needs, typical costs, and how to find brokers who actually serve the industry.",
        "category": "insurance-providers",
        "content": """
            <h2>The coverage every cannabis business needs</h2>
            <p>At minimum, you need general liability, product liability, property insurance, workers' compensation, and commercial auto. Most states require proof of insurance as a licensing condition. Beyond the mandates, product liability is critical because one contamination incident can bankrupt an uninsured operator.</p>

            <h2>Why cannabis insurance costs more</h2>
            <p>Federal illegality shrinks the carrier market. Fewer carriers means less competition and higher premiums. A dispensary pays $5,000-15,000 annually for general liability versus $1,000-3,000 for a comparable retail business. Premiums are trending down as more carriers enter the space, but the gap persists.</p>

            <h2>Crop insurance for cultivators</h2>
            <p>Standard agricultural crop insurance doesn't cover cannabis. A handful of specialty carriers offer cannabis crop coverage, but premiums are high and coverage limits are often lower than your actual crop value. Budget $10,000-50,000 annually depending on canopy size and location. If you're growing outdoors, this coverage becomes essential.</p>

            <h2>Finding a cannabis insurance broker</h2>
            <p>Most mainstream brokers can't place cannabis coverage because their carrier partners exclude it. You need a broker who works with admitted and surplus lines carriers that explicitly cover plant-touching businesses. Ask for their cannabis client count, carrier relationships, and claims handling experience. A broker with 5+ cannabis clients in your state is a good starting point.</p>

            <h2>What to watch for in policies</h2>
            <p>Read exclusions carefully. Many cannabis policies exclude coverage for regulatory fines, product recalls, mold contamination, or theft by employees. These are exactly the risks cannabis businesses face most often. Negotiate to remove or narrow these exclusions. If a carrier won't budge, find one that will.</p>
        """,
        "faqs": [
            {"question": "Does cannabis insurance cover federal enforcement?", "answer": "Generally no. Most cannabis insurance policies exclude coverage for federal enforcement actions. This is a known gap in cannabis insurance. Some carriers are beginning to offer limited federal defense coverage, but it's not standard."},
            {"question": "How do I reduce my cannabis insurance premiums?", "answer": "Implement robust security (cameras, alarms, access controls), maintain clean compliance records, bundle multiple policies with one carrier, increase your deductible, and shop quotes annually. A clean claims history is the single biggest factor in premium reduction over time."},
            {"question": "Do I need cyber insurance for my dispensary?", "answer": "If you process any customer data or use connected POS systems, yes. Cannabis businesses are increasingly targeted by cyber attacks because they handle cash and have valuable customer data. Cyber liability policies typically run $1,000-5,000 annually for dispensaries."},
        ],
    },
    {
        "title": "280E Tax Planning for Cannabis Businesses",
        "slug": "280e-tax-planning-cannabis",
        "description": "How Section 280E impacts cannabis businesses and the legal strategies CPAs use to minimize your effective tax rate from 70% to under 40%.",
        "category": "accounting-tax",
        "content": """
            <h2>What 280E actually says</h2>
            <p>Section 280E of the Internal Revenue Code says businesses trafficking in Schedule I or II controlled substances cannot deduct ordinary business expenses. Cannabis is still Schedule I federally. That means a dispensary generating $2M in revenue with $800K in normal operating expenses (rent, payroll, marketing, utilities) cannot deduct any of them. The only deduction allowed is cost of goods sold (COGS).</p>
            <p>For a cultivation operation, COGS includes seeds, soil, nutrients, grow lights, and labor directly involved in plant production. For a dispensary, COGS is essentially the wholesale cost of inventory purchased for resale. Everything else (your receptionist, your Weedmaps advertising, your accountant fees) is non-deductible.</p>

            <h2>The math that kills unprepared operators</h2>
            <p>A normal retailer with $2M revenue, $1M COGS, and $800K operating expenses pays tax on $200K profit. A cannabis dispensary with identical numbers pays tax on $1M ($2M minus $1M COGS, with $800K in expenses completely disallowed). At a 35% effective rate, that's $350K in taxes on a business that actually made $200K. You owe more than you earned.</p>
            <p>This is why cannabis businesses fail at higher rates than other retail. The tax burden is structurally designed to be punishing, and operators who don't plan for it discover the problem when their first tax return is due.</p>

            <h2>Legal strategies to maximize COGS</h2>
            <p>The key is proper cost accounting. A <a href="/categories/accounting-tax/">cannabis-specialized CPA</a> allocates every defensible dollar to COGS. For cultivators, this includes facility costs tied to production (a portion of rent, utilities, depreciation), packaging materials, quality control testing, and direct labor. For manufacturers, it includes extraction equipment, processing labor, and ingredient costs.</p>
            <p>The IRS uses the rules from IRC Section 263A to determine what qualifies as COGS for cannabis. These "uniform capitalization" rules let you include indirect costs that support production: warehouse rent, equipment maintenance, quality assurance staff, and production supervisors.</p>

            <h2>Entity structuring</h2>
            <p>Many operators split their business into plant-touching and non-plant-touching entities. The plant-touching entity (the license holder) handles cultivation, processing, or retail. The non-plant-touching entity provides management services, IP licensing, real estate, or consulting to the plant-touching entity. Non-plant-touching entities can deduct normal business expenses because 280E doesn't apply to them.</p>
            <p>This structure has to be legitimate. The IRS scrutinizes related-party transactions in cannabis. Transfer pricing between entities must reflect fair market value. Work with a <a href="/categories/cannabis-attorneys/">cannabis attorney</a> and CPA together on entity design.</p>

            <h2>What the SAFE Banking Act would change</h2>
            <p>Federal rescheduling or the SAFE Banking Act wouldn't automatically fix 280E. Rescheduling to Schedule III would remove the 280E burden entirely, but SAFE Banking only addresses financial services access. As of early 2026, 280E remains fully in effect. Plan your tax strategy assuming it stays.</p>

            <h2>Finding the right CPA</h2>
            <p>Your CPA needs direct cannabis 280E experience. Ask how many cannabis returns they've filed, whether they've handled an IRS audit of a cannabis business, and what their average COGS allocation rate is for your license type. Browse <a href="/categories/accounting-tax/">cannabis accountants and tax specialists</a> in our directory to find qualified CPAs in your state.</p>
        """,
        "faqs": [
            {"question": "Can cannabis businesses deduct rent?", "answer": "Only the portion of rent tied to production space (grow rooms, processing areas, inventory storage) can be included in COGS under Section 263A. Retail floor space, administrative offices, and break rooms are non-deductible operating expenses under 280E."},
            {"question": "What happens if I don't plan for 280E?", "answer": "You'll face an effective tax rate of 60-80% on your actual profit, which regularly exceeds 100% of true net income. Many operators discover this at tax time and can't pay. IRS payment plans for cannabis businesses carry penalties and interest that compound quickly."},
            {"question": "Is cannabis tax planning worth the cost?", "answer": "A qualified cannabis CPA costs $5,000-25,000 annually for tax planning and preparation. For a business doing $1M+ in revenue, proper 280E planning typically saves $50,000-200,000 per year in taxes. The ROI is 10-40x the cost of professional help."},
        ],
    },
    {
        "title": "Cannabis Compliance: A State-by-State Survival Guide",
        "slug": "cannabis-compliance-state-guide",
        "description": "How cannabis compliance requirements differ across states and what every operator needs to know about licensing, inspections, and staying current.",
        "category": "compliance-consultants",
        "content": """
            <h2>No two states regulate cannabis the same way</h2>
            <p>California has a dual state-and-local licensing system where cities can ban cannabis businesses entirely. Colorado was first-mover and has a relatively mature framework. Michigan opened adult-use in 2019 and is still refining its rules. New York built social equity into its licensing structure from day one. Each state's regulatory body has different priorities, different inspection cadences, and different penalties for violations.</p>
            <p>This means compliance isn't a one-size-fits-all checklist. What keeps you legal in Oregon might get your license suspended in Illinois.</p>

            <h2>The license application process</h2>
            <p>Applications range from straightforward (Oregon's relatively simple forms) to brutal (New York's social equity scoring, California's dual-track approvals). Most require: a detailed business plan, premises diagrams, security plans, financial disclosures, background checks for all owners, and proof of local approval. Application fees range from $1,000 to $50,000 depending on the state and license type.</p>
            <p>A <a href="/categories/compliance-consultants/">compliance consultant</a> who has successfully submitted applications in your state is worth the investment. They know what reviewers look for and which mistakes cause automatic rejection.</p>

            <h2>Seed-to-sale tracking</h2>
            <p>Most states require every cannabis plant and product to be tracked from seed to final sale using a state-mandated system. Metrc is the most common (used in California, Colorado, Michigan, Oregon, and others). BioTrack and Leaf Data are used in some states. Your <a href="/categories/pos-software/">POS system</a> must integrate with your state's tracking platform, and discrepancies between your inventory and the tracking system trigger automatic flags.</p>
            <p>Tracking errors are the most common compliance violation. They're usually caused by human data entry mistakes, system integration failures, or inadequate staff training. Budget for tracking system training during onboarding and refresher sessions quarterly.</p>

            <h2>Inspections: what to expect</h2>
            <p>State regulators conduct both scheduled and unannounced inspections. They check: security system functionality, camera coverage and recording retention, inventory accuracy against seed-to-sale records, packaging and labeling compliance, employee badge/credential currency, waste disposal documentation, and general facility condition.</p>
            <p>Failed inspections result in warnings, fines ($1,000-50,000 per violation), mandatory corrective action plans, or license suspension. Repeated failures lead to license revocation. The best defense is a compliance calendar with weekly self-audits.</p>

            <h2>Staying current with regulatory changes</h2>
            <p>Cannabis regulations change frequently. States amend rules multiple times per year, often with short implementation windows. Subscribe to your state cannabis authority's email updates, join your state cannabis trade association, and consider retaining a compliance consultant who monitors regulatory changes professionally.</p>
            <p>Common areas of change: testing requirements (new contaminants added), packaging rules (new warning label requirements), advertising restrictions (platform-specific bans), and tax structures (rate adjustments).</p>

            <h2>Building a compliance team</h2>
            <p>Small operations can handle compliance with a dedicated owner or manager plus an external consultant. Mid-size operations (multiple licenses or locations) need a full-time compliance officer. Large operators build internal compliance departments with dedicated staff for tracking, quality assurance, and regulatory affairs.</p>
            <p>Browse <a href="/categories/compliance-consultants/">compliance consultants</a> by state to find specialists in your market.</p>
        """,
        "faqs": [
            {"question": "How often do cannabis regulations change?", "answer": "Frequently. Most states amend their cannabis regulations 2-5 times per year. Major overhauls happen less often (every 2-3 years), but incremental changes to testing requirements, packaging rules, and licensing procedures are constant. Monitoring regulatory updates is an ongoing operational requirement."},
            {"question": "What's the most common compliance violation?", "answer": "Seed-to-sale tracking errors. Inventory discrepancies between your physical count and the state tracking system account for more violations than any other category. These are usually caused by data entry mistakes, not intentional diversion, but regulators treat them seriously regardless of intent."},
            {"question": "Do I need a compliance consultant or can I handle it myself?", "answer": "For your initial license application, a consultant dramatically improves your approval odds and saves months of back-and-forth. For ongoing compliance, small single-location operators can self-manage with proper training and systems. Multi-location or multi-state operations almost always need professional compliance support."},
        ],
    },
    {
        "title": "How to Find Cannabis-Friendly Banking",
        "slug": "cannabis-banking-guide",
        "description": "Why 85% of banks reject cannabis businesses, which financial institutions will work with you, and what it costs to bank legally.",
        "category": "banking-financial-services",
        "content": """
            <h2>Why most banks say no</h2>
            <p>Cannabis is federally illegal. Banks are federally regulated. Every dollar a cannabis business deposits creates potential liability for the bank under the Bank Secrecy Act. A bank that knowingly processes cannabis proceeds could face federal money laundering charges, lose its FDIC insurance, or trigger enforcement from FinCEN. Most national banks (Chase, Bank of America, Wells Fargo) won't touch cannabis as a policy decision.</p>
            <p>The 2014 FinCEN guidance created a pathway for banks to serve cannabis businesses through enhanced due diligence and Suspicious Activity Reports (SARs). But filing a SAR for every deposit is expensive, and many banks decided the compliance burden wasn't worth the revenue.</p>

            <h2>Who will bank cannabis businesses</h2>
            <p>Regional banks and credit unions are the primary options. These institutions are often state-chartered (reducing some federal exposure) and see cannabis banking as a competitive opportunity. As of 2026, roughly 800 financial institutions across the US serve cannabis businesses, up from fewer than 400 in 2020.</p>
            <p>Cannabis-specific fintech companies have also emerged. They partner with bank sponsors to offer deposit accounts, payment processing, and payroll services designed for the industry. Browse <a href="/categories/banking-financial-services/">cannabis banking providers</a> in your state to see what's available in your market.</p>

            <h2>What it costs</h2>
            <p>Cannabis banking is expensive compared to normal business banking. Monthly account maintenance fees run $750-2,500 (versus $10-50 for a standard business account). Cash deposit fees range from $500-1,500 per deposit event. Some banks charge a percentage of monthly deposits (0.5-2%). Wire transfer and ACH fees are also higher than standard commercial rates.</p>
            <p>Total monthly banking costs for a dispensary typically run $2,000-5,000. Cultivators and manufacturers with lower cash volumes may pay less. The cost is real, but operating in all-cash is more expensive when you factor in security, armored transport, cash counting labor, and the theft risk.</p>

            <h2>The application process</h2>
            <p>Cannabis banking applications require extensive documentation: state license copies, ownership disclosures, business plans, financial statements, compliance procedures, and sometimes on-site facility inspections. Approval takes 30-90 days. Banks conduct ongoing monitoring and may request quarterly compliance documentation.</p>
            <p>Work with a <a href="/categories/cannabis-attorneys/">cannabis attorney</a> to prepare your banking application. A well-organized package signals that you're a low-risk, compliance-focused operator.</p>

            <h2>Payment processing alternatives</h2>
            <p>True credit card processing remains unavailable for plant-touching businesses because Visa and Mastercard prohibit it at the network level. The workarounds: cashless ATM (debit-based, in a regulatory gray area), ACH transfers through cannabis-friendly processors, closed-loop payment apps, and cryptocurrency. Each has trade-offs in customer experience, compliance risk, and cost.</p>
            <p>The most sustainable approach is a compliant bank account for deposits plus ACH or debit-based payment processing for customer transactions.</p>
        """,
        "faqs": [
            {"question": "Can cannabis businesses use Venmo or Cash App?", "answer": "Technically no. Both platforms prohibit cannabis transactions in their terms of service. Accounts discovered processing cannabis payments get frozen and closed. Some operators use personal accounts for convenience, but this creates serious legal and tax problems. Use a proper cannabis banking provider."},
            {"question": "Will the SAFE Banking Act fix cannabis banking?", "answer": "The SAFE Banking Act would protect financial institutions from federal penalties for serving state-legal cannabis businesses. It would dramatically increase the number of banks willing to work with cannabis and reduce banking costs. As of early 2026, the bill has passed the House multiple times but has not cleared the Senate."},
            {"question": "What happens if my cannabis bank account gets closed?", "answer": "It happens. Banks periodically exit cannabis banking when they reassess their risk appetite. Have a backup banking relationship in place and keep at least 60 days of operating expenses accessible. When you lose a bank, your cannabis attorney and trade association can often help you find a replacement quickly."},
        ],
    },
    {
        "title": "Cannabis Packaging Compliance by State",
        "slug": "cannabis-packaging-compliance",
        "description": "Child-resistant packaging requirements, labeling rules, and exit bag regulations across major cannabis markets.",
        "category": "packaging-labeling",
        "content": """
            <h2>The baseline: child-resistant packaging</h2>
            <p>Every legal state requires cannabis products to be sold in child-resistant packaging. The standard is ASTM D3475, which means the packaging must be difficult for children under five to open but usable by normal adults. Most states require this certification documentation from your <a href="/categories/packaging-labeling/">packaging supplier</a>. Using non-certified packaging is a license-level violation.</p>
            <p>Child-resistant doesn't mean childproof. The ASTM standard requires that 85% of children in a test panel cannot open the package within five minutes, and 90% of adults can open it within the same timeframe. Pre-roll tubes, mylar bags with zip locks, and push-and-turn containers all meet this standard when properly certified.</p>

            <h2>Labeling requirements vary wildly</h2>
            <p>This is where state differences create the most operational headaches. California requires a universal cannabis symbol (the THC triangle), specific font sizes for potency numbers, and a "GOVERNMENT WARNING" statement. Colorado requires its own universal symbol, different warning language, and specific formatting for THC/CBD content per serving and per package. Michigan has yet another set of requirements.</p>
            <p>If you sell in multiple states, you need separate packaging and labels for each market. A label that's compliant in California will fail inspection in Colorado. Budget for state-specific design and print runs.</p>

            <h2>Exit bag requirements</h2>
            <p>Several states (including California and Colorado) require dispensaries to place all purchases in an opaque, child-resistant exit bag before the customer leaves the store. These bags must meet the same ASTM D3475 standard. Some states accept resealable mylar bags; others require specific bag types.</p>
            <p>Exit bags add $0.25-1.50 per transaction to your packaging costs. Order in bulk to reduce per-unit cost, and negotiate with your packaging supplier for volume pricing.</p>

            <h2>Edibles: the strictest requirements</h2>
            <p>Edible cannabis products face the tightest packaging and labeling rules. Most states cap THC at 10mg per serving and 100mg per package. Packaging must be opaque (the product can't be visible), individually dosed, and clearly labeled with serving size, total THC, ingredient list, allergen warnings, and consumption instructions. Some states ban packaging that resembles commercial candy or food products.</p>
            <p>Edible packaging errors are among the most common recall triggers. A mislabeled THC count or missing allergen warning can pull your entire batch from shelves.</p>

            <h2>Working with packaging suppliers</h2>
            <p>The right supplier understands your state's requirements and provides certification documentation proactively. Ask for: ASTM D3475 test reports, sample labels reviewed against your state's checklist, and minimum order quantities. Lead times for custom packaging are typically 4-8 weeks, so plan ahead for new product launches.</p>
            <p>Browse <a href="/categories/packaging-labeling/">cannabis packaging and labeling companies</a> to find suppliers who specialize in your state's requirements.</p>
        """,
        "faqs": [
            {"question": "What is ASTM D3475 certification?", "answer": "ASTM D3475 is the testing standard for child-resistant packaging. It requires that 85% of children under five cannot open the package within five minutes during controlled testing. Your packaging supplier should provide test reports proving their products meet this standard. Most states require this documentation as a condition of your license."},
            {"question": "Can I use the same packaging across multiple states?", "answer": "The physical container (jar, tube, bag) may work across states if it meets child-resistant standards everywhere. But labels almost certainly need to be state-specific. Warning language, required symbols, font sizes, and information placement all vary. Plan for separate label designs per market."},
            {"question": "How much does compliant cannabis packaging cost?", "answer": "Stock compliant containers (jars, tubes, bags) run $0.15-0.75 per unit at volume. Custom printed packaging adds $0.50-2.00 per unit depending on complexity. Labels cost $0.05-0.25 each. Exit bags add $0.25-1.50 per transaction. Total packaging cost typically represents 3-8% of retail product price."},
        ],
    },
    {
        "title": "Hiring Your First Cannabis Employee",
        "slug": "hiring-first-cannabis-employee",
        "description": "What cannabis businesses need to know about hiring, background checks, agent cards, and building a team in a federally illegal industry.",
        "category": "staffing-hr",
        "content": """
            <h2>The background check problem</h2>
            <p>Most states require criminal background checks for cannabis employees, but the rules on what disqualifies a candidate vary enormously. Some states bar anyone with a drug felony. Others have carved out exceptions for prior cannabis convictions, especially as social equity becomes a bigger policy priority. A few states (like Illinois) explicitly prohibit using past cannabis convictions as a disqualification for cannabis employment.</p>
            <p>Run background checks through a service that understands cannabis-specific rules in your state. A standard employment screening company may flag candidates who are perfectly eligible under your state's cannabis regulations.</p>

            <h2>Agent cards and employee licensing</h2>
            <p>Most states require cannabis employees to obtain a state-issued agent card, badge, or employee license before they can work in a cannabis facility. The application process usually involves: photo ID, background check, fingerprinting, and a fee ($50-200). Processing times range from one week to three months depending on the state.</p>
            <p>Plan for this lead time when hiring. A new employee who starts before their agent card arrives creates a compliance violation. Some states allow supervised provisional work while the card is processing; others don't.</p>

            <h2>Compensation benchmarks</h2>
            <p>Cannabis pay varies widely by role and market. Entry-level budtenders earn $15-20/hour in most markets, with higher wages in expensive cities (San Francisco, New York). Cultivation technicians earn $18-25/hour. Master growers command $80,000-150,000 annually. Dispensary managers earn $55,000-85,000. Compliance officers range from $65,000-120,000 depending on the scope of responsibility.</p>
            <p>Benefits are increasingly important for retention. The 60%+ turnover rate in cannabis retail is driven partly by compensation but mostly by lack of benefits, unpredictable scheduling, and limited advancement opportunities. Operators who offer health insurance, consistent schedules, and clear promotion paths retain staff longer.</p>

            <h2>Training requirements</h2>
            <p>State training requirements range from minimal to extensive. Colorado requires a Responsible Vendor Program for dispensary employees. California requires specific training on checking IDs and recognizing intoxication. Other states mandate training on seed-to-sale tracking, product knowledge, and safety protocols.</p>
            <p>Beyond state mandates, invest in product knowledge training. Budtenders who can explain the difference between terpene profiles, recommend appropriate products for specific needs, and answer compliance questions confidently generate higher per-ticket sales and better customer retention.</p>

            <h2>Finding cannabis-experienced talent</h2>
            <p>The talent pool is growing but still thin for specialized roles. <a href="/categories/staffing-hr/">Cannabis staffing agencies</a> maintain networks of pre-screened candidates with industry experience. For executive roles, specialized cannabis recruiters are worth the placement fee because a bad VP-level hire in cannabis costs more than in other industries (the regulatory knowledge gap is hard to overcome).</p>
            <p>For entry-level roles, recruit from adjacent industries: pharmacy techs, retail managers, and hospitality workers all transfer skills well. Focus your interview process on compliance mindset and attention to detail rather than cannabis experience alone.</p>

            <h2>Employment law considerations</h2>
            <p>Cannabis employment law is a minefield. Workers' comp claims for cannabis employees can be complicated by federal illegality. Employee drug testing policies need to exclude cannabis in legal states (some states have explicit protections). Non-compete agreements may be unenforceable. Consult a <a href="/categories/cannabis-attorneys/">cannabis attorney</a> before drafting employment agreements or HR policies.</p>
        """,
        "faqs": [
            {"question": "Can I require drug testing for cannabis employees?", "answer": "It depends on your state. Many legal states prohibit employers from penalizing employees for off-duty cannabis use. You can typically still enforce impairment policies (no being under the influence at work), but blanket THC testing as a condition of employment is increasingly restricted. Check your state's specific employment laws."},
            {"question": "How long does it take to get an employee agent card?", "answer": "Processing times range from 1-12 weeks depending on the state. California and Colorado are typically faster (1-3 weeks). States with newer programs can take 4-12 weeks. Apply for employee credentials as soon as you make a hiring decision, and check whether your state allows provisional supervised work while the card is processing."},
            {"question": "What's the turnover rate in cannabis retail?", "answer": "Industry-wide, cannabis retail turnover exceeds 60% annually. Dispensaries with competitive pay, benefits, consistent scheduling, and advancement opportunities see rates closer to 30-40%. The biggest retention factor is usually benefits and schedule predictability rather than base pay alone."},
        ],
    },
    {
        "title": "Cannabis Security Requirements by State",
        "slug": "cannabis-security-requirements",
        "description": "Surveillance, alarm, guard, and vault requirements for dispensaries and cultivation facilities across major cannabis states.",
        "category": "security-services",
        "content": """
            <h2>Video surveillance: the universal requirement</h2>
            <p>Every legal state requires video surveillance at cannabis facilities. The specifics differ, but the baseline is similar: cameras must cover all entry/exit points, point-of-sale areas, inventory storage, and any area where cannabis is handled. Recording must be continuous during operating hours, and footage must be retained for 30-90 days depending on the state.</p>
            <p>Camera resolution requirements are getting stricter. Colorado requires footage clear enough to identify individuals. California requires cameras to capture activity in "sufficient detail." Budget for high-definition IP cameras (1080p minimum, 4K increasingly recommended) with adequate lighting for nighttime recording.</p>

            <h2>Alarm systems and monitoring</h2>
            <p>Most states require commercial-grade alarm systems with 24/7 monitoring by a licensed security company. Sensors on all doors, windows, and access points. Panic buttons at point-of-sale locations. Motion detection in storage areas after hours. The alarm must notify both the monitoring company and local law enforcement within a specified timeframe.</p>
            <p>Work with a <a href="/categories/security-services/">cannabis security provider</a> who understands state-specific alarm requirements. Generic commercial alarm companies may install systems that don't meet cannabis-specific standards, which creates compliance gaps during inspections.</p>

            <h2>Access control and vaults</h2>
            <p>Cannabis facilities need tiered access control. Public areas (retail floor) are separate from limited-access areas (inventory, processing) which are separate from restricted areas (vault, server room). Most states require electronic access logs showing who entered each area and when. Biometric access (fingerprint or badge) is increasingly common for vault areas.</p>
            <p>Vault specifications vary by state. Most require a UL-rated safe or vault room with reinforced walls, a commercial-grade lock, and limited key/code access. Cash and high-value inventory must be stored in the vault when the facility is closed. Some states specify minimum wall thickness and door ratings.</p>

            <h2>Guard requirements</h2>
            <p>Some states require armed or unarmed security guards during operating hours. California leaves guard requirements to local jurisdictions. Colorado requires dispensaries to have security plans but doesn't mandate guards. Illinois requires guards at dispensaries. Check both state and local requirements, as cities often add guard mandates on top of state rules.</p>
            <p>Armed guards cost $25-45/hour. Unarmed guards cost $18-28/hour. For a dispensary open 12 hours a day, a single guard position costs $78,000-197,000 annually. Some operators share guards between adjacent cannabis businesses to reduce costs.</p>

            <h2>Transport security</h2>
            <p>Moving cannabis between facilities requires specific security measures. Most states mandate GPS-tracked vehicles, locked compartments, and transport manifests. Some require armed guards for high-value shipments. Vehicles must be unmarked (no cannabis branding) in many states.</p>
            <p>If you're moving product regularly, a relationship with a licensed cannabis <a href="/categories/transportation-distribution/">transport company</a> is more cost-effective than building an in-house transport team. They carry the proper insurance, maintain compliant vehicles, and handle manifest documentation.</p>

            <h2>Budgeting for security</h2>
            <p>Dispensary security systems (cameras, alarms, access control) typically cost $15,000-50,000 for installation plus $300-800/month for monitoring and maintenance. Cultivation facilities with larger footprints run $30,000-100,000 for initial setup. Guards add ongoing labor costs. Total annual security spending for a single-location dispensary is typically $50,000-150,000.</p>
        """,
        "faqs": [
            {"question": "How long do I need to retain surveillance footage?", "answer": "Retention requirements range from 30 to 90 days depending on the state. California requires 90 days. Colorado requires 40 days. Michigan requires 30 days. Your system needs enough storage capacity to hold the required retention period at full resolution. Cloud-based storage solutions handle this automatically but add monthly costs."},
            {"question": "Do I need armed or unarmed guards?", "answer": "It depends on your state and local regulations, the volume of cash your business handles, and your risk assessment. Dispensaries in high-crime areas or those handling large amounts of cash benefit from armed guards. Some states mandate guards regardless. Check both state and city requirements before deciding."},
            {"question": "Can I install my own security system?", "answer": "Technically yes, but it's not recommended. State regulations require systems to meet specific standards, and inspectors check for compliance. A cannabis security specialist ensures your system meets all state and local requirements from day one. DIY installations that fail inspection cost more to fix than professional installation would have cost upfront."},
        ],
    },
    {
        "title": "Choosing a Cannabis POS System",
        "slug": "choosing-cannabis-pos-system",
        "description": "How to evaluate cannabis point-of-sale systems for compliance, Metrc integration, inventory management, and daily operations.",
        "category": "pos-software",
        "content": """
            <h2>Compliance integration is non-negotiable</h2>
            <p>Your POS system must integrate with your state's seed-to-sale tracking system. For most states, that means certified Metrc integration. If your POS doesn't sync with the state tracking platform, every sale creates a manual reconciliation task, and discrepancies accumulate fast. These discrepancies trigger compliance flags that lead to inspections, fines, and potential license suspension.</p>
            <p>Check your state's list of certified integration partners. Not every POS that claims Metrc compatibility has actually completed the certification process. Ask vendors for their certification documentation and call the state tracking system provider to verify.</p>

            <h2>The major cannabis POS platforms</h2>
            <p>Dutchie (acquired Greenbits and LeafLogix) is the market leader by dispensary count. Treez focuses on enterprise operators with complex inventory needs. Flowhub emphasizes ease of use and rapid onboarding. Meadow targets California dispensaries. Each has different strengths depending on your operation size, state, and technical requirements.</p>
            <p>Demo at least three platforms before committing. Bring your compliance officer or manager to the demo and test actual workflow scenarios: processing a sale, handling a return, running end-of-day reconciliation, generating a state compliance report. A POS that demos well but fumbles daily operations will cost you hours every week.</p>

            <h2>Pricing structures to watch for</h2>
            <p>Cannabis <a href="/categories/pos-software/">POS systems</a> charge $200-2,000/month depending on features, terminal count, and support level. Payment processing adds 3-5% per transaction through their integrated processors. Watch for: long-term contracts (some lock you in for 2-3 years), hardware rental fees, per-terminal charges, and premium pricing for compliance reporting features that should be standard.</p>
            <p>Get total cost of ownership numbers, not just the monthly subscription. Include hardware, payment processing fees, training costs, and any API access charges for connecting to your accounting or analytics tools.</p>

            <h2>Inventory management capabilities</h2>
            <p>Your POS should handle: real-time inventory tracking synced with the state system, automated low-stock alerts, batch/lot tracking for recall capability, waste logging, and multi-location inventory transfers (if applicable). For dispensaries with both medical and recreational programs, the system must track and report these separately.</p>
            <p>Ask about inventory audit tools. How easy is it to run a physical count and reconcile against the system? What does the discrepancy resolution workflow look like? Good inventory management prevents the most common compliance violations.</p>

            <h2>Reporting and analytics</h2>
            <p>Beyond compliance reporting, your POS should provide: daily sales summaries, product performance by category, average transaction value, customer purchase patterns, employee performance metrics, and tax reporting. These analytics drive purchasing decisions, staffing optimization, and marketing strategy.</p>
            <p>Some platforms charge extra for analytics dashboards that should be included. Don't pay a premium for basic reporting. If you need advanced analytics (customer segmentation, predictive inventory), evaluate whether the POS platform or a separate analytics tool provides better value.</p>

            <h2>Migration and switching costs</h2>
            <p>Switching POS systems is painful. Data migration, staff retraining, new hardware setup, and state system re-integration typically take 2-4 weeks and cost $5,000-15,000 in direct costs plus lost productivity. Choose carefully the first time to avoid this pain. If your current system is failing, plan the migration during your slowest sales period.</p>
        """,
        "faqs": [
            {"question": "Which cannabis POS system is best?", "answer": "There's no single best system. Dutchie has the largest market share and broadest state coverage. Treez is preferred by multi-location operators. Flowhub excels at usability for single-location dispensaries. The best choice depends on your state, operation size, and specific workflow needs. Demo multiple platforms before deciding."},
            {"question": "How long does it take to set up a cannabis POS?", "answer": "Initial setup takes 1-4 weeks including hardware installation, state tracking system integration, menu setup, and staff training. Complex multi-location deployments can take 4-8 weeks. Factor this timeline into your store opening plan and schedule training before your soft launch."},
            {"question": "Can I use a regular POS system for a dispensary?", "answer": "No. Standard retail POS systems (Square, Clover, Shopify) don't integrate with state seed-to-sale tracking systems and can't handle cannabis-specific compliance requirements like THC limits, medical vs recreational tracking, and mandatory purchase logging. Using a non-compliant system is a licensing violation."},
        ],
    },
]


# =============================================================================
# BUILD HOMEPAGE
# =============================================================================

def build_homepage():
    """Generate index.html."""
    # Category cards
    category_cards = ""
    for cat in CATEGORIES:
        category_cards += generate_category_card(cat)

    # State cards
    state_cards = ""
    for state in sorted(STATES, key=lambda s: s["name"]):
        count = len(LISTINGS_BY_STATE.get(state["abbrev"], []))
        state_cards += generate_state_card(state, count)

    # How it works
    steps = [
        ("Step 01", "Search by category or state",
         "Pick from 18 service categories across 36 legal states. Find testing labs in California or compliance consultants in Colorado."),
        ("Step 02", "Compare providers",
         "See license status, services offered, and location. Every listing is verified against state licensing databases."),
        ("Step 03", "Connect directly",
         "Contact providers through their listed phone, email, or website. No middleman, no paywall, no gated leads."),
    ]

    steps_html = ""
    for num, title, desc in steps:
        steps_html += f'''
            <div class="step-card">
                <span class="step-card__number">{num}</span>
                <h3 class="step-card__title">{title}</h3>
                <p class="step-card__text">{desc}</p>
            </div>'''

    # Homepage FAQ
    homepage_faqs = [
        {"question": "What is Cannabisers?", "answer": "Cannabisers is a free B2B directory of ancillary service providers for the cannabis industry. We help cannabis operators find testing labs, attorneys, compliance consultants, packaging companies, and 14 other service categories across every legal US state."},
        {"question": "How do you verify listings?", "answer": "We cross-reference every listing against state cannabis licensing databases, business registrations, and industry association memberships. License status and business information are updated regularly."},
        {"question": "Is Cannabisers free to use?", "answer": "Yes. Searching and contacting providers is completely free for cannabis operators. Service providers can claim their listing for free to update their information. Featured placement and enhanced profiles are available through paid plans."},
        {"question": "How do I get my business listed?", "answer": "If your business serves the cannabis industry, you may already be in our directory. Search for your business name. If it's listed, click 'Claim This Listing' to verify ownership and update your profile. If it's not listed, use the contact form to submit your business."},
        {"question": "What states does Cannabisers cover?", "answer": "We cover every US state with a legal cannabis program, both medical and recreational. That's currently 36 states. Each state page includes local regulatory information and links to relevant licensing authorities."},
    ]

    faq_html, faq_schema = generate_faq_html(homepage_faqs)

    # Schemas
    org_schema = {
        "@type": "Organization",
        "@id": f"{BASE_URL}/#organization",
        "name": SITE_NAME,
        "url": BASE_URL,
        "description": "The cannabis industry directory. Find testing labs, attorneys, compliance consultants, and 15 other ancillary service categories across 36 legal US states.",
    }

    website_schema = {
        "@type": "WebSite",
        "@id": f"{BASE_URL}/#website",
        "name": SITE_NAME,
        "url": BASE_URL,
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{BASE_URL}/search?q={{search_term_string}}",
            "query-input": "required name=search_term_string",
        },
    }

    howto_schema = {
        "@type": "HowTo",
        "name": "How to Find Cannabis Service Providers on Cannabisers",
        "step": [
            {"@type": "HowToStep", "position": i+1, "name": t, "text": d}
            for i, (_, t, d) in enumerate(steps)
        ],
    }

    schemas = [org_schema, website_schema, howto_schema]
    if faq_schema:
        schemas.append(faq_schema)

    extra_schema = generate_graph_schema(schemas)

    body = f'''
        <section class="hero">
            <div class="container">
                <h1 class="hero__title">The testing labs, attorneys, and consultants cannabis operators use</h1>
                <p class="hero__subtitle">18 ancillary services cannabis operators need, organized by state.</p>
                <div class="hero__stats">
                    <div class="hero__stat">
                        <span class="hero__stat-value">18</span>
                        <span class="hero__stat-label">Service categories</span>
                    </div>
                    <div class="hero__stat">
                        <span class="hero__stat-value">36</span>
                        <span class="hero__stat-label">Legal states</span>
                    </div>
                    <div class="hero__stat">
                        <span class="hero__stat-value">100%</span>
                        <span class="hero__stat-label">Free to search</span>
                    </div>
                </div>
                <div class="hero__actions">
                    <a href="/categories/" class="btn btn--primary btn--lg">Browse Categories</a>
                    <a href="/states/" class="btn btn--secondary btn--lg">Browse by State</a>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <h2 class="section__title">Service Categories</h2>
                <p class="section__subtitle">Every ancillary service a cannabis business needs, from seed to sale.</p>
                <div class="category-grid">
                    {category_cards}
                </div>
            </div>
        </section>

        <section class="section" style="background: var(--color-bg-deep)">
            <div class="container">
                <h2 class="section__title">How It Works</h2>
                <div class="steps-grid">
                    {steps_html}
                </div>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <h2 class="section__title">Browse by State</h2>
                <p class="section__subtitle">Every state with a legal cannabis program. Regulatory info, local providers, and license requirements.</p>
                <div class="state-grid">
                    {state_cards}
                </div>
            </div>
        </section>

        {generate_newsletter_signup()}

        {generate_cta_section(
            title="Own a cannabis service business?",
            text="Claim your free listing to get found by cannabis operators searching for your services.",
            button_text="Get Listed",
            button_href="/contact/",
        )}

        {faq_html}
    '''

    html = get_page_wrapper(
        title="Cannabis Service Directory — Testing Labs, Attorneys & More",
        description="Find cannabis testing labs, attorneys, compliance consultants, and 15 other ancillary service categories across 36 legal US states. Free B2B directory.",
        canonical_path="/",
        body_content=body,
        extra_schema=extra_schema,
    )

    write_page("index.html", html)
    ALL_PAGES.append(("/", 1.0, "daily"))


# =============================================================================
# BUILD CATEGORY PAGES
# =============================================================================

def build_category_index():
    """Generate /categories/index.html."""
    cards = ""
    for cat in CATEGORIES:
        cards += generate_category_card(cat)

    body = f'''
        <section class="hero">
            <div class="container">
                <h1 class="hero__title">Cannabis Service Categories</h1>
                <p class="hero__subtitle">18 categories of ancillary services for cannabis operators. Testing, compliance, legal, packaging, security, and more.</p>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <div class="category-grid">
                    {cards}
                </div>
            </div>
        </section>
    '''

    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "Categories", "url": f"{BASE_URL}/categories/"},
    ]
    bc_schema = get_breadcrumb_schema(breadcrumbs)
    bc_html = get_breadcrumb_html(breadcrumbs)

    html = get_page_wrapper(
        title="Cannabis Service Categories",
        description="Browse 18 categories of cannabis ancillary services. Testing labs, attorneys, compliance consultants, packaging, insurance, and more.",
        canonical_path="/categories/",
        body_content=f'<div class="container">{bc_html}</div>{body}',
        active_page="/categories/",
        extra_schema=bc_schema,
    )

    write_page("categories/index.html", html)
    ALL_PAGES.append(("/categories/", 0.8, "weekly"))


def build_category_page(cat):
    """Generate /categories/{slug}/index.html for a single category."""
    slug = cat["slug"]
    name = cat["name"]
    description = cat.get("description", "")
    hero_title = cat.get("hero_title", f"{name} for Cannabis Businesses")
    hero_subtitle = cat.get("hero_subtitle", description)
    faqs = cat.get("faqs", [])

    # Listings in this category
    cat_listings = LISTINGS_BY_CATEGORY.get(slug, [])

    # State breakdown
    states_with_listings = defaultdict(int)
    for listing in cat_listings:
        st = listing.get("state", "")
        if st in STATES_BY_ABBREV:
            states_with_listings[st] += 1

    # State links
    state_links_html = ""
    for state in sorted(STATES, key=lambda s: s["name"]):
        abbrev = state["abbrev"]
        st_slug = state["slug"]
        count = states_with_listings.get(abbrev, 0)
        count_text = f" ({count})" if count > 0 else ""
        state_links_html += f'<a href="/states/{st_slug}/{slug}/" class="state-card">'
        state_links_html += f'<div class="state-card__header"><span class="state-card__abbrev">{abbrev}</span></div>'
        state_links_html += f'<h3 class="state-card__name">{state["name"]}{count_text}</h3></a>'

    # Listing cards
    listing_cards = ""
    for listing in cat_listings[:12]:
        listing_cards += generate_listing_card(listing, CATEGORIES_BY_SLUG)

    faq_html, faq_schema = generate_faq_html(faqs)

    # Related categories — same content_pillar first, then others
    same_pillar = [c for c in CATEGORIES if c["slug"] != slug and c.get("content_pillar") == cat.get("content_pillar")]
    diff_pillar = [c for c in CATEGORIES if c["slug"] != slug and c.get("content_pillar") != cat.get("content_pillar")]
    related = (same_pillar + diff_pillar)[:5]
    related_links = [{"href": f'/categories/{c["slug"]}/', "label": c["name"]} for c in related]

    # Schemas
    article_schema = generate_article_schema(hero_title, description, f"/categories/{slug}/")
    schemas = [article_schema]
    if faq_schema:
        schemas.append(faq_schema)

    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "Categories", "url": f"{BASE_URL}/categories/"},
        {"name": name, "url": f"{BASE_URL}/categories/{slug}/"},
    ]
    bc_schema_data = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": b["name"], "item": b["url"]}
            for i, b in enumerate(breadcrumbs)
        ]
    }
    schemas.append(bc_schema_data)
    extra_schema = generate_graph_schema(schemas)
    bc_html = get_breadcrumb_html(breadcrumbs)

    listings_section = ""
    if listing_cards:
        listings_section = f'''
        <section class="section">
            <div class="container">
                <h2 class="section__title">Featured {name} Providers</h2>
                <div class="listing-grid">
                    {listing_cards}
                </div>
            </div>
        </section>'''

    body = f'''
        <section class="hero">
            <div class="container">
                <h1 class="hero__title">{hero_title}</h1>
                <p class="hero__subtitle">{hero_subtitle}</p>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <h2 class="section__title">{name} by State</h2>
                <div class="state-grid">
                    {state_links_html}
                </div>
            </div>
        </section>

        {listings_section}

        {faq_html}

        {generate_related_links(related_links, heading="Related Categories")}

        {generate_newsletter_signup(category=name)}
    '''

    html = get_page_wrapper(
        title=hero_title,
        description=description[:158],
        canonical_path=f"/categories/{slug}/",
        body_content=f'<div class="container">{bc_html}</div>{body}',
        active_page="/categories/",
        extra_schema=extra_schema,
        og_type="article",
    )

    write_page(f"categories/{slug}/index.html", html)
    ALL_PAGES.append((f"/categories/{slug}/", 0.8, "weekly"))


# =============================================================================
# BUILD STATE PAGES
# =============================================================================

def build_state_index():
    """Generate /states/index.html."""
    cards = ""
    for state in sorted(STATES, key=lambda s: s["name"]):
        count = len(LISTINGS_BY_STATE.get(state["abbrev"], []))
        cards += generate_state_card(state, count)

    body = f'''
        <section class="hero">
            <div class="container">
                <h1 class="hero__title">Cannabis Services by State</h1>
                <p class="hero__subtitle">Every state with a legal cannabis program. Local providers, regulatory info, and license requirements.</p>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <div class="state-grid">
                    {cards}
                </div>
            </div>
        </section>
    '''

    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "States", "url": f"{BASE_URL}/states/"},
    ]
    bc_schema = get_breadcrumb_schema(breadcrumbs)
    bc_html = get_breadcrumb_html(breadcrumbs)

    html = get_page_wrapper(
        title="Cannabis Services by State",
        description="Browse cannabis ancillary services across 36 legal US states. Find local testing labs, attorneys, compliance consultants, and more.",
        canonical_path="/states/",
        body_content=f'<div class="container">{bc_html}</div>{body}',
        active_page="/states/",
        extra_schema=bc_schema,
    )

    write_page("states/index.html", html)
    ALL_PAGES.append(("/states/", 0.8, "weekly"))


def build_state_page(state):
    """Generate /states/{slug}/index.html for a single state."""
    slug = state["slug"]
    name = state["name"]
    abbrev = state["abbrev"]
    legal_status = state.get("legal_status", "")
    regulatory_body = state.get("regulatory_body", "")
    regulatory_notes = state.get("regulatory_notes", "")
    license_url = state.get("license_url", "")
    faqs = state.get("faqs", [])

    state_listings = LISTINGS_BY_STATE.get(abbrev, [])

    # Category breakdown
    cats_with_listings = defaultdict(int)
    for listing in state_listings:
        cats_with_listings[listing.get("category", "")] += 1

    # Category links for this state
    cat_links_html = ""
    for cat in CATEGORIES:
        cat_slug = cat["slug"]
        count = cats_with_listings.get(cat_slug, 0)
        count_text = f" ({count})" if count > 0 else ""
        color = cat.get("color", "#3AA882")
        cat_links_html += f'''<a href="/states/{slug}/{cat_slug}/" class="category-card" style="--card-accent: {color}">
            <h3 class="category-card__name">{cat["name"]}{count_text}</h3>
        </a>'''

    # Regulatory info
    reg_html = ""
    if regulatory_body or regulatory_notes:
        reg_items = ""
        if legal_status:
            status_label = legal_status.title()
            reg_items += f'<p><strong>Legal status:</strong> {status_label}</p>'
        if regulatory_body:
            reg_items += f'<p><strong>Regulatory body:</strong> {regulatory_body}</p>'
        if license_url:
            reg_items += f'<p><strong>Licensing:</strong> <a href="{license_url}" target="_blank" rel="noopener noreferrer">Apply for a license</a></p>'
        if regulatory_notes:
            reg_items += f'<p>{regulatory_notes}</p>'

        reg_html = f'''
        <section class="section" style="background: var(--color-bg-deep)">
            <div class="container">
                <h2 class="section__title">Regulatory Overview</h2>
                <div class="content-page" style="max-width: 100%; padding: 0;">
                    {reg_items}
                </div>
            </div>
        </section>'''

    faq_html, faq_schema = generate_faq_html(faqs)

    # Related states
    state_idx = next((i for i, s in enumerate(STATES) if s["slug"] == slug), 0)
    neighbors = []
    for offset in [-2, -1, 1, 2]:
        idx = (state_idx + offset) % len(STATES)
        neighbors.append(STATES[idx])
    related_links = [{"href": f'/states/{s["slug"]}/', "label": s["name"]} for s in neighbors]

    # Schemas
    state_schema_desc = f"Find cannabis ancillary services in {name}. {len(state_listings)} providers across 18 categories." if state_listings else f"Find cannabis ancillary services in {name}. Testing labs, attorneys, compliance consultants, and more."
    article_schema = generate_article_schema(
        f"Cannabis Services in {name}",
        state_schema_desc,
        f"/states/{slug}/",
    )
    schemas = [article_schema]
    if faq_schema:
        schemas.append(faq_schema)

    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "States", "url": f"{BASE_URL}/states/"},
        {"name": name, "url": f"{BASE_URL}/states/{slug}/"},
    ]
    bc_schema_data = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": b["name"], "item": b["url"]}
            for i, b in enumerate(breadcrumbs)
        ]
    }
    schemas.append(bc_schema_data)
    extra_schema = generate_graph_schema(schemas)
    bc_html = get_breadcrumb_html(breadcrumbs)

    status_badge = generate_state_badge(legal_status.title(), legal_status)

    body = f'''
        <section class="hero">
            <div class="container">
                <h1 class="hero__title">Cannabis Services in {name}</h1>
                <p class="hero__subtitle">Find testing labs, attorneys, compliance consultants, and more for {name} cannabis operators. {status_badge}</p>
            </div>
        </section>

        {reg_html}

        <section class="section">
            <div class="container">
                <h2 class="section__title">Service Categories in {name}</h2>
                <div class="category-grid">
                    {cat_links_html}
                </div>
            </div>
        </section>

        {faq_html}

        {generate_related_links(related_links, heading="Nearby States")}

        {generate_newsletter_signup(state=name)}
    '''

    html = get_page_wrapper(
        title=f"Cannabis Services in {name}",
        description=f"Find cannabis service providers in {name}. Testing labs, attorneys, compliance, packaging, and more for {abbrev} operators.",
        canonical_path=f"/states/{slug}/",
        body_content=f'<div class="container">{bc_html}</div>{body}',
        active_page="/states/",
        extra_schema=extra_schema,
        og_type="article",
    )

    write_page(f"states/{slug}/index.html", html)
    ALL_PAGES.append((f"/states/{slug}/", 0.8, "weekly"))


# =============================================================================
# BUILD STATE+CATEGORY PAGES (THE MONEY PAGES)
# =============================================================================

def build_state_category_page(state, cat):
    """Generate /states/{state_slug}/{cat_slug}/index.html."""
    st_slug = state["slug"]
    st_name = state["name"]
    st_abbrev = state["abbrev"]
    cat_slug = cat["slug"]
    cat_name = cat["name"]

    listings = LISTINGS_BY_STATE_CATEGORY.get((st_abbrev, cat_slug), [])

    listing_cards = ""
    for listing in listings:
        listing_cards += generate_listing_card(listing, CATEGORIES_BY_SLUG)

    # Generate FAQs specific to this intersection
    # Singular form for FAQ phrasing (e.g. "testing lab" not "testing labs providers")
    cat_singular = cat_name.lower().rstrip("s") if cat_name.lower().endswith("s") and not cat_name.lower().endswith("ss") else cat_name.lower()
    count_phrase = f"We currently list {len(listings)} verified {cat_name.lower()} in {st_name}." if listings else f"We're actively building our {cat_name.lower()} directory in {st_name}."
    state_cat_faqs = [
        {"question": f"How do I find {cat_name.lower()} for cannabis businesses in {st_name}?",
         "answer": f"{count_phrase} Each listing is verified against state licensing databases and includes contact information and license status. New providers are added regularly."},
        {"question": f"What should I look for in a {cat_singular} in {st_name}?",
         "answer": f"Verify they hold a current {st_name} state license, check their experience with cannabis-specific requirements, and confirm they serve your license type. Always verify credentials directly with {st_name}'s regulatory body."},
        {"question": f"Are {cat_name.lower()} in {st_name} verified?",
         "answer": f"We verify listings against {st_name}'s state licensing databases. License status is shown on each listing. Always confirm current licensing directly with the provider and the state regulatory body before engaging their services."},
    ]

    faq_html, faq_schema = generate_faq_html(state_cat_faqs)

    # Related links
    related = []
    related.append({"href": f"/states/{st_slug}/", "label": f"All services in {st_name}"})
    related.append({"href": f"/categories/{cat_slug}/", "label": f"{cat_name} in all states"})
    # Same state, other categories
    for other_cat in CATEGORIES[:4]:
        if other_cat["slug"] != cat_slug:
            related.append({"href": f'/states/{st_slug}/{other_cat["slug"]}/', "label": f'{other_cat["name"]} in {st_name}'})

    # Schemas
    schema_desc = f"Find {cat_name.lower()} for cannabis businesses in {st_name}. {len(listings)} verified providers." if listings else f"Find {cat_name.lower()} for cannabis businesses in {st_name}. Browse verified providers with license status and contact info."
    article_schema = generate_article_schema(
        f"{cat_name} in {st_name}",
        schema_desc,
        f"/states/{st_slug}/{cat_slug}/",
    )
    schemas = [article_schema]
    if faq_schema:
        schemas.append(faq_schema)

    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "States", "url": f"{BASE_URL}/states/"},
        {"name": st_name, "url": f"{BASE_URL}/states/{st_slug}/"},
        {"name": cat_name, "url": f"{BASE_URL}/states/{st_slug}/{cat_slug}/"},
    ]
    bc_schema_data = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": b["name"], "item": b["url"]}
            for i, b in enumerate(breadcrumbs)
        ]
    }
    schemas.append(bc_schema_data)
    extra_schema = generate_graph_schema(schemas)
    bc_html = get_breadcrumb_html(breadcrumbs)

    empty_state = ""
    if not listings:
        empty_state = f'''
        <section class="section">
            <div class="container">
                <div class="empty-state">
                    <h2 class="empty-state__title">No listings yet</h2>
                    <p class="empty-state__text">We're building our {cat_name.lower()} directory in {st_name}. Know a provider that should be listed?</p>
                    <a href="/contact/" class="btn btn--primary">Submit a Business</a>
                </div>
            </div>
        </section>'''

    listings_section = ""
    if listings:
        listings_section = f'''
        <section class="section">
            <div class="container">
                <div class="listing-grid">
                    {listing_cards}
                </div>
            </div>
        </section>'''

    body = f'''
        <section class="hero">
            <div class="container">
                <h1 class="hero__title">{cat_name} in {st_name}</h1>
                <p class="hero__subtitle">Find verified {cat_name.lower()} for cannabis businesses in {st_name}.</p>
            </div>
        </section>

        {listings_section}
        {empty_state}

        {faq_html}

        {generate_related_links(related, heading="Related Pages")}

        {generate_claim_cta()}
    '''

    html = get_page_wrapper(
        title=f"{cat_name} in {st_name}",
        description=f"Find {cat_name.lower()} for cannabis businesses in {st_name}. Browse verified providers with contact info and license status.",
        canonical_path=f"/states/{st_slug}/{cat_slug}/",
        body_content=f'<div class="container">{bc_html}</div>{body}',
        active_page="/states/",
        extra_schema=extra_schema,
        og_type="article",
    )

    write_page(f"states/{st_slug}/{cat_slug}/index.html", html)
    ALL_PAGES.append((f"/states/{st_slug}/{cat_slug}/", 0.9, "weekly"))


# =============================================================================
# BUILD CITY+CATEGORY PAGES
# =============================================================================

def build_city_category_pages():
    """Generate /cities/{city-state}/{category}/index.html for city+category combos with 2+ listings."""
    for (city_key, cat_slug), listings in LISTINGS_BY_CITY_STATE_CATEGORY.items():
        if len(listings) < 2:
            continue

        city = listings[0].get("city", "")
        state_abbrev = listings[0].get("state", "")
        state = STATES_BY_ABBREV.get(state_abbrev, {})
        st_name = state.get("name", state_abbrev)
        st_slug = state.get("slug", state_abbrev.lower())
        cat = CATEGORIES_BY_SLUG.get(cat_slug, {})
        cat_name = cat.get("name", cat_slug.replace("-", " ").title())

        listing_cards = ""
        for listing in listings:
            listing_cards += generate_listing_card(listing, CATEGORIES_BY_SLUG)

        breadcrumbs = [
            {"name": "Home", "url": BASE_URL},
            {"name": st_name, "url": f"{BASE_URL}/states/{st_slug}/"},
            {"name": cat_name, "url": f"{BASE_URL}/states/{st_slug}/{cat_slug}/"},
            {"name": city, "url": f"{BASE_URL}/cities/{city_key}/{cat_slug}/"},
        ]
        bc_schema_data = {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i+1, "name": b["name"], "item": b["url"]}
                for i, b in enumerate(breadcrumbs)
            ]
        }
        extra_schema = generate_graph_schema([bc_schema_data])
        bc_html = get_breadcrumb_html(breadcrumbs)

        body = f'''
            <section class="hero">
                <div class="container">
                    <h1 class="hero__title">{cat_name} in {city}, {st_name}</h1>
                    <p class="hero__subtitle">{len(listings)} verified {cat_name.lower()} providers in {city}.</p>
                </div>
            </section>

            <section class="section">
                <div class="container">
                    <div class="listing-grid">
                        {listing_cards}
                    </div>
                </div>
            </section>

            {generate_claim_cta()}
        '''

        html = get_page_wrapper(
            title=f"{cat_name} in {city}, {state_abbrev}",
            description=f"Find {cat_name.lower()} in {city}, {st_name}. {len(listings)} verified cannabis service providers.",
            canonical_path=f"/cities/{city_key}/{cat_slug}/",
            body_content=f'<div class="container">{bc_html}</div>{body}',
            active_page="/states/",
            extra_schema=extra_schema,
        )

        write_page(f"cities/{city_key}/{cat_slug}/index.html", html)
        ALL_PAGES.append((f"/cities/{city_key}/{cat_slug}/", 0.7, "weekly"))


# =============================================================================
# BUILD LISTING PAGES
# =============================================================================

def build_listing_page(listing):
    """Generate /listing/{slug}/index.html for a single listing."""
    slug = listing["slug"]
    name = listing["name"]
    city = listing.get("city", "")
    state_abbrev = listing.get("state", "")
    state = STATES_BY_ABBREV.get(state_abbrev, {})
    st_name = state.get("name", state_abbrev)
    st_slug = state.get("slug", state_abbrev.lower())
    cat_slug = listing.get("category", "")
    cat = CATEGORIES_BY_SLUG.get(cat_slug, {})
    cat_name = cat.get("name", cat_slug.replace("-", " ").title())
    description = listing.get("description", "")
    services = listing.get("services", [])
    phone = listing.get("phone", "")
    email = listing.get("email", "")
    website = listing.get("website", "")
    address = listing.get("address", "")
    license_number = listing.get("license_number", "")
    license_status = listing.get("license_status", "")

    # Contact card
    contact_items = ""
    if address:
        contact_items += f'<div class="listing-detail__contact-item"><span class="listing-detail__contact-label">Address</span><span>{address}, {city}, {state_abbrev}</span></div>'
    if phone:
        contact_items += f'<div class="listing-detail__contact-item"><span class="listing-detail__contact-label">Phone</span><a href="tel:{phone}">{phone}</a></div>'
    if email:
        contact_items += f'<div class="listing-detail__contact-item"><span class="listing-detail__contact-label">Email</span><a href="mailto:{email}">{email}</a></div>'
    if website:
        display_url = website.replace("https://", "").replace("http://", "").rstrip("/")
        contact_items += f'<div class="listing-detail__contact-item"><span class="listing-detail__contact-label">Website</span><a href="{website}" target="_blank" rel="noopener noreferrer">{display_url}</a></div>'
    if license_number:
        status_html = f' <span class="license-status license-status--{license_status}">{license_status.title()}</span>' if license_status else ""
        contact_items += f'<div class="listing-detail__contact-item"><span class="listing-detail__contact-label">License</span><span>{license_number}{status_html}</span></div>'

    # Services list
    services_html = ""
    if services:
        items = ""
        for svc in services:
            items += f"<li>{svc}</li>"
        services_html = f'''
            <div class="listing-detail__section">
                <h2 class="listing-detail__section-title">Services</h2>
                <ul class="listing-detail__services">{items}</ul>
            </div>'''

    # Category/state badges
    badges = generate_category_badge(cat_name, cat.get("color", "#3AA882"))
    if state_abbrev:
        badges += " " + generate_state_badge(state_abbrev)

    # Related listings
    related_listings = [l for l in LISTINGS_BY_STATE_CATEGORY.get((state_abbrev, cat_slug), []) if l["slug"] != slug][:3]
    related_cards = ""
    for rl in related_listings:
        related_cards += generate_listing_card(rl, CATEGORIES_BY_SLUG)

    related_section = ""
    if related_cards:
        related_section = f'''
        <section class="section">
            <div class="container">
                <h2 class="section__title">Similar Providers in {st_name}</h2>
                <div class="listing-grid">
                    {related_cards}
                </div>
            </div>
        </section>'''

    # Related links
    related_links = [
        {"href": f"/states/{st_slug}/{cat_slug}/", "label": f"{cat_name} in {st_name}"},
        {"href": f"/states/{st_slug}/", "label": f"All services in {st_name}"},
        {"href": f"/categories/{cat_slug}/", "label": f"{cat_name} nationwide"},
    ]

    # Schemas
    lb_schema = generate_local_business_schema(listing)
    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": st_name, "url": f"{BASE_URL}/states/{st_slug}/"},
        {"name": cat_name, "url": f"{BASE_URL}/states/{st_slug}/{cat_slug}/"},
        {"name": name, "url": f"{BASE_URL}/listing/{slug}/"},
    ]
    bc_schema_data = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": b["name"], "item": b["url"]}
            for i, b in enumerate(breadcrumbs)
        ]
    }
    extra_schema = generate_graph_schema([lb_schema, bc_schema_data])
    bc_html = get_breadcrumb_html(breadcrumbs)

    location = f"{city}, {state_abbrev}" if city else state_abbrev

    body = f'''
        <section class="listing-detail">
            <div class="container">
                <div class="listing-detail__header">
                    <h1 class="listing-detail__name">{name}</h1>
                    <div class="listing-detail__meta">
                        <span class="listing-detail__meta-item">{location}</span>
                        {badges}
                    </div>
                </div>

                <div class="listing-detail__body">
                    <div class="listing-detail__main">
                        <div class="listing-detail__section">
                            <h2 class="listing-detail__section-title">About</h2>
                            <p class="listing-detail__description">{description or "No description available yet. Claim this listing to add your business description."}</p>
                        </div>
                        {services_html}
                    </div>

                    <div class="listing-detail__sidebar">
                        <div class="listing-detail__contact-card">
                            <h3 class="listing-detail__section-title">Contact</h3>
                            {contact_items or '<p class="listing-detail__description">No contact information available. Claim this listing to add your details.</p>'}
                        </div>
                    </div>
                </div>
            </div>
        </section>

        {related_section}

        {generate_claim_cta(listing_name=name)}

        {generate_related_links(related_links)}

        {generate_newsletter_signup(category=cat_name, state=st_name)}
    '''

    meta_desc = f"{name} in {location}. {cat_name} for cannabis businesses."
    if description:
        meta_desc = description[:155]

    html = get_page_wrapper(
        title=f"{name} - {cat_name} in {location}",
        description=meta_desc,
        canonical_path=f"/listing/{slug}/",
        body_content=f'<div class="container">{bc_html}</div>{body}',
        extra_schema=extra_schema,
    )

    write_page(f"listing/{slug}/index.html", html)
    ALL_PAGES.append((f"/listing/{slug}/", 0.6, "monthly"))


# =============================================================================
# BUILD GUIDE PAGES
# =============================================================================

def build_guides_index():
    """Generate /guides/index.html."""
    guide_cards = ""
    for guide in GUIDES:
        cat = CATEGORIES_BY_SLUG.get(guide.get("category", ""), {})
        cat_name = cat.get("name", "")
        cat_color = cat.get("color", "#3AA882")
        badge = generate_category_badge(cat_name, cat_color) if cat_name else ""

        guide_cards += f'''<a href="/guides/{guide['slug']}/" class="listing-card">
            <h3 class="listing-card__name">{guide['title']}</h3>
            <p class="listing-card__desc">{guide['description']}</p>
            <div class="listing-card__footer">{badge}</div>
        </a>'''

    body = f'''
        <section class="hero">
            <div class="container">
                <h1 class="hero__title">Cannabis Industry Guides</h1>
                <p class="hero__subtitle">Practical guides for cannabis operators. How to choose vendors, reduce costs, and stay compliant.</p>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <div class="listing-grid">
                    {guide_cards}
                </div>
            </div>
        </section>
    '''

    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "Guides", "url": f"{BASE_URL}/guides/"},
    ]
    bc_schema = get_breadcrumb_schema(breadcrumbs)
    bc_html = get_breadcrumb_html(breadcrumbs)

    html = get_page_wrapper(
        title="Cannabis Industry Guides",
        description="Practical guides for cannabis operators on choosing service providers, reducing costs, and navigating compliance requirements.",
        canonical_path="/guides/",
        body_content=f'<div class="container">{bc_html}</div>{body}',
        active_page="/guides/",
        extra_schema=bc_schema,
    )

    write_page("guides/index.html", html)
    ALL_PAGES.append(("/guides/", 0.7, "weekly"))


def build_guide_page(guide):
    """Generate /guides/{slug}/index.html."""
    slug = guide["slug"]
    title = guide["title"]
    description = guide["description"]
    content = guide.get("content", "")
    faqs = guide.get("faqs", [])
    cat_slug = guide.get("category", "")

    faq_html, faq_schema = generate_faq_html(faqs)

    # Related links
    related = []
    if cat_slug:
        cat = CATEGORIES_BY_SLUG.get(cat_slug, {})
        if cat:
            related.append({"href": f'/categories/{cat_slug}/', "label": f'{cat.get("name", "")} Directory'})
    for other_guide in GUIDES:
        if other_guide["slug"] != slug:
            related.append({"href": f'/guides/{other_guide["slug"]}/', "label": other_guide["title"]})

    # Schemas
    article_schema = generate_article_schema(title, description, f"/guides/{slug}/")
    schemas = [article_schema]
    if faq_schema:
        schemas.append(faq_schema)

    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "Guides", "url": f"{BASE_URL}/guides/"},
        {"name": title, "url": f"{BASE_URL}/guides/{slug}/"},
    ]
    bc_schema_data = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": b["name"], "item": b["url"]}
            for i, b in enumerate(breadcrumbs)
        ]
    }
    schemas.append(bc_schema_data)
    extra_schema = generate_graph_schema(schemas)
    bc_html = get_breadcrumb_html(breadcrumbs)

    body = f'''
        <div class="content-page">
            <h1>{title}</h1>
            {content}
        </div>

        {faq_html}

        {generate_related_links(related)}

        {generate_newsletter_signup()}
    '''

    html = get_page_wrapper(
        title=title,
        description=description[:158],
        canonical_path=f"/guides/{slug}/",
        body_content=f'<div class="container">{bc_html}</div>{body}',
        active_page="/guides/",
        extra_schema=extra_schema,
        og_type="article",
    )

    write_page(f"guides/{slug}/index.html", html)
    ALL_PAGES.append((f"/guides/{slug}/", 0.7, "monthly"))


# =============================================================================
# BUILD STATIC PAGES
# =============================================================================

def build_about():
    """Generate /about/index.html."""
    body = '''
        <div class="content-page">
            <h1>About Cannabisers</h1>
            <p>Cannabisers is the B2B directory for cannabis industry ancillary services. We help cannabis operators find the service providers they need to run compliant, profitable businesses.</p>

            <h2>The problem we solve</h2>
            <p>Cannabis operators spend hours searching Google for basic services: testing labs, attorneys, compliance consultants, packaging companies. The results are a mess of outdated listings, pay-to-play directories, and companies that don't actually serve cannabis. You end up calling five places to find one that's licensed and available in your state.</p>

            <h2>How we're different</h2>
            <p>We verify every listing against state licensing databases. We organize by service category and state so you find what you need in your market. We don't gate contact information behind a paywall or force you to "request a quote" through our platform. You get direct contact details and reach out on your own terms.</p>

            <h2>What we cover</h2>
            <p>18 categories of ancillary services across every legal US state. Testing labs, compliance consultants, cannabis attorneys, packaging companies, security services, HVAC contractors, insurance providers, accountants, real estate brokers, POS systems, marketing agencies, transport companies, staffing firms, banks, waste management, construction firms, and general consultants.</p>

            <h2>For service providers</h2>
            <p>If your business serves the cannabis industry, you may already be in our directory. Search for your business and claim your listing to update your information, add your logo, and get in front of cannabis operators searching for your services. Featured placement is available for businesses that want more visibility.</p>
        </div>
    '''

    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "About", "url": f"{BASE_URL}/about/"},
    ]
    bc_html = get_breadcrumb_html(breadcrumbs)
    bc_schema = get_breadcrumb_schema(breadcrumbs)

    html = get_page_wrapper(
        title="About Cannabisers",
        description="Cannabisers is the B2B directory for cannabis ancillary services. We help operators find verified testing labs, attorneys, and 16 other service categories.",
        canonical_path="/about/",
        body_content=f'<div class="container">{bc_html}</div>{body}',
        active_page="/about/",
        extra_schema=bc_schema,
    )

    write_page("about/index.html", html)
    ALL_PAGES.append(("/about/", 0.5, "monthly"))


def build_contact():
    """Generate /contact/index.html."""
    body = f'''
        <div class="content-page">
            <h1>Contact Us</h1>
            <p>Want to get listed, claim a listing, or report an issue? Use the form below.</p>
        </div>

        {generate_cta_section(
            title="Get in touch",
            text="Whether you want to submit your business, claim an existing listing, or report incorrect information, we'll respond within 24 hours.",
            button_text="Send Message",
            include_form=True,
            formspree_id="",
        )}
    '''

    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "Contact", "url": f"{BASE_URL}/contact/"},
    ]
    bc_html = get_breadcrumb_html(breadcrumbs)
    bc_schema = get_breadcrumb_schema(breadcrumbs)

    html = get_page_wrapper(
        title="Contact Cannabisers",
        description="Contact Cannabisers to get listed, claim your listing, or report an issue. We respond within 24 hours.",
        canonical_path="/contact/",
        body_content=f'<div class="container">{bc_html}</div>{body}',
        extra_schema=bc_schema,
    )

    write_page("contact/index.html", html)
    ALL_PAGES.append(("/contact/", 0.5, "monthly"))


def build_newsletter():
    """Generate /newsletter/index.html."""
    body = f'''
        <div class="content-page">
            <h1>Cannabis Industry Newsletter</h1>
            <p>Weekly updates on new listings, regulatory changes, and industry news. No spam, no fluff, just practical information for cannabis operators.</p>
        </div>

        {generate_newsletter_signup()}
    '''

    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "Newsletter", "url": f"{BASE_URL}/newsletter/"},
    ]
    bc_html = get_breadcrumb_html(breadcrumbs)
    bc_schema = get_breadcrumb_schema(breadcrumbs)

    html = get_page_wrapper(
        title="Cannabis Industry Newsletter",
        description="Weekly cannabis industry updates. New vendor listings, regulatory changes, and practical insights for cannabis operators.",
        canonical_path="/newsletter/",
        body_content=f'<div class="container">{bc_html}</div>{body}',
        extra_schema=bc_schema,
    )

    write_page("newsletter/index.html", html)
    ALL_PAGES.append(("/newsletter/", 0.5, "monthly"))


def build_privacy():
    """Generate /privacy/index.html."""
    body = '''
        <div class="content-page">
            <h1>Privacy Policy</h1>
            <p><em>Last updated: February 27, 2026</em></p>

            <h2>Information we collect</h2>
            <p>When you use Cannabisers, we may collect information you provide directly (name, email, company via forms) and usage data (pages visited, time on site). We use cookies for analytics through Google Analytics 4.</p>

            <h2>How we use your information</h2>
            <p>We use collected information to: operate and improve the directory, respond to your inquiries, send newsletter updates you've subscribed to, and analyze site usage to improve the user experience.</p>

            <h2>Information sharing</h2>
            <p>We don't sell your personal information. Form submissions (claim requests, contact inquiries) are processed through Formspree. Analytics data is processed through Google Analytics. We may share information when required by law.</p>

            <h2>Cookies</h2>
            <p>We use Google Analytics cookies to understand how visitors use our site. You can disable cookies in your browser settings. The site will function normally without them.</p>

            <h2>Your rights</h2>
            <p>You can request access to, correction of, or deletion of your personal data by contacting us. If you've subscribed to our newsletter, every email includes an unsubscribe link.</p>

            <h2>Contact</h2>
            <p>For privacy-related questions, contact us through our <a href="/contact/">contact page</a>.</p>
        </div>
    '''

    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "Privacy Policy", "url": f"{BASE_URL}/privacy/"},
    ]
    bc_html = get_breadcrumb_html(breadcrumbs)
    bc_schema = get_breadcrumb_schema(breadcrumbs)

    html = get_page_wrapper(
        title="Privacy Policy",
        description="Cannabisers privacy policy. How we collect, use, and protect your information.",
        canonical_path="/privacy/",
        body_content=f'<div class="container">{bc_html}</div>{body}',
        extra_schema=bc_schema,
    )

    write_page("privacy/index.html", html)
    ALL_PAGES.append(("/privacy/", 0.4, "yearly"))


def build_terms():
    """Generate /terms/index.html."""
    body = '''
        <div class="content-page">
            <h1>Terms of Service</h1>
            <p><em>Last updated: February 27, 2026</em></p>

            <h2>Acceptance of terms</h2>
            <p>By accessing Cannabisers, you agree to these terms. If you don't agree, don't use the site.</p>

            <h2>Directory information</h2>
            <p>Cannabisers provides directory information about cannabis ancillary service providers. While we verify listings against state licensing databases, we don't guarantee the accuracy, completeness, or timeliness of any listing. Always verify licensing and credentials directly with the provider and relevant state authorities before engaging their services.</p>

            <h2>No endorsement</h2>
            <p>Listing a business on Cannabisers doesn't constitute an endorsement. We don't evaluate the quality of services provided by listed businesses. Featured placement is a paid advertising service and doesn't indicate superior quality.</p>

            <h2>User submissions</h2>
            <p>By submitting information through our forms (listings, claims, contact), you grant us permission to use that information to operate the directory. You represent that information you submit is accurate.</p>

            <h2>Intellectual property</h2>
            <p>The Cannabisers name, logo, and original content are our property. Business listings contain factual information compiled from public sources and user submissions.</p>

            <h2>Limitation of liability</h2>
            <p>Cannabisers is provided "as is." We're not liable for any damages arising from your use of the directory or your interactions with listed businesses. Use this directory as a starting point for your own research and due diligence.</p>

            <h2>Changes to terms</h2>
            <p>We may update these terms at any time. Continued use after changes constitutes acceptance. Check this page periodically for updates.</p>
        </div>
    '''

    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "Terms of Service", "url": f"{BASE_URL}/terms/"},
    ]
    bc_html = get_breadcrumb_html(breadcrumbs)
    bc_schema = get_breadcrumb_schema(breadcrumbs)

    html = get_page_wrapper(
        title="Terms of Service",
        description="Cannabisers terms of service. Read our terms for using the cannabis industry directory.",
        canonical_path="/terms/",
        body_content=f'<div class="container">{bc_html}</div>{body}',
        extra_schema=bc_schema,
    )

    write_page("terms/index.html", html)
    ALL_PAGES.append(("/terms/", 0.4, "yearly"))


def build_404():
    """Generate 404.html."""
    body = '''
        <section class="error-page">
            <div class="error-page__code">404</div>
            <h1 class="error-page__title">Page not found</h1>
            <p class="error-page__text">The page you're looking for doesn't exist or has been moved.</p>
            <div>
                <a href="/" class="btn btn--primary">Back to Home</a>
                <a href="/categories/" class="btn btn--secondary">Browse Categories</a>
            </div>
        </section>
    '''

    html = get_page_wrapper(
        title="Page Not Found",
        description="The page you're looking for doesn't exist.",
        canonical_path="/404/",
        body_content=body,
        noindex=True,
    )

    write_page("404.html", html)


# =============================================================================
# SITEMAP & ROBOTS
# =============================================================================

def build_sitemap():
    """Generate sitemap.xml."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for path, priority, changefreq in ALL_PAGES:
        url = f"{BASE_URL}{path}"
        lines.append(f"  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{TODAY}</lastmod>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append(f"  </url>")

    lines.append("</urlset>")

    sitemap_path = os.path.join(PROJECT_ROOT, "sitemap.xml")
    with open(sitemap_path, "w") as f:
        f.write("\n".join(lines))
    print(f"  Generated: /sitemap.xml ({len(ALL_PAGES)} URLs)")


def build_robots_txt():
    """Generate robots.txt."""
    content = f"""User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: CCBot
Disallow: /

Sitemap: {BASE_URL}/sitemap.xml
"""

    robots_path = os.path.join(PROJECT_ROOT, "robots.txt")
    with open(robots_path, "w") as f:
        f.write(content)
    print("  Generated: /robots.txt")


def build_cname():
    """Generate CNAME file for GitHub Pages."""
    cname_path = os.path.join(PROJECT_ROOT, "CNAME")
    with open(cname_path, "w") as f:
        f.write("cannabisers.com")
    print("  Generated: /CNAME")


# =============================================================================
# MAIN BUILD
# =============================================================================

def main():
    """Run the full build."""
    print(f"\n{'='*60}")
    print(f"  Cannabisers Build — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Categories: {len(CATEGORIES)} | States: {len(STATES)} | Listings: {len(LISTINGS)}")
    print(f"{'='*60}\n")

    # 1. Homepage
    print("Building homepage...")
    build_homepage()

    # 2. Category pages
    print("\nBuilding category pages...")
    build_category_index()
    for cat in CATEGORIES:
        build_category_page(cat)

    # 3. State pages
    print("\nBuilding state pages...")
    build_state_index()
    for state in STATES:
        build_state_page(state)

    # 4. State+Category money pages (generate for ALL combinations)
    print("\nBuilding state+category pages...")
    for state in STATES:
        for cat in CATEGORIES:
            build_state_category_page(state, cat)

    # 5. City+Category pages (only where 2+ listings exist)
    print("\nBuilding city+category pages...")
    build_city_category_pages()

    # 6. Listing pages
    print("\nBuilding listing pages...")
    for listing in LISTINGS:
        build_listing_page(listing)

    # 7. Guide pages
    print("\nBuilding guide pages...")
    build_guides_index()
    for guide in GUIDES:
        build_guide_page(guide)

    # 8. Static pages
    print("\nBuilding static pages...")
    build_about()
    build_contact()
    build_newsletter()
    build_privacy()
    build_terms()
    build_404()

    # 9. Sitemap, robots, CNAME
    print("\nBuilding sitemap, robots.txt, CNAME...")
    build_sitemap()
    build_robots_txt()
    build_cname()

    # Summary
    print(f"\n{'='*60}")
    print(f"  Build complete. {len(ALL_PAGES)} pages generated.")
    print(f"  Preview: python3 -m http.server 8083")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
