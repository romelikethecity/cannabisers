#!/usr/bin/env python3
"""
Seed data script for Cannabisers.

Populates data/listings.json with cannabis ancillary service providers.
Uses Outscraper (Google Places) to search for providers by category and state.

Usage:
    # Search a single category in a single state
    python3 scripts/seed_data.py --category testing-labs --state CA

    # Search a single category across all states
    python3 scripts/seed_data.py --category testing-labs --all-states

    # Search all categories in a single state (good for testing)
    python3 scripts/seed_data.py --all-categories --state CA

    # Full seed (all categories, all states) — expensive, use with care
    python3 scripts/seed_data.py --full

    # Dry run (show what would be searched, don't call API)
    python3 scripts/seed_data.py --category testing-labs --state CA --dry-run

Requires:
    pip install outscraper
    OUTSCRAPER_API_KEY in environment or .env file

Cost:
    Outscraper charges ~$2 per 1,000 results.
    18 categories × 36 states = 648 queries.
    At ~20 results per query average, that's ~$26 for a full seed.
"""

import os
import sys
import json
import time
import argparse
import re
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# Load .env if present
env_path = os.path.join(PROJECT_ROOT, ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip())

# Also check verum .env as fallback (same Outscraper key)
verum_env = os.path.expanduser("~/Documents/projects/verum/data_prep_app/.env")
if os.path.exists(verum_env):
    with open(verum_env) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip())


# =============================================================================
# SEARCH QUERIES PER CATEGORY
# =============================================================================

CATEGORY_QUERIES = {
    "testing-labs": [
        "cannabis testing laboratory",
        "marijuana testing lab",
        "THC testing lab",
    ],
    "compliance-consultants": [
        "cannabis compliance consultant",
        "marijuana regulatory consultant",
    ],
    "cannabis-attorneys": [
        "cannabis attorney",
        "marijuana lawyer",
        "cannabis law firm",
    ],
    "packaging-labeling": [
        "cannabis packaging company",
        "marijuana packaging supplier",
    ],
    "security-services": [
        "cannabis security company",
        "dispensary security services",
    ],
    "hvac-climate-control": [
        "cannabis HVAC contractor",
        "grow room climate control",
    ],
    "lighting-equipment": [
        "cannabis grow equipment supplier",
        "commercial grow lights cannabis",
    ],
    "insurance-providers": [
        "cannabis insurance broker",
        "marijuana business insurance",
    ],
    "accounting-tax": [
        "cannabis CPA",
        "cannabis accountant",
        "marijuana tax specialist",
    ],
    "real-estate-leasing": [
        "cannabis real estate broker",
        "marijuana commercial property",
    ],
    "pos-software": [
        "cannabis POS system",
        "dispensary point of sale",
    ],
    "marketing-branding": [
        "cannabis marketing agency",
        "marijuana branding company",
    ],
    "transportation-distribution": [
        "cannabis transport company",
        "marijuana distribution service",
    ],
    "staffing-hr": [
        "cannabis staffing agency",
        "marijuana recruiting firm",
    ],
    "banking-financial-services": [
        "cannabis banking",
        "cannabis credit union",
    ],
    "waste-management": [
        "cannabis waste disposal",
        "marijuana waste management",
    ],
    "construction-build-out": [
        "dispensary build out contractor",
        "cannabis facility construction",
    ],
    "consulting-general": [
        "cannabis business consultant",
        "marijuana consulting firm",
    ],
}

# State name lookup
STATE_NAMES = {}


def load_states():
    """Load state data and build lookup."""
    global STATE_NAMES
    states_path = os.path.join(DATA_DIR, "states.json")
    with open(states_path) as f:
        states = json.load(f)
    STATE_NAMES = {s["abbrev"]: s["name"] for s in states}
    return states


def load_existing_listings():
    """Load existing listings from JSON file."""
    path = os.path.join(DATA_DIR, "listings.json")
    with open(path) as f:
        return json.load(f)


def save_listings(listings):
    """Save listings to JSON file."""
    path = os.path.join(DATA_DIR, "listings.json")
    with open(path, "w") as f:
        json.dump(listings, f, indent=2)
    print(f"  Saved {len(listings)} listings to {path}")


def slugify(text):
    """Generate URL slug from text."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def make_listing_slug(name, city, state):
    """Generate unique slug for a listing."""
    return slugify(f"{name}-{city}-{state}")


def search_outscraper(query, location, limit=20):
    """Search Outscraper Google Places for businesses.

    Args:
        query: Search query string
        location: Location string (e.g., "California, USA")
        limit: Max results per query

    Returns:
        List of dicts with business data, or empty list on error.
    """
    try:
        from outscraper import ApiClient
    except ImportError:
        print("  ERROR: outscraper package not installed. Run: pip install outscraper")
        return []

    api_key = os.environ.get("OUTSCRAPER_API_KEY", "")
    if not api_key:
        print("  ERROR: OUTSCRAPER_API_KEY not set in environment or .env")
        return []

    client = ApiClient(api_key=api_key)

    try:
        results = client.google_maps_search(
            f"{query} {location}",
            limit=limit,
            language="en",
            region="us",
        )

        if not results or not results[0]:
            return []

        return results[0]

    except Exception as e:
        print(f"  ERROR: Outscraper search failed: {e}")
        return []


def outscraper_to_listing(result, category_slug, state_abbrev):
    """Convert an Outscraper result to a listing dict.

    Args:
        result: Dict from Outscraper API
        category_slug: Primary category slug
        state_abbrev: 2-letter state code

    Returns:
        Listing dict matching the data model, or None if insufficient data.
    """
    name = result.get("name", "").strip()
    if not name:
        return None

    city = result.get("city", "") or ""
    state = result.get("state", state_abbrev) or state_abbrev
    address = result.get("full_address", "") or result.get("street", "") or ""
    phone = result.get("phone", "") or ""
    website = result.get("site", "") or ""
    description = result.get("description", "") or result.get("about", "") or ""

    # Skip results that are clearly not cannabis-related
    skip_keywords = ["restaurant", "pizza", "hair salon", "nail", "dental",
                     "veterinary", "pet", "auto repair", "car wash"]
    name_lower = name.lower()
    for kw in skip_keywords:
        if kw in name_lower:
            return None

    slug = make_listing_slug(name, city, state_abbrev)

    return {
        "name": name,
        "slug": slug,
        "category": category_slug,
        "categories": [category_slug],
        "state": state_abbrev.upper(),
        "city": city,
        "address": address,
        "phone": phone,
        "email": "",
        "website": website,
        "license_number": "",
        "license_type": "",
        "license_status": "",
        "services": [],
        "certifications": [],
        "description": description[:500] if description else "",
        "claimed": False,
        "featured": False,
        "date_added": datetime.now().strftime("%Y-%m-%d"),
        "date_updated": datetime.now().strftime("%Y-%m-%d"),
        "source": "outscraper",
    }


def seed_category_state(category_slug, state_abbrev, existing_slugs, dry_run=False):
    """Seed listings for one category in one state.

    Args:
        category_slug: Category to search
        state_abbrev: State to search
        existing_slugs: Set of existing listing slugs (for dedup)
        dry_run: If True, print queries but don't call API

    Returns:
        List of new listing dicts
    """
    queries = CATEGORY_QUERIES.get(category_slug, [])
    state_name = STATE_NAMES.get(state_abbrev, state_abbrev)
    new_listings = []
    seen_names = set()

    for query in queries:
        location = f"{state_name}, USA"
        print(f"  Searching: \"{query}\" in {location}")

        if dry_run:
            continue

        results = search_outscraper(query, location, limit=20)
        time.sleep(0.5)  # Rate limit courtesy

        for result in results:
            listing = outscraper_to_listing(result, category_slug, state_abbrev)
            if not listing:
                continue

            # Dedup by slug and by name
            if listing["slug"] in existing_slugs:
                continue
            if listing["name"].lower() in seen_names:
                continue

            new_listings.append(listing)
            existing_slugs.add(listing["slug"])
            seen_names.add(listing["name"].lower())

    return new_listings


def main():
    parser = argparse.ArgumentParser(description="Seed Cannabisers listings data")
    parser.add_argument("--category", type=str, help="Single category slug to search")
    parser.add_argument("--state", type=str, help="Single state abbreviation (e.g., CA)")
    parser.add_argument("--all-states", action="store_true", help="Search all states")
    parser.add_argument("--all-categories", action="store_true", help="Search all categories")
    parser.add_argument("--full", action="store_true", help="Full seed (all categories × all states)")
    parser.add_argument("--dry-run", action="store_true", help="Show queries without calling API")
    parser.add_argument("--limit", type=int, default=20, help="Results per query (default 20)")
    args = parser.parse_args()

    states = load_states()
    state_abbrevs = [s["abbrev"] for s in states]

    # Determine what to search
    categories = list(CATEGORY_QUERIES.keys())
    search_states = state_abbrevs

    if args.full:
        pass  # Use all categories and all states
    elif args.category and args.all_states:
        categories = [args.category]
    elif args.all_categories and args.state:
        search_states = [args.state.upper()]
    elif args.category and args.state:
        categories = [args.category]
        search_states = [args.state.upper()]
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python3 scripts/seed_data.py --category testing-labs --state CA")
        print("  python3 scripts/seed_data.py --category testing-labs --all-states")
        print("  python3 scripts/seed_data.py --full --dry-run")
        return

    # Load existing
    existing = load_existing_listings()
    existing_slugs = {l["slug"] for l in existing}
    total_new = 0

    print(f"\n{'='*60}")
    print(f"  Cannabisers Seed Data")
    print(f"  Categories: {len(categories)} | States: {len(search_states)}")
    print(f"  Existing listings: {len(existing)}")
    print(f"  Dry run: {args.dry_run}")
    print(f"{'='*60}\n")

    for cat_slug in categories:
        print(f"\n--- {cat_slug} ---")
        for state_abbrev in search_states:
            new = seed_category_state(cat_slug, state_abbrev, existing_slugs, args.dry_run)
            if new:
                existing.extend(new)
                total_new += len(new)
                print(f"    +{len(new)} new listings in {state_abbrev}")

    if not args.dry_run and total_new > 0:
        save_listings(existing)

    print(f"\n{'='*60}")
    print(f"  Done. {total_new} new listings added.")
    print(f"  Total listings: {len(existing)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
