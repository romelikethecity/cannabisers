#!/usr/bin/env python3
"""
Shared HTML generation module for the Cannabisers website build system.

This module provides all common HTML template functions used by build.py
to generate static pages. It reads navigation and footer data from
nav_config.py and produces clean, SEO-optimized HTML output.

Usage:
    from templates import get_page_wrapper, write_page

    html = get_page_wrapper(
        title="Testing Labs in California",
        description="Find licensed cannabis testing labs in California.",
        canonical_path="/states/california/testing-labs/",
        body_content="<section>...</section>",
        active_page="/states/",
    )
    write_page("states/california/testing-labs/index.html", html)
"""

import os
import json
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nav_config import (
    NAV_ITEMS,
    FOOTER_COLUMNS,
    SITE_NAME,
    SITE_URL,
    SITE_TAGLINE,
    COPYRIGHT_YEAR,
    CTA_HREF,
    CTA_LABEL,
)


# =============================================================================
# CONSTANTS
# =============================================================================

BASE_URL = "https://cannabisers.com"
CSS_VERSION = "2"
DEFAULT_OG_IMAGE = "og-default.png"
GA_MEASUREMENT_ID = ""  # Set to "G-XXXXXXXXXX" when ready


# =============================================================================
# HTML HEAD
# =============================================================================

def get_html_head(title, description, canonical_path, extra_schema="",
                  noindex=False, og_type="website"):
    """Generate complete <head> section with meta, OG, fonts, favicon, CSS.

    Args:
        title: Page title (without site name suffix). 50-60 chars target.
        description: Meta description. 120-158 chars target.
        canonical_path: Path for canonical URL, e.g. "/states/california/"
        extra_schema: Optional additional JSON-LD schema script tags
        noindex: If True, add robots noindex and omit canonical tag
        og_type: Open Graph type, e.g. "website" or "article"
    """
    canonical = f"{BASE_URL}{canonical_path}"
    full_title = f"{title} | {SITE_NAME}" if title != SITE_NAME else title
    og_image = f"{BASE_URL}/assets/social/{DEFAULT_OG_IMAGE}"
    canonical_tag = "" if noindex else f'\n    <link rel="canonical" href="{canonical}">'
    if noindex:
        robots_tag = '\n    <meta name="robots" content="noindex">'
    else:
        robots_tag = ""

    ga_html = ""
    if GA_MEASUREMENT_ID:
        ga_html = f'''
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_MEASUREMENT_ID}')</script>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#0D1A17">{ga_html}
    <title>{full_title}</title>
    <meta name="description" content="{description}">{canonical_tag}{robots_tag}

    <!-- Open Graph -->
    <meta property="og:type" content="{og_type}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:title" content="{full_title}">
    <meta property="og:description" content="{description}">
    <meta property="og:site_name" content="{SITE_NAME}">
    <meta property="og:image" content="{og_image}">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{full_title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{og_image}">
{extra_schema}
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="/assets/favicons/favicon.svg">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap">

    <!-- CSS -->
    <link rel="stylesheet" href="/css/styles.css?v={CSS_VERSION}">
</head>'''


# =============================================================================
# NAVIGATION
# =============================================================================

def _build_desktop_nav_items(active_page=None):
    """Build desktop nav list items HTML."""
    items_html = ""
    for item in NAV_ITEMS:
        children = item.get("children")
        is_active = active_page and active_page.startswith(item["href"])

        if children:
            chevron_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12" fill="currentColor"><path d="M2 4l4 4 4-4"/></svg>'
            dropdown_items = ""
            for child in children:
                dropdown_items += f'<a href="{child["href"]}" class="nav__dropdown-item">{child["label"]}</a>\n'

            active_cls = " active" if is_active else ""
            items_html += f'''<li class="nav__item--dropdown{active_cls}">
                    <button class="nav__dropdown-toggle" aria-expanded="false">{item["label"]} {chevron_svg}</button>
                    <div class="nav__dropdown">
                        {dropdown_items}
                    </div>
                </li>'''
        else:
            link_classes = "nav__link nav__link--active" if is_active else "nav__link"
            items_html += f'<li><a href="{item["href"]}" class="{link_classes}">{item["label"]}</a></li>'

    return items_html


def _build_mobile_nav_items():
    """Build mobile nav list items HTML."""
    items_html = ""
    for item in NAV_ITEMS:
        children = item.get("children")

        if children:
            chevron_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12" fill="currentColor"><path d="M2 4l4 4 4-4"/></svg>'
            dropdown_items = ""
            for child in children:
                dropdown_items += f'<a href="{child["href"]}" class="nav__dropdown-item">{child["label"]}</a>\n'

            items_html += f'''<li class="nav__item--dropdown">
                    <button class="nav__dropdown-toggle" aria-expanded="false">{item["label"]} {chevron_svg}</button>
                    <div class="nav__dropdown">
                        {dropdown_items}
                    </div>
                </li>'''
        else:
            items_html += f'<li><a href="{item["href"]}" class="nav__link">{item["label"]}</a></li>'

    return items_html


def get_nav_html(active_page=None):
    """Generate full header + mobile nav HTML with inline JS toggle.

    Args:
        active_page: Current page path for active state, e.g. "/categories/"
    """
    desktop_items = _build_desktop_nav_items(active_page)
    mobile_items = _build_mobile_nav_items()

    return f'''<body>
    <a href="#main-content" class="sr-only sr-only--focusable">Skip to main content</a>
    <header class="header" role="banner">
        <div class="container header__inner">
            <a href="/" class="header__logo">
                <img src="/assets/logos/logo-dark.svg" alt="{SITE_NAME}" class="header__logo-img" height="40" fetchpriority="high">
            </a>

            <nav class="nav--desktop" role="navigation" aria-label="Main navigation">
                <ul class="nav__list">
                    {desktop_items}
                </ul>
            </nav>

            <div class="header__cta">
                <a href="{CTA_HREF}" class="btn btn--primary btn--sm">{CTA_LABEL}</a>
            </div>

            <button class="menu-toggle" aria-label="Open menu" aria-expanded="false">
                <span class="menu-toggle__icon"></span>
            </button>
        </div>
    </header>

    <nav class="nav--mobile" role="navigation" aria-label="Mobile navigation">
        <ul class="nav__list">
            {mobile_items}
        </ul>
        <a href="{CTA_HREF}" class="btn btn--primary">{CTA_LABEL}</a>
    </nav>

    <script>
    (function(){{
        var toggle=document.querySelector('.menu-toggle');
        var mobileNav=document.querySelector('.nav--mobile');
        if(!toggle||!mobileNav)return;
        toggle.addEventListener('click',function(){{
            var open=mobileNav.classList.toggle('active');
            toggle.classList.toggle('active');
            toggle.setAttribute('aria-expanded',open);
            document.body.style.overflow=open?'hidden':'';
        }});
        var dropdowns=document.querySelectorAll('.nav__item--dropdown .nav__dropdown-toggle');
        dropdowns.forEach(function(btn){{
            btn.addEventListener('click',function(e){{
                e.preventDefault();
                var parent=btn.closest('.nav__item--dropdown');
                var wasActive=parent.classList.contains('active');
                if(mobileNav.contains(parent)){{
                    mobileNav.querySelectorAll('.nav__item--dropdown.active').forEach(function(d){{d.classList.remove('active');d.querySelector('.nav__dropdown-toggle').setAttribute('aria-expanded','false');}});
                }}
                if(!wasActive){{
                    parent.classList.add('active');
                    btn.setAttribute('aria-expanded','true');
                }}else{{
                    parent.classList.remove('active');
                    btn.setAttribute('aria-expanded','false');
                }}
            }});
        }});
    }})();
    </script>

    <main id="main-content">'''


# =============================================================================
# FOOTER
# =============================================================================

def get_footer_html():
    """Generate complete footer with logo, tagline, link columns, copyright."""
    columns_html = ""
    for heading, links in FOOTER_COLUMNS.items():
        links_html = ""
        for link in links:
            if link["href"].startswith("http"):
                links_html += f'<li><a href="{link["href"]}" target="_blank" rel="noopener noreferrer">{link["label"]}</a></li>\n'
            else:
                links_html += f'<li><a href="{link["href"]}">{link["label"]}</a></li>\n'

        columns_html += f'''
            <div class="footer__column">
                <h4 class="footer__heading">{heading}</h4>
                <ul class="footer__links">
                    {links_html}
                </ul>
            </div>'''

    return f'''
    </main>

    <footer class="footer" role="contentinfo">
        <div class="container">
            <div class="footer__grid">
                <div class="footer__brand">
                    <a href="/" class="footer__logo">
                        <img src="/assets/logos/logo-dark.svg" alt="{SITE_NAME}" class="footer__logo-img" height="32" loading="lazy">
                    </a>
                    <p class="footer__tagline">{SITE_TAGLINE}</p>
                </div>
                {columns_html}
            </div>
            <div class="footer__bottom">
                <span>&copy; {COPYRIGHT_YEAR} {SITE_NAME}. All rights reserved.</span>
            </div>
        </div>
    </footer>

    <script src="/js/main.js" defer></script>
</body>
</html>'''


# =============================================================================
# BREADCRUMBS
# =============================================================================

def get_breadcrumb_schema(breadcrumbs):
    """Generate BreadcrumbList JSON-LD schema.

    Args:
        breadcrumbs: List of dicts with 'name' and 'url' keys.
    Returns:
        JSON-LD script tag as string, or empty string if no breadcrumbs.
    """
    if not breadcrumbs:
        return ""

    items = []
    for i, crumb in enumerate(breadcrumbs, 1):
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": crumb.get("name", ""),
            "item": crumb.get("url", "")
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }

    return f'''
    <script type="application/ld+json">
{json.dumps(schema, indent=2)}
    </script>'''


def get_breadcrumb_html(breadcrumbs):
    """Generate visible breadcrumb navigation HTML.

    Args:
        breadcrumbs: List of dicts with 'name' and 'url' keys.
                    Last item is treated as current page (no link).
    """
    if not breadcrumbs:
        return ""

    crumb_parts = []
    for i, crumb in enumerate(breadcrumbs):
        if i < len(breadcrumbs) - 1:
            crumb_parts.append(f'<a href="{crumb["url"]}">{crumb["name"]}</a>')
            crumb_parts.append('<span class="breadcrumb__separator">/</span>')
        else:
            crumb_parts.append(f'<span class="breadcrumb__current">{crumb["name"]}</span>')

    return f'''<nav class="breadcrumb" aria-label="Breadcrumb">
            {" ".join(crumb_parts)}
        </nav>'''


# =============================================================================
# SCHEMA HELPERS
# =============================================================================

def generate_graph_schema(schemas):
    """Wrap multiple schemas in an @graph array.

    Args:
        schemas: List of schema dicts (without @context)
    Returns:
        JSON-LD script tag as string
    """
    if not schemas:
        return ""

    graph = {
        "@context": "https://schema.org",
        "@graph": schemas
    }

    return f'''
    <script type="application/ld+json">
{json.dumps(graph, indent=2)}
    </script>'''


def generate_local_business_schema(listing):
    """Generate LocalBusiness JSON-LD for a listing.

    Args:
        listing: Dict with listing data
    Returns:
        Schema dict (no @context, for use in @graph)
    """
    schema = {
        "@type": "LocalBusiness",
        "name": listing.get("name", ""),
        "description": listing.get("description", ""),
    }

    if listing.get("address"):
        schema["address"] = {
            "@type": "PostalAddress",
            "streetAddress": listing.get("address", ""),
            "addressLocality": listing.get("city", ""),
            "addressRegion": listing.get("state", ""),
            "addressCountry": "US",
        }

    if listing.get("phone"):
        schema["telephone"] = listing["phone"]
    if listing.get("website"):
        schema["url"] = listing["website"]

    return schema


def generate_article_schema(title, description, canonical_path,
                            date_published="2026-02-27", date_modified=None):
    """Generate Article JSON-LD schema.

    Args:
        title: Article headline
        description: Article description
        canonical_path: Page path
        date_published: ISO date
        date_modified: ISO date, defaults to date_published
    Returns:
        Schema dict (no @context, for use in @graph)
    """
    if not date_modified:
        date_modified = date_published

    return {
        "@type": "Article",
        "headline": title,
        "description": description,
        "url": f"{BASE_URL}{canonical_path}",
        "inLanguage": "en-US",
        "datePublished": date_published,
        "dateModified": date_modified,
        "author": {
            "@type": "Organization",
            "@id": f"{BASE_URL}/#organization",
            "name": SITE_NAME,
        },
        "publisher": {
            "@type": "Organization",
            "@id": f"{BASE_URL}/#organization",
            "name": SITE_NAME,
        },
    }


# =============================================================================
# FAQ
# =============================================================================

def generate_faq_html(faqs, heading="Frequently Asked Questions"):
    """Generate FAQ section HTML with FAQPage schema markup.

    Args:
        faqs: List of dicts with 'question' and 'answer' keys
        heading: Section heading text

    Returns:
        Tuple of (html_string, schema_dict) for FAQ section. Schema dict
        has no @context (for use in @graph).
    """
    if not faqs:
        return "", None

    faq_items_html = ""
    for faq in faqs:
        faq_items_html += f'''
                <details class="faq-item">
                    <summary class="faq-item__question">{faq["question"]}</summary>
                    <div class="faq-item__answer"><p>{faq["answer"]}</p></div>
                </details>'''

    faq_schema = {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["answer"]
                }
            }
            for faq in faqs
        ]
    }

    html = f'''
        <section class="section faq-section">
            <div class="container">
                <h2 class="section__title">{heading}</h2>
                {faq_items_html}
            </div>
        </section>'''

    return html, faq_schema


# =============================================================================
# NEWSLETTER SIGNUP
# =============================================================================

def generate_newsletter_signup(category=None, state=None, formspree_id=""):
    """Generate contextual newsletter signup section.

    Args:
        category: Category name for contextual copy (optional)
        state: State name for contextual copy (optional)
        formspree_id: Formspree form ID
    """
    if category and state:
        heading = f"Get {category} updates in {state}"
        subtext = f"New {category.lower()} vendors, regulatory changes, and industry news for {state} operators."
    elif category:
        heading = f"Get {category} industry updates"
        subtext = f"New vendors, compliance changes, and insights for cannabis {category.lower()} services."
    elif state:
        heading = f"Get {state} cannabis industry updates"
        subtext = f"New listings, regulatory changes, and industry news for {state} operators."
    else:
        heading = "Stay in the loop"
        subtext = "New vendors, regulatory changes, and industry news. Weekly, no spam."

    action = f"https://formspree.io/f/{formspree_id}" if formspree_id else "#"

    return f'''
        <section class="section newsletter-section">
            <div class="container">
                <div class="newsletter-box">
                    <h2 class="newsletter-box__title">{heading}</h2>
                    <p class="newsletter-box__text">{subtext}</p>
                    <form class="newsletter-form" action="{action}" method="POST">
                        <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
                        <div class="newsletter-form__row">
                            <input class="newsletter-form__input" type="email" name="email" placeholder="you@company.com" required>
                            <button type="submit" class="btn btn--primary newsletter-form__btn">Subscribe</button>
                        </div>
                    </form>
                </div>
            </div>
        </section>'''


# =============================================================================
# CLAIM CTA
# =============================================================================

def generate_claim_cta(listing_name=None, formspree_id=""):
    """Generate 'Claim This Listing' CTA box.

    Args:
        listing_name: Business name for contextual copy
        formspree_id: Formspree form ID
    """
    if listing_name:
        heading = f"Is this your business?"
        subtext = f"Claim {listing_name} to update your information, add your logo, and get featured placement."
    else:
        heading = "Own a cannabis service business?"
        subtext = "Claim your free listing to update your information, add your logo, and get in front of cannabis operators."

    action = f"https://formspree.io/f/{formspree_id}" if formspree_id else "#"

    return f'''
        <section class="section claim-section">
            <div class="container">
                <div class="claim-box">
                    <h2 class="claim-box__title">{heading}</h2>
                    <p class="claim-box__text">{subtext}</p>
                    <a href="{action}" class="btn btn--primary">Claim This Listing</a>
                </div>
            </div>
        </section>'''


# =============================================================================
# CTA SECTION
# =============================================================================

def generate_cta_section(title="Find the service providers you need",
                         text="Browse 18 categories of cannabis ancillary services across every legal state.",
                         button_text=None, button_href=None,
                         include_form=False, formspree_id=""):
    """Generate CTA section with button or form.

    Args:
        title: CTA heading
        text: CTA description
        button_text: Button label (defaults to CTA_LABEL)
        button_href: Button URL (defaults to CTA_HREF)
        include_form: If True, render a contact form
        formspree_id: Formspree form ID for the action URL
    """
    btn_text = button_text or CTA_LABEL
    btn_href = button_href or CTA_HREF

    if include_form and formspree_id:
        action_url = f"https://formspree.io/f/{formspree_id}"
        inner = f'''
                <form class="form" action="{action_url}" method="POST">
                    <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
                    <div class="form__row">
                        <div class="form__group">
                            <label class="form__label" for="cta-name">Name</label>
                            <input class="form__input" type="text" id="cta-name" name="name" required>
                        </div>
                        <div class="form__group">
                            <label class="form__label" for="cta-email">Email</label>
                            <input class="form__input" type="email" id="cta-email" name="email" required>
                        </div>
                    </div>
                    <div class="form__group">
                        <label class="form__label" for="cta-company">Company</label>
                        <input class="form__input" type="text" id="cta-company" name="company">
                    </div>
                    <div class="form__group">
                        <label class="form__label" for="cta-message">Tell us about your business</label>
                        <textarea class="form__textarea" id="cta-message" name="message" rows="3"></textarea>
                    </div>
                    <button type="submit" class="btn btn--primary btn--lg form__submit">{btn_text}</button>
                </form>'''
    else:
        inner = f'''
                <a href="{btn_href}" class="btn btn--primary btn--lg">{btn_text}</a>'''

    return f'''
        <section class="section cta-section">
            <div class="container">
                <div class="cta-section__header">
                    <h2 class="cta-section__title">{title}</h2>
                    <p class="cta-section__text">{text}</p>
                </div>
                {inner}
            </div>
        </section>'''


# =============================================================================
# CARDS & BADGES
# =============================================================================

def generate_category_badge(category_name, category_color="#3AA882"):
    """Generate a category badge.

    Args:
        category_name: Display name
        category_color: Hex color for badge
    """
    return f'<span class="badge badge--category" style="--badge-color: {category_color}">{category_name}</span>'


def generate_state_badge(state_abbrev, legal_status="recreational"):
    """Generate a state badge.

    Args:
        state_abbrev: 2-letter state abbreviation
        legal_status: recreational, medical, or decriminalized
    """
    status_class = f"badge--{legal_status}" if legal_status else "badge--state"
    return f'<span class="badge {status_class}">{state_abbrev}</span>'


def generate_listing_card(listing, categories_lookup=None):
    """Generate a listing card.

    Args:
        listing: Dict with listing data
        categories_lookup: Dict of slug -> category data for badge colors
    """
    name = listing.get("name", "Unknown")
    city = listing.get("city", "")
    state = listing.get("state", "")
    slug = listing.get("slug", "")
    category = listing.get("category", "")
    license_status = listing.get("license_status", "")
    description = listing.get("description", "")

    location = f"{city}, {state}" if city and state else state or city

    cat_color = "#3AA882"
    cat_name = category.replace("-", " ").title()
    if categories_lookup and category in categories_lookup:
        cat_color = categories_lookup[category].get("color", cat_color)
        cat_name = categories_lookup[category].get("name", cat_name)

    badge_html = generate_category_badge(cat_name, cat_color)

    status_html = ""
    if license_status:
        status_cls = "license-status--active" if license_status == "active" else "license-status--inactive"
        status_html = f'<span class="license-status {status_cls}">{license_status.title()}</span>'

    desc_truncated = description[:120] + "..." if len(description) > 120 else description

    return f'''<a href="/listing/{slug}/" class="listing-card">
            <div class="listing-card__header">
                <h3 class="listing-card__name">{name}</h3>
                {status_html}
            </div>
            <p class="listing-card__location">{location}</p>
            <p class="listing-card__desc">{desc_truncated}</p>
            <div class="listing-card__footer">
                {badge_html}
            </div>
        </a>'''


CATEGORY_ICONS = {
    "flask": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6M10 3v6.5L4.5 19.5a1 1 0 0 0 .87 1.5h13.26a1 1 0 0 0 .87-1.5L14 9.5V3"/><path d="M8.5 14h7"/></svg>',
    "clipboard-check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/><path d="m9 14 2 2 4-4"/></svg>',
    "scale": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18"/><path d="M4 7h16"/><path d="M4 7l3 7a4 4 0 0 0 4-3"/><path d="M20 7l-3 7a4 4 0 0 1-4-3"/><path d="m4 14 3.5-1"/><path d="m20 14-3.5-1"/></svg>',
    "package": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="m16.5 9.4-9-5.19"/><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><path d="M3.27 6.96 12 12.01l8.73-5.05"/><path d="M12 22.08V12"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
    "thermometer": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/></svg>',
    "lightbulb": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>',
    "umbrella": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 19a3 3 0 0 1-6 0"/><path d="M12 2v1"/><path d="M12 3a9 9 0 0 1 9 9H3a9 9 0 0 1 9-9z"/><path d="M12 12v7"/></svg>',
    "calculator": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8"/><path d="M8 10h8"/><path d="M8 14h4"/><path d="M8 18h4"/><path d="M16 14h.01"/><path d="M16 18h.01"/></svg>',
    "building": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22V12h6v10"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M16 10h.01"/></svg>',
    "monitor": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/></svg>',
    "megaphone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="m3 11 18-5v12L3 13v-2z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 18H3V7a1 1 0 0 1 1-1h9v12"/><path d="M14 9h4l4 4v5h-2"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/></svg>',
    "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "bank": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"/><path d="M3 10h18"/><path d="M12 3l9 7H3l9-7z"/><path d="M5 10v8"/><path d="M9 10v8"/><path d="M15 10v8"/><path d="M19 10v8"/></svg>',
    "recycle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5"/><path d="M11 19h8.203a1.83 1.83 0 0 0 1.556-.89 1.784 1.784 0 0 0 0-1.775l-1.226-2.12"/><path d="m14 16-3 3 3 3"/><path d="M8.293 13.596 4.875 7.97a1.83 1.83 0 0 1 .009-1.784A1.784 1.784 0 0 1 6.44 5.4h5.4"/><path d="m7 9 1-4.5L12.5 7"/><path d="M15.707 13.596 19.125 7.97"/><path d="m17 4-3.5 2L16 9"/></svg>',
    "hammer": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="m15 12-8.5 8.5a2.12 2.12 0 1 1-3-3L12 9"/><path d="M17.64 15 22 10.64"/><path d="m20.91 11.7-1.25-1.25c-.6-.6-.93-1.4-.93-2.25V6.5a.5.5 0 0 0-.5-.5H16.5a.5.5 0 0 1-.5-.5V4.2c0-.85.33-1.65.93-2.25L18 .88"/></svg>',
    "briefcase": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/><path d="M12 12v.01"/></svg>',
}


def generate_category_card(category):
    """Generate a category card for the homepage/category index.

    Args:
        category: Dict with category data from categories.json
    """
    name = category.get("name", "")
    slug = category.get("slug", "")
    description = category.get("description", "")
    color = category.get("color", "#3AA882")
    icon_key = category.get("icon", "")

    desc_short = description[:100] + "..." if len(description) > 100 else description
    icon_svg = CATEGORY_ICONS.get(icon_key, CATEGORY_ICONS.get("briefcase", ""))

    return f'''<a href="/categories/{slug}/" class="category-card" style="--card-accent: {color}">
            <div class="category-card__icon" style="background: {color}20; border-color: {color}40; color: {color}">
                {icon_svg}
            </div>
            <h3 class="category-card__name">{name}</h3>
            <p class="category-card__desc">{desc_short}</p>
        </a>'''


def generate_state_card(state, listing_count=0):
    """Generate a state card for the homepage/state index.

    Args:
        state: Dict with state data from states.json
        listing_count: Number of listings in this state
    """
    name = state.get("name", "")
    slug = state.get("slug", "")
    abbrev = state.get("abbrev", "")
    legal_status = state.get("legal_status", "")

    status_badge = generate_state_badge(legal_status.title(), legal_status)
    count_text = f"{listing_count} listing{'s' if listing_count != 1 else ''}" if listing_count > 0 else "Coming soon"

    return f'''<a href="/states/{slug}/" class="state-card">
            <div class="state-card__header">
                <span class="state-card__abbrev">{abbrev}</span>
                {status_badge}
            </div>
            <h3 class="state-card__name">{name}</h3>
            <p class="state-card__count">{count_text}</p>
        </a>'''


# =============================================================================
# RELATED LINKS
# =============================================================================

def generate_related_links(links, heading="Related Pages"):
    """Generate related links section.

    Args:
        links: List of dicts with 'href' and 'label' keys
        heading: Section heading
    """
    if not links:
        return ""

    links_html = ""
    for link in links:
        links_html += f'<li><a href="{link["href"]}">{link["label"]}</a></li>\n'

    return f'''
        <section class="section related-section">
            <div class="container">
                <h2 class="section__title">{heading}</h2>
                <ul class="related-links">
                    {links_html}
                </ul>
            </div>
        </section>'''


# =============================================================================
# PAGE WRAPPER
# =============================================================================

def get_page_wrapper(title, description, canonical_path, body_content,
                     active_page=None, extra_schema="", noindex=False,
                     og_type="website"):
    """Generate a complete HTML page by combining head, nav, content, footer.

    Args:
        title: Page title for <title> tag
        description: Meta description
        canonical_path: Path for canonical URL, e.g. "/states/california/"
        body_content: Inner HTML content (sections, etc.)
        active_page: Nav item to highlight, e.g. "/categories/"
        extra_schema: Additional JSON-LD schema script tags
        noindex: If True, add robots noindex
        og_type: Open Graph type

    Returns:
        Complete HTML page as string
    """
    head = get_html_head(title, description, canonical_path, extra_schema,
                         noindex=noindex, og_type=og_type)
    nav = get_nav_html(active_page)
    footer = get_footer_html()

    return f'''{head}
{nav}

{body_content}

{footer}'''


# =============================================================================
# FILE WRITER
# =============================================================================

def write_page(path, html):
    """Write an HTML page to disk, creating directories as needed.

    Args:
        path: Relative file path from project root, e.g. "states/california/index.html"
        html: Complete HTML content string
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(project_root, path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(html)

    print(f"  Generated: /{path}")
