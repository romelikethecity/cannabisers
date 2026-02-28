# Cannabisers — The Cannabis Industry Directory

## Project Overview
B2B directory for the cannabis industry's ancillary services ecosystem. Helps cannabis operators find suppliers, labs, consultants, and service providers by state and city. Monetized through featured listings, category sponsorships, lead gen, and newsletter sponsorships.

**Domain:** cannabisers.com
**Tagline:** The Cannabis Industry Directory
**Target audience:** Cannabis operators (dispensary owners, cultivators, processors, distributors) searching for B2B services
**Local:** `/Users/rome/Documents/projects/cannabisers/`
**Preview:** `python3 -m http.server 8083` from project root

## Architecture
- **Build:** `scripts/build.py` generates all HTML pages from data files
- **Data:** `data/*.json` — structured listings seeded from state licensing databases + Outscraper
- **Templates:** Python string templates (same pattern as Provyx build.py)
- **Deploy:** GitHub Pages + custom domain (cannabisers.com)
- **CSS:** Single `css/styles.css?v=1` — bump version on every CSS edit, update ALL HTML files

## Page Taxonomy
1. **Homepage** — hero + category grid + state map + newsletter signup
2. **State pages** (`/states/{state}/`) — all categories in that state, license counts, regulatory context
3. **Category pages** (`/categories/{category}/`) — all states for that category, national overview
4. **State + Category pages** (`/states/{state}/{category}/`) — THE MONEY PAGES. Individual listings for that intersection.
5. **City + Category pages** (`/cities/{city}-{state}/{category}/`) — local-level listings
6. **Individual listing pages** (`/listing/{slug}/`) — single business profile with claim CTA
7. **Comparison/guide pages** (`/guides/`) — editorial content for SEO authority
8. **About, Contact, Newsletter** — standard pages

## Data Model (per listing)
```json
{
  "name": "string",
  "slug": "string",
  "category": "string (primary)",
  "categories": ["array of all categories"],
  "state": "string (2-letter)",
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
  "source": "string (where data came from)"
}
```

## Categories (B2B Ancillary Services)
1. Testing Labs
2. Compliance Consultants
3. Cannabis Attorneys
4. Packaging & Labeling
5. Security Services
6. HVAC & Climate Control
7. Lighting & Equipment
8. Insurance Providers
9. Accounting & Tax
10. Real Estate & Leasing
11. POS & Software
12. Marketing & Branding
13. Transportation & Distribution
14. Staffing & HR
15. Banking & Financial Services
16. Waste Management
17. Construction & Build-Out
18. Consulting (General)

## SEO Requirements (MANDATORY — every page)
- Unique title tag (50-60 chars, keyword-first)
- Unique meta description (150-160 chars)
- Canonical URL (absolute, trailing slash)
- Open Graph tags (type, url, title, description, image 1200x630)
- Twitter Card tags (card, title, description, image)
- BreadcrumbList JSON-LD on all inner pages
- FAQPage JSON-LD on pages with FAQ sections (min 3 Q&A)
- Organization + WebSite JSON-LD on homepage (use @graph pattern)
- LocalBusiness JSON-LD on individual listing pages
- sitemap.xml with all pages
- robots.txt pointing to sitemap

## Internal Linking Rules
- Every deep page links to parent hub (state page, category page)
- State pages link to all category intersections in that state
- Category pages link to all state intersections for that category
- Listing pages link to: parent state+category page, related listings, category hub
- 3+ internal links per page beyond nav/footer
- Related links footer on every deep page

## Content & Writing Rules
- **Voice:** Direct, practical, no fluff. Cannabis operators are busy and skeptical.
- **NEVER:** False reframes ("not X, it's Y"), em-dashes for asides, "genuinely/truly/really/actually", "game-changer", "paradigm shift", "robust", "leverage", "seamless"
- **NEVER:** Exclamation points in B2B copy
- **ALWAYS:** Contractions, varied sentence length, specific numbers, admit limitations
- **ALWAYS:** Pain-first headlines (what the operator needs), not description-first
- **CTAs:** Value-focused ("Find Testing Labs", "Get Listed"), not generic ("Get Started", "Learn More")
- **Hero formula:** Title = value hook addressing pain. Subtitle = what + how. Stats = 3 credibility metrics. CTA = value action.

## Pain Stats Formatting (CRITICAL)
- NO SPACES in stat numbers (causes mobile line wrapping)
- Good: `30%`, `$12.9M`, `24&#8209;48hr`, `18mo`, `11K+`
- Bad: `13 hrs`, `84 days`, `15+ hrs`

## Claim This Listing
- Every seeded listing has "Claim This Listing" CTA from day 1
- Links to a form (Formspree with honeypot `_gotcha` field)
- Claimed listings get: edit rights, logo upload, enhanced description, featured placement option

## Newsletter
- Email capture on every page: "Get notified when new {category} vendors are added in {state}"
- Weekly digest: new licenses granted, regulatory changes, new listings
- Monetized through ancillary business sponsorships (no cannabis advertising restrictions on lawyers, accountants, security, HVAC, etc.)

## Data Sources (all free/public)
- State cannabis licensing databases (every legal state publishes these)
- State business registrations
- Outscraper/Google Places for ancillary businesses serving cannabis
- Industry association membership lists (NCIA, state associations)
- Conference exhibitor lists (MJBizCon, CannaCon)

## File Structure
```
/cannabisers
  /scripts/
    build.py           ← generates all HTML pages
    nav_config.py      ← navigation source of truth
    seed_data.py       ← initial data seeding from public sources
  /data/
    listings.json      ← all business listings
    categories.json    ← category metadata (name, slug, icon, color, description)
    states.json        ← state metadata (name, abbrev, legal status, license URL, regulatory notes)
  /css/
    styles.css?v=1
  /js/
    main.js
  /assets/
    /logos/
    /icons/
    /social/           ← OG images (1200x630)
    /favicons/
  /pages/              ← generated HTML output
    /states/
    /categories/
    /cities/
    /listings/
    /guides/
  index.html
  sitemap.xml
  robots.txt
  CNAME
```

## Branding (Finalized)
Source files: `/Users/rome/Downloads/cannabisers_branding/`

### Colors (Dark Theme)
- Background: `#0D1A17` (bg), `#070F0D` (deep), `#152B25` (surface), `#1A362E` (surface-hover), `#112420` (surface-alt)
- Primary (botanical green): `#2D8B6E` / light `#3AA882` / dark `#1F6B53` / muted `rgba(45,139,110,0.15)`
- Accent (warm amber): `#D4915A` / light `#E5A872` / dark `#B87A48` / muted `rgba(212,145,90,0.15)`
- Text: `#E8EDE9` (primary), `#9BAFA5` (secondary), `#5C7A6E` (muted), `#0D1A17` (inverse)
- Semantic: success `#34A97B`, error `#C75D5D`, info `#5AA3D4`, warning = accent
- Borders: `rgba(45,139,110,0.15)` / strong `rgba(45,139,110,0.30)`

### Fonts (Google Fonts)
- **Display:** Instrument Serif (headlines, hero). Weight 400. -0.02em letter-spacing.
- **Body:** DM Sans (body, UI). Weights 300-700.
- **Mono:** IBM Plex Mono (badges, stats, license numbers). Weights 400-600.

### Logo ("The Index")
- `assets/logos/logo-dark.svg` — header (dark bg, light text wordmark)
- `assets/logos/logo-light.svg` — light bg variant
- `assets/logos/logo-icon.svg` — icon-only (dark variant)
- `assets/logos/logo-icon-light.svg` — icon-only (light variant)
- `assets/favicons/favicon.svg` — favicon (from logo-icon.svg)

### Visual Language
- Icons: outlined, 1.5px stroke, rounded caps/joins, 24px canvas
- Buttons: 8px radius, DM Sans 600 14px. Primary = amber. Secondary = border. Ghost = text.
- Cards: 12px radius, 24px padding, 1px border, hover = stronger border + shadow
- Badges: IBM Plex Mono 11px uppercase, 4px radius. Category = green. State = amber.
- Spacing: 4px base (--space-1 through --space-20)

### Handoff
- **HANDOFF.md** — self-contained context for new Claude sessions to build the entire site
- **Plan file:** `/Users/rome/.claude/plans/quirky-discovering-yeti.md`

## Git
- Repo: `romelikethecity/cannabisers` (create when ready)
- Deploy: GitHub Pages with custom domain
- CNAME: `cannabisers.com`
