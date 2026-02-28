#!/usr/bin/env python3
"""
Centralized navigation configuration for Cannabisers.

Edit this file to update navigation across ALL pages on the site.
After editing, regenerate all pages by running:
    python3 scripts/build.py
"""

# Site info
SITE_NAME = "Cannabisers"
SITE_URL = "https://cannabisers.com"
SITE_TAGLINE = "The Cannabis Industry Directory"
COPYRIGHT_YEAR = "2026"

# CTA button
CTA_HREF = "/contact/"
CTA_LABEL = "Get Listed"

# Main navigation items (appear in header)
NAV_ITEMS = [
    {
        "href": "/categories/",
        "label": "Categories",
        "children": [
            {"href": "/categories/", "label": "All Categories"},
            {"href": "/categories/testing-labs/", "label": "Testing Labs"},
            {"href": "/categories/compliance-consultants/", "label": "Compliance"},
            {"href": "/categories/cannabis-attorneys/", "label": "Attorneys"},
            {"href": "/categories/packaging-labeling/", "label": "Packaging"},
            {"href": "/categories/insurance-providers/", "label": "Insurance"},
            {"href": "/categories/accounting-tax/", "label": "Accounting"},
        ],
    },
    {
        "href": "/states/",
        "label": "States",
        "children": [
            {"href": "/states/", "label": "All States"},
            {"href": "/states/california/", "label": "California"},
            {"href": "/states/colorado/", "label": "Colorado"},
            {"href": "/states/michigan/", "label": "Michigan"},
            {"href": "/states/illinois/", "label": "Illinois"},
            {"href": "/states/oregon/", "label": "Oregon"},
            {"href": "/states/new-york/", "label": "New York"},
        ],
    },
    {"href": "/guides/", "label": "Guides"},
    {"href": "/about/", "label": "About"},
]

# Footer link columns
FOOTER_COLUMNS = {
    "Top Categories": [
        {"href": "/categories/testing-labs/", "label": "Testing Labs"},
        {"href": "/categories/compliance-consultants/", "label": "Compliance Consultants"},
        {"href": "/categories/cannabis-attorneys/", "label": "Cannabis Attorneys"},
        {"href": "/categories/packaging-labeling/", "label": "Packaging & Labeling"},
        {"href": "/categories/insurance-providers/", "label": "Insurance Providers"},
        {"href": "/categories/accounting-tax/", "label": "Accounting & Tax"},
    ],
    "Top States": [
        {"href": "/states/california/", "label": "California"},
        {"href": "/states/colorado/", "label": "Colorado"},
        {"href": "/states/michigan/", "label": "Michigan"},
        {"href": "/states/illinois/", "label": "Illinois"},
        {"href": "/states/oregon/", "label": "Oregon"},
        {"href": "/states/new-york/", "label": "New York"},
    ],
    "Resources": [
        {"href": "/guides/", "label": "Industry Guides"},
        {"href": "/newsletter/", "label": "Newsletter"},
        {"href": "/contact/", "label": "Contact Us"},
    ],
    "Company": [
        {"href": "/about/", "label": "About Cannabisers"},
        {"href": "/privacy/", "label": "Privacy Policy"},
        {"href": "/terms/", "label": "Terms of Service"},
    ],
}
