# Cannabisers Build Handoff

## Current Status (Updated Feb 27, 2026)

### What's Built
- **720 pages generated**, zero errors, initial git commit (`ee854a7`)
- **Build system:** `python3 scripts/build.py` — generates all pages from JSON data
- **Page types:** 1 homepage + 19 category + 37 state + 648 state+category money pages + 9 guide pages + 5 static + 1 404 + sitemap + robots + CNAME
- **8 editorial guides** (1,200+ words each): Testing labs, Insurance, 280E tax, Compliance, Banking, Packaging, Hiring, Security, POS systems
- **Branding:** Dark theme (botanical green + warm amber), DM Sans 700 headlines, IBM Plex Mono badges
- **SEO:** Unique title/desc per page, JSON-LD @graph schemas (Organization, WebSite, Article, FAQPage, BreadcrumbList, LocalBusiness), sitemap.xml, robots.txt
- **OG social image:** 1200x630 PNG at `/assets/social/og-default.png`
- **Google Analytics:** Placeholder in templates.py, set `GA_MEASUREMENT_ID` when ready
- **seed_data.py:** Ready to populate listings via Outscraper (Google Places)

### Design Decisions Made
- **Headline:** "The testing labs, attorneys, and consultants cannabis operators use" (Harry Dry style)
- **Subtitle:** "18 ancillary services cannabis operators need, organized by state."
- **Font:** DM Sans 700 for all headlines (Instrument Serif rejected as too editorial for B2B ICP)
- **Category icons:** 18 inline SVG icons in `CATEGORY_ICONS` dict (templates.py)
- **Stats:** DM Sans 700 (not mono) for hero stat values
- **No personal name** in any generated/deployed files

### What Needs Doing Next
1. **Seed listings data** — Run `seed_data.py` to populate listings.json via Outscraper. Start with CA + CO as test, then expand. Can't publish a directory with 0 listings.
2. **Newsletter strategy** — Scoped (see below) but needs platform decision (Beehiiv vs Resend vs Substack) and Formspree IDs for capture forms.
3. **Create GitHub repo** — `gh repo create romelikethecity/cannabisers --private --source=.` then push
4. **GitHub Pages** — Enable after repo creation, point custom domain
5. **Formspree** — Create 3 form IDs (contact, newsletter, claim) and set in templates.py
6. **Google Analytics** — Create GA4 property, set `GA_MEASUREMENT_ID` in templates.py
7. **Visual/mobile review** — Full page check at localhost:8083, test 375px mobile

### Newsletter Strategy (Scoped)
- **Cadence:** Weekly
- **Content:** 1 regulatory update (the opener), 3-5 new/featured listings, 1 guide link
- **Format:** 500-800 words, specific subject lines ("3 new testing labs in CA + Colorado's new packaging rules")
- **Monetization:** Sponsored listing slots ($200-500/issue)
- **Platform:** TBD (Beehiiv, Resend, or Substack)
- **Source:** State cannabis authority RSS feeds + new listings from seed pipeline

### Key Technical Notes
- **CSS version:** `?v=2` — bump `CSS_VERSION` in templates.py on every CSS edit, then rebuild
- **Build:** `python3 scripts/build.py` from project root — generates ALL pages
- **Preview:** `python3 -m http.server 8083` from project root
- **Guides:** Inline in build.py `GUIDES` array (move to JSON later if >15)
- **Related categories:** Uses `content_pillar` field for intelligent linking
- **Money page FAQs:** Generic language when 0 listings, count-specific when populated
- **Logo SVGs:** Use DM Sans font (was Instrument Serif, updated Feb 27)

---

## What This Is
Cannabisers (cannabisers.com) is a B2B directory for cannabis industry ancillary services. Cannabis operators use it to find testing labs, compliance consultants, attorneys, packaging companies, and 14 other service categories across 30+ legal US states. No existing directory owns this space — the closest competitors are MJBizDaily's directory (an afterthought to their media business, ~2,000 thin listings) and Cannabiz Media (a $3,600/yr CRM database, not a discovery directory).

Monetization: featured listings ($49-199/mo), category sponsorships ($500-2K/mo), newsletter sponsorships ($200-500/issue), lead gen ($25-100/lead), data products ($500-2K/report).

## Project Location
`/Users/rome/Documents/projects/cannabisers/`

## Architecture
Python build.py generates all static HTML from JSON data files. Same pattern as Provyx (`/Users/rome/Documents/projects/provyx-website/scripts/`). No Node.js, no Astro, no React. Pure Python + HTML + CSS.

```
scripts/build.py        ← Master build, generates ALL pages + sitemap
scripts/templates.py    ← Shared HTML generators (head, nav, footer, cards, schemas)
scripts/nav_config.py   ← Site constants + navigation source of truth
scripts/seed_data.py    ← Data collection from public licensing databases + Outscraper
data/categories.json    ← 18 category definitions
data/states.json        ← ~38 legal state definitions
data/listings.json      ← All business listings
css/styles.css          ← Full CSS (dark theme, BEM naming)
js/main.js              ← Minimal JS (scroll, nav toggle, forms)
assets/logos/            ← SVG logos (dark + light variants)
assets/favicons/        ← Favicon SVGs
```

**Build:** `python3 scripts/build.py` from project root
**Preview:** `python3 -m http.server 8083` → http://localhost:8083/
**Deploy:** GitHub Pages + custom domain (CNAME: cannabisers.com)
**Plan file:** `/Users/rome/.claude/plans/quirky-discovering-yeti.md`

## Branding (Finalized)
Source files: `/Users/rome/Downloads/cannabisers_branding/` (includes `cannabisers-brand-identity.html` with full interactive brand guide + all CSS)

### Colors
- Background: `#0D1A17` (bg), `#070F0D` (deep), `#152B25` (surface), `#1A362E` (surface-hover), `#112420` (surface-alt)
- Primary (botanical green): `#2D8B6E` / light `#3AA882` / dark `#1F6B53` / muted `rgba(45,139,110,0.15)`
- Accent (warm amber): `#D4915A` / light `#E5A872` / dark `#B87A48` / muted `rgba(212,145,90,0.15)`
- Text: `#E8EDE9` (primary), `#9BAFA5` (secondary), `#5C7A6E` (muted), `#0D1A17` (inverse)
- Semantic: success `#34A97B`, error `#C75D5D`, info `#5AA3D4`, warning = accent
- Borders: `rgba(45,139,110,0.15)` / strong `rgba(45,139,110,0.30)`

### CSS Custom Properties (paste into :root)
```css
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Instrument+Serif:ital@0;1&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
  --color-bg: #0D1A17;
  --color-bg-deep: #070F0D;
  --color-surface: #152B25;
  --color-surface-hover: #1A362E;
  --color-surface-alt: #112420;
  --color-primary: #2D8B6E;
  --color-primary-light: #3AA882;
  --color-primary-dark: #1F6B53;
  --color-primary-muted: rgba(45, 139, 110, 0.15);
  --color-accent: #D4915A;
  --color-accent-light: #E5A872;
  --color-accent-dark: #B87A48;
  --color-accent-muted: rgba(212, 145, 90, 0.15);
  --color-text: #E8EDE9;
  --color-text-secondary: #9BAFA5;
  --color-text-muted: #5C7A6E;
  --color-text-inverse: #0D1A17;
  --color-success: #34A97B;
  --color-warning: #D4915A;
  --color-error: #C75D5D;
  --color-info: #5AA3D4;
  --color-border: rgba(45, 139, 110, 0.15);
  --color-border-strong: rgba(45, 139, 110, 0.30);
  --font-display: 'Instrument Serif', Georgia, serif;
  --font-body: 'DM Sans', -apple-system, sans-serif;
  --font-mono: 'IBM Plex Mono', 'Courier New', monospace;
  --space-1: 4px;  --space-2: 8px;  --space-3: 12px;
  --space-4: 16px; --space-5: 20px; --space-6: 24px;
  --space-8: 32px; --space-10: 40px; --space-12: 48px;
  --space-16: 64px; --space-20: 80px;
  --radius-sm: 4px; --radius-md: 8px;
  --radius-lg: 12px; --radius-xl: 16px;
  --shadow-card: 0 1px 3px rgba(0,0,0,0.3), 0 4px 12px rgba(0,0,0,0.2);
  --shadow-elevated: 0 4px 16px rgba(0,0,0,0.4), 0 8px 32px rgba(0,0,0,0.3);
}
```

### Fonts (Google Fonts)
- **Display:** Instrument Serif (headlines H1-H3, hero text). Weight 400. Letter-spacing -0.02em. Sizes: hero 48px/1.1, h1 36px/1.15, h2 28px/1.2, h3 22px/1.25.
- **Body:** DM Sans (body copy, UI text). Weights 300-700. Standard 16px/1.6.
- **Mono:** IBM Plex Mono (badges, license numbers, stats, metadata). Weights 400-600. Badges 11px uppercase, data 14px, meta 12px.

### Logo ("The Index" concept)
- 3-4 horizontal bars (varying widths, primary green) + amber dot = directory finding metaphor
- `assets/logos/logo-dark.svg` — header use (dark bg, light text wordmark). Viewbox 320x50.
- `assets/logos/logo-light.svg` — light bg variant
- `assets/logos/logo-icon.svg` — icon-only for favicon (40x40 viewbox)
- `assets/logos/logo-icon-light.svg` — icon-only light bg
- `assets/favicons/favicon.svg` — copy of logo-icon.svg

### Visual Language
- **Icons:** Outlined, 1.5px stroke, rounded caps/joins, 24px canvas, primary green (#3AA882) active / muted inactive
- **Buttons:** 8px radius, DM Sans 600 14px, padding 10px 24px, transition all 0.2s
  - Primary: bg accent (#D4915A), text inverse, hover #E5A872 + translateY(-1px) + shadow
  - Secondary: transparent, border border-strong, hover bg surface-hover
  - Ghost: text primary-light, hover bg primary-muted
- **Cards:** 12px radius, 24px padding, 1px border (--color-border), hover stronger border + shadow-card
- **Badges:** IBM Plex Mono 11px uppercase, padding 3px 10px, 4px radius, 1px border
  - Category: bg primary-muted, text primary-light, border primary
  - State: bg accent-muted, text accent, border accent-dark
- **Spacing:** 4px base system (--space-1 through --space-20)
- **Shadows:** card and elevated (see CSS vars)
- **State density gradient:** #0F3D2E (low) → #165A44 → #1F6B53 → #2D8B6E → #3AA882 → #4BC496 (high)

## Page Types

### 1. Homepage (`index.html`)
Hero (Instrument Serif headline, 3 pain stats, 2 CTAs) → Category grid (18 cards) → How It Works (3 steps, HowTo schema) → State grid (density gradient) → Newsletter signup → Claim CTA → FAQ (FAQPage schema).
Schema: @graph [Organization + WebSite + SearchAction + HowTo + FAQPage]

### 2. Category Index (`/categories/index.html`)
Grid of 18 categories with colors, listing counts, descriptions.

### 3. Category Pages (`/categories/{slug}/index.html`) — 18 pages
Hero → state-by-state breakdown → featured listings → FAQ → related categories. BreadcrumbList + FAQPage.

### 4. State Index (`/states/index.html`)
Grid of legal states with legal_status badges, listing counts.

### 5. State Pages (`/states/{slug}/index.html`) — ~38 pages
Hero with legal status → category breakdown → featured listings → regulatory context → FAQ → related states. BreadcrumbList + FAQPage.

### 6. State+Category Pages (`/states/{state}/{category}/index.html`) — THE MONEY PAGES
Only generated when listings exist. "Testing Labs in California" — listing grid + regulatory note + FAQ + related pages + claim CTA. BreadcrumbList + FAQPage. Sitemap priority 0.9.

### 7. City+Category Pages (`/cities/{city}-{state}/{category}/index.html`)
Only generated when 2+ listings exist. Same as state+category but city-scoped. BreadcrumbList.

### 8. Listing Pages (`/listing/{slug}/index.html`)
Full business profile + "Claim This Listing" CTA + LocalBusiness JSON-LD + related listings + newsletter signup. BreadcrumbList.

### 9. Guide Pages (`/guides/{slug}/index.html`)
Editorial content (min 1,200 words). Article JSON-LD + FAQPage + BreadcrumbList. 3+ internal links to category/state pages.

### 10. Static Pages
About, Contact, Newsletter, Privacy, Terms, 404.

## Data Model (per listing in data/listings.json)
```json
{
  "name": "string",
  "slug": "string (unique, format: {name}-{city}-{state})",
  "category": "string (primary category slug)",
  "categories": ["array of category slugs"],
  "state": "string (2-letter abbreviation)",
  "city": "string",
  "address": "string",
  "phone": "string",
  "email": "string",
  "website": "string",
  "license_number": "string",
  "license_type": "string",
  "license_status": "active|inactive|pending",
  "services": ["array of service descriptions"],
  "certifications": ["array"],
  "description": "string",
  "claimed": false,
  "featured": false,
  "date_added": "ISO date",
  "date_updated": "ISO date",
  "source": "string"
}
```

## 18 Service Categories
testing-labs, compliance-consultants, cannabis-attorneys, packaging-labeling, security-services, hvac-climate-control, lighting-equipment, insurance-providers, accounting-tax, real-estate-leasing, pos-software, marketing-branding, transportation-distribution, staffing-hr, banking-financial-services, waste-management, construction-build-out, consulting-general

Each category needs in `data/categories.json`: name, slug, description, icon, color (hex for badges), hero_title, hero_subtitle, pain_headline, content_pillar, faqs array (3+ Q&As).

## SEO Requirements (MANDATORY — every page)

### Meta Tags
- Unique `<title>` 50-60 chars, keyword-first, append `| Cannabisers`
- Unique `<meta name="description">` 120-160 chars
- `<link rel="canonical">` absolute URL with trailing slash
- OG tags: type, url, title, description, image (1200x630)
- Twitter Card: summary_large_image, title, description, image
- No duplicate meta tags (watch for double twitter:card — happened on Provyx)

### JSON-LD Schema (@graph pattern)
All schemas consolidated: `{"@context":"https://schema.org","@graph":[...]}`
- **Homepage:** Organization + WebSite + SearchAction + HowTo + FAQPage
- **Category/State hubs:** Article + BreadcrumbList + FAQPage
- **State+Category pages:** Article + BreadcrumbList + FAQPage
- **Listing pages:** LocalBusiness + BreadcrumbList
- **Guide pages:** Article + BreadcrumbList + FAQPage

### Sitemap (generated by build.py)
Priorities: Homepage 1.0, State+Category 0.9, Category/State hubs 0.8, City+Category/Guides 0.7, Listings 0.6, Static 0.5, Legal 0.4.

### robots.txt
Allow all bots. Explicitly allow: GPTBot, ChatGPT-User, Google-Extended, PerplexityBot, ClaudeBot, Bingbot. Block CCBot. Reference sitemap.

### Internal Linking (3+ per page beyond nav/footer)
- Listing pages → parent state+category, state hub, category hub, 2 related listings
- State+Category pages → state hub, category hub, neighboring state same category, same state other category
- State hubs → all state+category intersections with listings, neighboring states
- Category hubs → all state intersections with listings, related categories
- Guides → relevant category/state pages, related guides
- Related links footer section on every deep page

## Content & Writing Rules

### Voice
Direct, practical, no fluff. Cannabis operators are busy and skeptical.

### NEVER
- False reframes ("not X, it's Y" / "isn't X. It's Y." / "less about X, more about Y") — ZERO TOLERANCE, #1 AI writing tell
- Em-dashes (—) for parenthetical asides — use commas, periods, or colons
- "genuinely/truly/really/actually", "game-changer", "paradigm shift", "robust", "leverage", "seamless", "cutting-edge", "in today's fast-paced"
- Exclamation points in B2B copy
- Unearned declarations ("The story:", "The pattern:", "What this means:", "Let that sink in")
- Short dramatic openers ("The frameworks caught up." / "Everything changed.")
- Performative interjections ("Good question.", "And honestly?")

### ALWAYS
- Contractions (you're, don't, it's, we'll)
- Varied sentence length dramatically (mix 4-word punches with longer flowing sentences)
- Specific numbers over vague claims
- Pain-first headlines (what the operator needs, not what you offer)
- CTAs value-focused ("Find Testing Labs", "Get Listed") not generic ("Get Started", "Learn More")
- Admit limitations ("This won't work for everyone")
- Second-person "you" speaking directly to the reader

### Hero Formula (Harry Dry pattern)
- Title = value hook addressing pain (not description)
- Subtitle = what + how in 1-2 sentences
- Stats = 3 credibility metrics (NO SPACES in numbers — causes mobile line wrapping)
- CTA = value action

### Pain Stats Formatting (CRITICAL)
NO SPACES in stat numbers. Good: `30%`, `$12.9M`, `24&#8209;48hr`, `18mo`. Bad: `13 hrs`, `84 days`, `15+ hrs`.

### FAQ Requirements
Min 3 questions per FAQ section. Must have matching FAQPage JSON-LD schema. Questions target actual search queries.

## Content Pillars
- **Supplier Identification (40%):** How to find/evaluate vendors
- **Compliance & Regulations (30%):** State-by-state legal requirements
- **Supply Chain (20%):** Sourcing, logistics, quality assurance
- **Product Knowledge (5%):** Cannabis product categories and testing
- **Industry Trends (5%):** Market data, growth, emerging categories

## Programmatic SEO Playbooks
1. **Directory** — comprehensive category listings with filtering (PRIMARY)
2. **Locations** — state-by-state hubs with actual local regulatory data (not just city-name swaps)
3. **Comparisons** — vendor evaluation guides
4. **Curation** — "Best {category} in {state}" ranked lists
5. **Glossary** — cannabis industry terms (future expansion)
6. **Integrations** — supply chain education (grower → processor → distributor)

## Forms
All forms via Formspree with honeypot `_gotcha` field. Separate form IDs for: contact, newsletter signup, claim listing.

## templates.py Functions Needed

**From Provyx (adapt for dark theme + cannabis fonts):**
- `get_html_head(title, description, canonical_path, og_image, og_type, schemas)` — full `<head>`
- `get_nav_html()` — header with logo-dark.svg, desktop dropdowns, mobile hamburger
- `get_footer_html()` — 4-column footer from FOOTER_COLUMNS
- `get_breadcrumb_schema(items)` / `get_breadcrumb_html(items)` — BreadcrumbList JSON-LD + visible
- `generate_faq_html(faqs)` — FAQ accordion + FAQPage JSON-LD
- `generate_cta_section(heading, subtext, form_id)` — Formspree form with honeypot
- `generate_related_links(links)` — Related pages footer
- `get_page_wrapper(title, description, canonical, content, schemas, breadcrumbs)` — full page assembly
- `write_page(filepath, html)` — write HTML to disk, mkdir -p

**New for Cannabisers:**
- `generate_newsletter_signup(category=None, state=None)` — contextual email capture
- `generate_claim_cta(listing_slug=None)` — "Claim This Listing" box
- `generate_listing_card(listing)` — card with name, city/state, category badge, license status
- `generate_category_badge(category)` — colored badge
- `generate_state_badge(state)` — amber badge
- `generate_local_business_schema(listing)` — LocalBusiness JSON-LD
- `generate_graph_schema(schemas)` — @graph wrapper for multiple schemas

## build.py Structure

```python
# Load JSON data
CATEGORIES = load_json("categories.json")
STATES = load_json("states.json")
LISTINGS = load_json("listings.json")

# Build index lookups
LISTINGS_BY_STATE = {}
LISTINGS_BY_CATEGORY = {}
LISTINGS_BY_STATE_CATEGORY = {}

# Build functions (one per page type)
build_homepage()
build_category_index() + build_category_page(cat)
build_state_index() + build_state_page(state)
build_state_category_page(state, cat)  # only if listings exist
build_city_category_page(city, state, cat)  # only if 2+ listings
build_listing_page(listing)
build_guides_index() + build_guide_page(guide)
build_about(), build_contact(), build_newsletter(), build_privacy(), build_terms(), build_404()
build_sitemap()
build_robots_txt()
```

## Reference Repos
- **Provyx build pattern:** `/Users/rome/Documents/projects/provyx-website/scripts/` (build.py, templates.py, nav_config.py — READ THESE for implementation patterns)
- **DataStackGuide SEO:** `/Users/rome/Documents/projects/datastackguide/` (schema patterns in `src/layouts/BaseLayout.astro`, internal linking in page templates)
- **Marketingskills frameworks:** https://github.com/coreyhaines31/marketingskills (`skills/programmatic-seo`, `skills/content-strategy`)
- **Branding interactive guide:** `/Users/rome/Downloads/cannabisers_branding/cannabisers-brand-identity.html`

## Build Order
1. `nav_config.py` → `templates.py` → `styles.css` (infrastructure)
2. `build.py` skeleton + homepage (proves the system works)
3. Category index + 18 category pages + State index + ~38 state pages
4. State+Category money pages + City+Category pages + Listing pages
5. `seed_data.py` + initial CO/CA data seed
6. Guide/editorial pages (5-10 initial)
7. Static pages (about, contact, newsletter, privacy, terms, 404)
8. Verification: build, serve locally, check SEO + mobile

## Verification
- `python3 scripts/build.py` completes without errors
- `python3 -m http.server 8083` → check every page type at localhost:8083
- Every page: unique title <60 chars, unique description 120-160 chars, canonical URL, OG tags, Twitter tags
- Every inner page: BreadcrumbList JSON-LD
- FAQ pages: FAQPage JSON-LD matching visible content
- Homepage: Organization + WebSite @graph
- Listing pages: LocalBusiness JSON-LD
- Mobile: nav collapses, cards stack, stats don't wrap at 375px
- No broken internal links (grep all href paths, verify file exists)
- CSS version param (`?v=1`) on all `<link>` tags
- No placeholder text
- sitemap.xml includes all generated pages
- robots.txt references sitemap
