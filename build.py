#!/usr/bin/env python3
"""Builds the static pages from shared parts. Run: python3 build.py
Home page body lives in src/home.html. Service pages are defined below."""
import json, html

SITE = "https://www.avanttotalsolutions.com"
PHONE = "410-357-1406"

SERVICES = [
    ("masonry", "Masonry", "Brick, stone, tuckpointing and facades"),
    ("concrete-restoration", "Concrete restoration", "Spall repair, steps, sidewalks and ADA ramps"),
    ("hoist-manpower", "Hoist manpower", "Local 542 trained operators for your hoist"),
    ("procurement", "Procurement", "Materials and rentals, sourced and delivered"),
    ("post-construction-cleaning", "Post-construction cleaning", "Rough, final and touch-up cleans"),
]

ICONS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="arrow" viewBox="0 0 20 20"><path d="M3 10h13M11 4.5l5.5 5.5-5.5 5.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="left" viewBox="0 0 20 20"><path d="M17 10H4M9 4.5 3.5 10 9 15.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="pause" viewBox="0 0 16 16"><path d="M4 2.5h2.5v11H4zM9.5 2.5H12v11H9.5z" fill="currentColor"/></symbol>
  <symbol id="play" viewBox="0 0 16 16"><path d="M4 2.5l9.5 5.5L4 13.5z" fill="currentColor"/></symbol>
</svg>"""

ARROW = '<svg class="arrow"><use href="#arrow"/></svg>'

BUSINESS = {
    "@type": "HomeAndConstructionBusiness",
    "@id": SITE + "/#business",
    "name": "Avant Total Solutions",
    "url": SITE + "/",
    "logo": SITE + "/assets/img/logo-stacked.png",
    "image": SITE + "/assets/video/hero.jpg",
    "telephone": "+1-410-357-1406",
    "email": "hello@avanttotalsolutions.com",
    "address": {"@type": "PostalAddress", "streetAddress": "409 Chester Avenue", "addressLocality": "Annapolis", "addressRegion": "MD", "postalCode": "21403", "addressCountry": "US"},
    "areaServed": ["Maryland", "Pennsylvania", "New Jersey", "Delaware"],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:00", "closes": "16:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "14:00"},
    ],
    "sameAs": ["https://www.linkedin.com/company/avant-total-solutions/", "https://www.instagram.com/at.solutions__"],
}


def head(title, desc, path, image, jsonld, preload=None):
    canon = SITE + "/" + path
    pre = f'\n<link rel="preload" as="image" href="{preload}">' if preload else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Avant Total Solutions">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#01122a">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@500;600;700;800&family=Figtree:wght@400;500;600;700&display=swap">{pre}
<link rel="stylesheet" href="assets/css/site.css">
<script>document.documentElement.classList.add('js');</script>
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@graph": jsonld}, indent=1)}
</script>
</head>
<body>
{ICONS}
<a class="skip" href="#main">Skip to content</a>
"""


def header(current=None, home=False):
    h = "" if home else "./"
    dd = "".join(
        f'<a href="{slug}.html"{" aria-current=\"page\"" if slug == current else ""}><b>{name}</b><small>{blurb}</small></a>'
        for slug, name, blurb in SERVICES)
    sub = "".join(f'<a href="{slug}.html">{name}</a>' for slug, name, _ in SERVICES)
    return f"""
<header class="site-header" id="header">
  <div class="wrap">
    <a class="brand" href="{'#top' if home else './'}" aria-label="Avant Total Solutions home"><img src="assets/img/logo-horizontal.png" alt="Avant Total Solutions" width="375" height="115"></a>
    <nav class="nav" aria-label="Main">
      <div class="nav-dd" id="nav-dd" data-open="false">
        <button type="button" id="nav-dd-btn" aria-expanded="false" aria-controls="dd-panel">Services</button>
        <div class="dd-panel" id="dd-panel">{dd}<a class="all" href="{h}#services">All services</a></div>
      </div>
      <a href="{h}#about">About</a>
      <a href="{h}#work">Our work</a>
      <a href="{h}#area">Service area</a>
      <a href="{h}#faq">FAQ</a>
    </nav>
    <div class="header-actions">
      <a class="header-phone" href="tel:+14103571406">{PHONE}</a>
      <a class="btn btn-amber" href="{h}#quote">Get a free quote</a>
      <button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>

<div class="mobile-menu dark" id="mobile-menu" aria-hidden="true">
  <div class="wrap">
    <nav aria-label="Mobile">
      <a href="{h}#services">Services</a>
      <div class="sub">{sub}</div>
      <a href="{h}#about">About</a>
      <a href="{h}#work">Our work</a>
      <a href="{h}#area">Service area</a>
      <a href="{h}#faq">FAQ</a>
    </nav>
    <div class="contact-row">
      <a class="btn btn-amber" href="{h}#quote">Get a free quote</a>
      <a class="btn btn-ghost" href="tel:+14103571406">Call or text {PHONE}</a>
    </div>
  </div>
</div>
"""


def footer(home=False):
    h = "" if home else "./"
    svc = "".join(f'<li><a href="{slug}.html">{name}</a></li>' for slug, name, _ in SERVICES)
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <div class="wm"><img src="assets/img/logo-mark.png" alt="" width="116" height="116"><div><b>AVANT</b><small>TOTAL SOLUTIONS</small></div></div>
        <p>Woman and minority owned contractor based in Annapolis, serving Maryland, Pennsylvania, New Jersey and Delaware.</p>
        <div class="licenses"><span>MHIC # <span class="pending">pending</span></span><span>PA HIC # <span class="pending">pending</span></span></div>
      </div>
      <div><h4>Services</h4><ul>{svc}</ul></div>
      <div><h4>Company</h4><ul><li><a href="{h}#about">About</a></li><li><a href="{h}#work">Our work</a></li><li><a href="{h}#area">Service area</a></li><li><a href="{h}#faq">FAQ</a></li><li><a href="{h}#top">Privacy policy</a></li></ul></div>
      <div><h4>Contact</h4><ul><li><a href="tel:+14103571406">{PHONE}</a></li><li><a href="mailto:hello@avanttotalsolutions.com">hello@avanttotalsolutions.com</a></li><li><a href="https://www.linkedin.com/company/avant-total-solutions/">LinkedIn</a></li><li><a href="https://www.instagram.com/at.solutions__">Instagram</a></li></ul></div>
    </div>
    <div class="foot-legal"><span>© 2026 Avant Total Solutions</span><span>409 Chester Avenue, Annapolis, MD 21403</span></div>
  </div>
</footer>

<script src="assets/js/site.js"></script>
</body>
</html>
"""


def faq_block(faqs, heading="Questions about this service"):
    items = "".join(f'<details><summary>{q}<span class="pl" aria-hidden="true"></span></summary><p class="ans">{a}</p></details>' for q, a in faqs)
    return f"""
  <section class="faq-sec mist-bg" aria-labelledby="faq-title" style="background: var(--mist)">
    <div class="wrap">
      <div class="head">
        <span class="label">Questions</span>
        <h2 id="faq-title">{heading}</h2>
        <p class="lede">If your question isn't here, call or text and you'll get a straight answer.</p>
        <div><a class="btn btn-ghost" href="tel:+14103571406">Call or text {PHONE}</a></div>
      </div>
      <div class="faq">{items}</div>
    </div>
  </section>"""


def compare_block(pairs, heading):
    first = pairs[0]
    tabs = "".join(
        f'<button role="tab" aria-selected="{"true" if i == 0 else "false"}"{"" if i == 0 else " tabindex=\"-1\""} data-b="{p["b"]}" data-a="{p["a"]}" data-cap="{p["cap"]}" data-tags="{p["tags"]}">{p["name"]}</button>'
        for i, p in enumerate(pairs))
    tags = "".join(f"<span>{t}</span>" for t in first["tags"].split("|"))
    tablist = f'<div class="ba-tabs" role="tablist" aria-label="Choose a project" id="ba-tabs">{tabs}</div>' if len(pairs) > 1 else ""
    return f"""
  <section class="ba" id="work" aria-labelledby="work-title" style="padding-bottom: clamp(4rem, 8vw, 6.5rem)">
    <div class="wrap">
      <div class="ba-head">
        <div class="head-text"><span class="label">Before and after</span><h2 id="work-title">{heading}</h2></div>
        {tablist}
      </div>
      <div class="compare" id="compare" style="--pos: 50%">
        <img class="before" id="ba-before" src="{first['b']}" alt="Before: {first['cap']}">
        <div class="after-wrap"><img id="ba-after" src="{first['a']}" alt="After: {first['cap']}"></div>
        <span class="tag-b">Before</span><span class="tag-a">After</span>
        <input type="range" min="0" max="100" value="50" id="compare-range" aria-label="Slide to compare before and after">
        <span class="handle" aria-hidden="true"><span class="grip"><svg><use href="#left"/></svg><svg><use href="#arrow"/></svg></span></span>
      </div>
      <div class="ba-cap"><p id="ba-cap">{first['cap']}</p><div class="ba-tags" id="ba-tags">{tags}</div></div>
    </div>
  </section>"""


def scope_block(groups, heading, lede=""):
    secs = "".join(f'<section><h3>{g}</h3><ul>{"".join(f"<li>{i}</li>" for i in items)}</ul></section>' for g, items in groups)
    lede_html = f'<p class="lede">{lede}</p>' if lede else ""
    return f"""
  <section class="sp" aria-labelledby="scope-title">
    <div class="wrap">
      <div class="sp-head"><span class="label">What's included</span><h2 id="scope-title">{heading}</h2>{lede_html}</div>
      <div class="scope-groups">{secs}</div>
    </div>
  </section>"""


def steps_block(steps, heading):
    lis = "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in steps)
    cols = len(steps)
    return f"""
  <section class="process" aria-labelledby="process-title">
    <div class="wrap">
      <div class="head"><span class="label">How it works</span><h2 id="process-title">{heading}</h2></div>
      <ol class="steps{" three" if cols == 3 else ""}">{lis}</ol>
    </div>
  </section>"""


def related_block(slugs):
    imgs = {"masonry": "assets/photo/veneer-closeup.webp", "concrete-restoration": "assets/photo/barn-floor-clean.webp",
            "hoist-manpower": "assets/video/hoist.jpg", "procurement": "assets/video/delivery.jpg",
            "post-construction-cleaning": "assets/photo/finished-interior.webp"}
    lookup = {s: (n, b) for s, n, b in SERVICES}
    cards = "".join(f'<a href="{s}.html"><img src="{imgs[s]}" alt="" loading="lazy"><b>{lookup[s][0]}</b><span>{lookup[s][1]}</span></a>' for s in slugs)
    return f"""
  <section class="sp" aria-labelledby="related-title">
    <div class="wrap">
      <div class="sp-head"><span class="label">Often paired with</span><h2 id="related-title">One crew for the next step too</h2></div>
      <div class="related">{cards}</div>
    </div>
  </section>"""


def cta_block(service, line):
    q = service.replace(" ", "+")
    return f"""
  <section class="cta-band dark" aria-label="Request a quote">
    <div class="wrap">
      <h2>{line}</h2>
      <div class="acts">
        <a class="btn btn-amber" href="./?service={q}#quote">Get a free quote {ARROW}</a>
        <a class="btn btn-ghost" href="tel:+14103571406">Call or text {PHONE}</a>
      </div>
    </div>
  </section>"""


def page_hero(name, h1, lede, media, service):
    q = service.replace(" ", "+")
    if media.endswith(".mp4"):
        poster = media.replace(".mp4", ".jpg")
        m = f'<img class="bgimg" src="{poster}" alt="" aria-hidden="true"><video autoplay muted loop playsinline preload="metadata" poster="{poster}" aria-hidden="true"><source src="{media}" type="video/mp4"></video>'
    else:
        m = f'<img class="bgimg" src="{media}" alt="" aria-hidden="true">'
    return f"""
  <section class="page-hero dark" id="top" aria-labelledby="page-title">
    {m}
    <div class="wrap">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="./">Home</a><span aria-hidden="true">/</span><a href="./#services">Services</a><span aria-hidden="true">/</span><span>{name}</span></nav>
      <h1 id="page-title">{h1}</h1>
      <p class="lede">{lede}</p>
      <div class="hero-actions">
        <a class="btn btn-amber" href="./?service={q}#quote">Get a free quote {ARROW}</a>
        <a class="btn btn-ghost" href="tel:+14103571406">Call or text {PHONE}</a>
      </div>
      <div class="hero-foot"><span><b>MHIC #</b> <span class="pending">pending</span></span><span><b>PA HIC #</b> <span class="pending">pending</span></span><span>Licensed and insured</span><span>Serving MD, PA, NJ and DE</span></div>
    </div>
  </section>"""


def split_block(label, heading, paras, img, alt):
    ps = "".join(f'<p{" class=\"big\"" if i == 0 else ""}>{p}</p>' for i, p in enumerate(paras))
    return f"""
  <section class="sp" aria-labelledby="intro-title">
    <div class="wrap split">
      <div class="copy"><span class="label">{label}</span><h2 id="intro-title">{heading}</h2>{ps}</div>
      <figure><img src="{img}" alt="{alt}" loading="lazy"></figure>
    </div>
  </section>"""


def signs_block(label, heading, signs, note):
    lis = "".join(f"<li><b>{t}</b><span>{d}</span></li>" for t, d in signs)
    return f"""
  <section class="sp" aria-labelledby="signs-title" style="padding-top: 0">
    <div class="wrap">
      <div class="sp-head"><span class="label">{label}</span><h2 id="signs-title">{heading}</h2><p class="lede">{note}</p></div>
      <ul class="signs{" four" if len(signs) == 4 else ""}">{lis}</ul>
    </div>
  </section>"""


def jsonld_service(slug, name, desc, faqs):
    url = f"{SITE}/{slug}"
    return [
        BUSINESS,
        {"@type": "Service", "@id": url + "#service", "name": name, "description": desc, "url": url,
         "provider": {"@id": SITE + "/#business"}, "areaServed": ["Maryland", "Pennsylvania", "New Jersey", "Delaware"]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in faqs]},
    ]


PAIRS = {
    "wall": {"name": "Retaining wall", "b": "assets/photo/wall-before.webp", "a": "assets/photo/wall-after.webp",
             "cap": "Failing block retaining wall refaced in red brick, with a soldier course cap and end piers", "tags": "Masonry|Retaining wall"},
    "window": {"name": "Window infill", "b": "assets/photo/window-before.webp", "a": "assets/photo/window-after.webp",
               "cap": "Window opening infilled with brick and mortar matched to the existing wall", "tags": "Masonry|Brick matching"},
    "stoop": {"name": "Herringbone stoop", "b": "assets/photo/stoop-before.webp", "a": "assets/photo/stoop-after.webp",
              "cap": "Stoop rebuilt with a herringbone brick inlay inside a concrete border", "tags": "Concrete restoration|Masonry"},
}

PAGES = []

# ---------- Masonry ----------
m_faqs = [
    ("Is the estimate free?", "Yes. We visit the property, look at the wall up close, take measurements and send an itemized quote with no obligation."),
    ("Can you match my existing brick and mortar?", "Usually, yes. Our suppliers carry hard-to-find brick and stone, including matches for older rowhomes, and we mix mortar to match the color and joint profile of the wall around the repair."),
    ("How long will my project take?", "It depends on size, access and weather. Your quote includes an estimated schedule, and you'll hear from us if weather moves a date."),
    ("Do you handle permits?", "When a permit is required, we help you through the process and make sure the work meets local code."),
    ("Can masonry be done in cold or wet weather?", "Mortar needs the right temperature and moisture to cure properly. If freezing temperatures or heavy rain would compromise the work, we reschedule and tell you right away."),
    ("Do you warranty your masonry work?", "Yes. Masonry projects carry a workmanship warranty. If an issue with our work comes up during the warranty period, we come back and fix it at no cost to you."),
]
PAGES.append(dict(
    slug="masonry", name="Masonry", service="Masonry",
    title="Masonry, Tuckpointing and Brick Repair | Avant Total Solutions",
    desc="Brick and stone repair, tuckpointing, facade restoration, retaining walls and new masonry by a Local 1 trained crew. Serving MD, PA, NJ and DE. Free itemized quotes.",
    image="assets/video/masonry.jpg",
    body=lambda: page_hero("Masonry", "Brick and stone masonry",
        "New work and repair on rowhomes, houses and commercial buildings, set by a crew trained in BAC Local 1. We match existing brick and mortar so a repair blends into the wall around it.",
        "assets/video/masonry.mp4", "Masonry")
    + split_block("Why it matters", "Repairs that disappear into the wall",
        ["Most masonry problems start small: a crumbling joint, a loose brick, a stain that keeps coming back. Caught early, they're a repair. Left alone, they become a rebuild.",
         "Jimmy Harris walks every masonry job before it's quoted. You get an itemized estimate that says exactly which courses, joints and materials are included, and a crew that leaves the site cleaner than they found it."],
        "assets/photo/veneer-closeup.webp", "Mason setting dark brick veneer against new block")
    + scope_block([
        ("Brick and block", ["Bricklaying and stone masonry", "Brick veneer over CMU", "Tuckpointing and repointing", "Chimney rebuilds and repair"]),
        ("Restoration", ["Facade restoration", "Mortar joint repair", "Brick and stone matching", "Historic masonry repair", "Cleaning and sealing"]),
        ("Outdoor", ["Retaining and garden walls", "Patios and paver walkways", "Steps and stoops", "Entry columns and mailboxes"]),
    ], "Masonry we build and repair", "Don't see your project here? If it's brick, block or stone, ask.")
    + compare_block([PAIRS["wall"], PAIRS["window"]], "Masonry we've finished")
    + signs_block("Signs it's time", "When to call a mason", [
        ("Crumbling mortar joints", "Joints you can scratch out with a key let water into the wall behind them."),
        ("Loose or missing brick", "Gaps let water in and weaken the courses around them."),
        ("Spalling", "Brick faces flaking or popping off usually means trapped moisture and freeze damage."),
        ("Water staining", "White streaks or dark patches point to water moving through the masonry."),
        ("Leaning or bulging walls", "Retaining and garden walls that move need attention before they fail."),
        ("Gaps at windows and steps", "Separation between brick and other materials lets water reach the structure."),
    ], "Small problems get expensive when water gets behind the face of the wall. If you see any of these, have it looked at.")
    + steps_block([
        ("Tell us about the project", "Call, text or send the form with photos if you have them."),
        ("Free site visit", "We look at the wall up close, take measurements and talk through options."),
        ("Itemized quote", "Scope, materials, schedule and price, line by line, with one point of contact."),
        ("Work and walkthrough", "We protect the property, do the work, clean up and walk it with you."),
    ], "From first call to final walkthrough")
    + related_block(["concrete-restoration", "procurement"])
    + faq_block(m_faqs, "Masonry questions")
    + cta_block("Masonry", "Have a wall, chimney or stoop that needs work?"),
    faqs=m_faqs))

# ---------- Concrete restoration ----------
c_faqs = [
    ("Should I repair or replace my concrete?", "If the slab is sound and the damage is on the surface, repair and resurfacing usually make sense. If it's heaved, sunk or cracked through, replacing that section is often the better value. We'll tell you which, and why, at the site visit."),
    ("Do you build ADA ramps and curb cuts?", "Yes. We build accessible ramps, curb cuts and pads for vertical platform lifts to the spec your project or municipality requires."),
    ("Can you match the finish on my block?", "Yes. We match broom, swirl and stamped finishes so new sections blend with the sidewalk or steps around them."),
    ("How soon can we use it?", "We give you exact times for your mix and the weather. As a rule, new concrete takes foot traffic after about a day and vehicles after about a week."),
    ("Is concrete work weather-dependent?", "Yes. Freezing temperatures and heavy rain affect curing, so we schedule pours around the forecast and tell you right away if a date moves."),
]
PAGES.append(dict(
    slug="concrete-restoration", name="Concrete restoration", service="Concrete restoration",
    title="Concrete Repair, Steps, Sidewalks and ADA Ramps | Avant Total Solutions",
    desc="Concrete restoration and new flatwork: spall and crack repair, step and stoop rebuilds, sidewalks, curb cuts and ADA ramps across MD, PA, NJ and DE. Free itemized quotes.",
    image="assets/photo/barn-floor-clean.webp",
    body=lambda: page_hero("Concrete restoration", "Concrete restoration and repair",
        "Spalled steps, cracked sidewalks and settled slabs repaired to last, plus new flatwork poured and finished to match the block.",
        "assets/photo/barn-floor-clean.webp", "Concrete restoration")
    + split_block("Why it matters", "Safe to walk on and built to last",
        ["Broken concrete is a trip hazard first and an eyesore second. The fix depends on what's happening underneath, so we look at the base before we quote the surface.",
         "Some jobs need a surface repair and a sealer. Others need a section cut out and poured new. Your estimate says which and why, with the finish spelled out so the new work matches what's next to it."],
        "assets/photo/stoop-before.webp", "Stoop being rebuilt with brick inside a concrete border")
    + scope_block([
        ("Repair", ["Spall and crack repair", "Resurfacing", "Joint repair", "Sealing and waterproofing"]),
        ("Rebuild", ["Step and stoop rebuilds", "Sidewalk replacement", "Curb cuts and ADA ramps", "Vertical platform lift pads"]),
        ("New flatwork", ["Slabs and pads", "Garage and basement floors", "Patios and walkways", "Broom, swirl and stamped finishes"]),
    ], "Concrete we repair and pour")
    + compare_block([PAIRS["stoop"]], "Concrete we've finished")
    + signs_block("Signs it's time", "When concrete needs attention", [
        ("Spalling or flaking", "The top layer breaking away exposes the concrete below to more damage."),
        ("Widening cracks", "Cracks that grow or let water in usually point to movement underneath."),
        ("Crumbling edges", "Step noses and curb edges that break off are a trip hazard."),
        ("Heaving or sinking", "Uneven sections create a lip that catches feet and wheels."),
        ("Rust stains", "Orange streaks can mean the steel inside is corroding."),
        ("Water pooling", "Standing water against a foundation means the slope has failed."),
    ], "Most concrete damage starts with water. Fixing it early usually costs less than replacing it later.")
    + steps_block([
        ("Tell us about the project", "Call, text or send the form with photos if you have them."),
        ("Free site visit", "We check the surface and the base, measure, and talk through repair or replace."),
        ("Itemized quote", "Scope, finish, schedule and price, line by line."),
        ("Pour and walkthrough", "We schedule around the forecast, finish to match and walk it with you."),
    ], "From first call to final walkthrough")
    + related_block(["masonry", "post-construction-cleaning"])
    + faq_block(c_faqs, "Concrete questions")
    + cta_block("Concrete restoration", "Have steps, a sidewalk or a slab that needs work?"),
    faqs=c_faqs))

# ---------- Hoist manpower ----------
h_faqs = [
    ("Do you supply the hoist?", "No. We supply trained operators only and you supply the hoist. If you need help finding hoist parts, safety gear or materials, our procurement team can source them."),
    ("Do you operate inside and outside hoists?", "Yes. Our operators run outside construction hoists along the structure and inside personnel and material elevators in the building core."),
    ("Are your operators union trained?", "Yes. Every operator is trained to union standards under Jimmy Harris, who holds active IUOE Local 542 certification."),
    ("How fast can you place an operator?", "In most cases within a few business days, depending on location and schedule. Call early to lock in your start date."),
    ("Can your operators handle busy, complex sites?", "Yes. Our operators work high-rise and multi-family sites where several trades call for lifts at once, and they coordinate with your supers by radio, hand signals or whatever your site uses."),
    ("How much does a hoist operator cost?", "Pricing depends on location, schedule, shift length and site requirements. You'll get a clear written rate with no hidden fees."),
]
PAGES.append(dict(
    slug="hoist-manpower", name="Hoist manpower", service="Hoist manpower",
    title="Hoist Operators, Local 542 Trained | Avant Total Solutions",
    desc="Local 542 trained hoist operators for outside construction hoists and inside personnel and material elevators across MD, PA, NJ and DE. You supply the hoist, we supply the operator.",
    image="assets/video/hoist.jpg",
    body=lambda: page_hero("Hoist manpower", "Hoist operators for your site",
        "Local 542 trained operators for outside construction hoists and inside personnel and material elevators. You supply the hoist and we supply the operator.",
        "assets/video/hoist.mp4", "Hoist manpower")
    + split_block("Why it matters", "Your hoist sets the pace of the site",
        ["Every delivery, every material move and every personnel lift runs through the hoist. When the operator falls behind, so does every trade waiting on the car.",
         "Our operators are trained in the field by Jimmy Harris, a Local 542 hoist operator who has also laid brick with BAC Local 1. They know what's riding on each load and how to keep several trades moving at once."],
        "assets/photo/crew-handshake.webp", "Jimmy Harris with a site supervisor")
    + scope_block([
        ("Equipment we run", ["Outside construction hoists", "Inside personnel elevators", "Inside material elevators"]),
        ("Sites we work", ["High-rise construction", "Multi-family buildings", "Commercial and mixed-use projects"]),
        ("How we staff", ["Placement in a few business days", "Single shifts or full project duration", "One contact from mobilization to final lift"]),
    ], "What our operators cover")
    + signs_block("Safety", "How our operators protect your site", [
        ("Daily inspections", "Operators check the car, gates and controls at the start of every shift."),
        ("OSHA standards", "Every operator is trained to OSHA and union safety requirements."),
        ("Your site rules", "Operators follow your site-specific procedures from day one."),
        ("Constant communication", "Radios, hand signals or whatever your supers use, all shift long."),
    ], "Safety is the job. These are standard on every placement.")
    + steps_block([
        ("Call or send the form", "Tell us the site, the hoist type and your start date."),
        ("Confirm the details", "We confirm shifts, site rules and contacts."),
        ("Operator on site", "Your operator shows up ready, usually within a few business days."),
        ("One point of contact", "Questions or changes go to one person through the last lift."),
    ], "How placement works")
    + related_block(["procurement", "masonry"])
    + faq_block(h_faqs, "Hoist questions")
    + cta_block("Hoist manpower", "Need an operator on your hoist?"),
    faqs=h_faqs))

# ---------- Procurement ----------
p_faqs = [
    ("What can you source?", "Building materials like brick, block, CMU, stone, lumber, drywall and concrete products, plus equipment rentals, fixtures, finishes and furnishings."),
    ("Do you have preferred suppliers?", "Yes. We work with suppliers we know for consistent quality, fair pricing and on-time delivery. If you have a brand or supplier in mind, we can work with them too."),
    ("Can you handle rush orders?", "Whenever possible, yes. If you need something fast, we find the best available option and get it to your site as soon as we can."),
    ("Do you work with homeowners?", "Case by case. Most of our procurement work supports contractors and multi-unit projects, and we're glad to talk about large renovations or specialty finds."),
    ("How do I start?", "Call, text or send the form with what you need, quantities and your delivery date. We confirm specs and budget before we source anything."),
]
PAGES.append(dict(
    slug="procurement", name="Procurement", service="Procurement",
    title="Construction Procurement and Material Sourcing | Avant Total Solutions",
    desc="Building materials, equipment rentals, fixtures and finishes sourced and delivered on your schedule, with one point of contact. Serving contractors, developers and property managers in MD, PA, NJ and DE.",
    image="assets/video/delivery.jpg",
    body=lambda: page_hero("Procurement", "Construction procurement",
        "Materials, rentals and finishes sourced through suppliers we know and delivered on your schedule, with one point of contact from quote to drop-off.",
        "assets/video/delivery.mp4", "Procurement")
    + split_block("Why it matters", "One call instead of ten",
        ["Chasing quotes, lead times and delivery windows eats days your crew should spend building. Hand us the list and the date, and we handle the rest.",
         "Because we work the trades ourselves, we know what a spec actually needs and where a cheaper substitute will cost you later. You approve every option before anything is ordered."],
        "assets/video/delivery.jpg", "Boom truck setting a supersack of material at a job site")
    + scope_block([
        ("Building materials", ["Brick, block, CMU and stone", "Lumber and drywall", "Concrete products", "Brick matched to older buildings"]),
        ("Equipment rentals", ["Tools and small equipment", "Lifts", "Machinery for short or long terms"]),
        ("Finishes and furnishings", ["Lighting and hardware", "Cabinetry and flooring", "Contract-grade furniture", "Staging furniture and decor"]),
    ], "What we source")
    + steps_block([
        ("Share your needs", "Send the list, quantities, specs and delivery date by call, text or form."),
        ("We source options", "We price it through our suppliers and send you choices that fit spec, budget and timeline."),
        ("You approve, we deliver", "We order, schedule delivery and stay your single contact until it's on site."),
    ], "How procurement works")
    + related_block(["hoist-manpower", "masonry"])
    + faq_block(p_faqs, "Procurement questions")
    + cta_block("Procurement", "Have a materials list and a deadline?"),
    faqs=p_faqs))

# ---------- Post-construction cleaning ----------
pc_faqs = [
    ("Which cleaning phases do you offer?", "All three standard phases: rough clean during construction, final clean before turnover and touch-up clean before move-in or inspection. You can book one phase or all three."),
    ("Can you do a custom scope?", "Yes. If your job needs something outside the standard phases, tell us what it is and we'll scope and price it."),
    ("How do you schedule around my turnover date?", "Give us your inspection, turnover or move-in date and we schedule each phase back from it."),
    ("Do you clean after home renovations?", "Yes. Homeowners use our final and touch-up cleans after kitchen, bath and whole-house renovations."),
]
PAGES.append(dict(
    slug="post-construction-cleaning", name="Post-construction cleaning", service="Post-construction cleaning",
    title="Post-Construction Cleaning: Rough, Final and Touch-Up | Avant Total Solutions",
    desc="Rough, final and touch-up post-construction cleaning for contractors, developers, property managers and homeowners across MD, PA, NJ and DE. Scheduled around your turnover date.",
    image="assets/photo/finished-interior.webp",
    body=lambda: page_hero("Post-construction cleaning", "Post-construction cleaning",
        "Rough, final and touch-up cleans scheduled around your punch list, so the space is ready for inspection, turnover or move-in.",
        "assets/photo/finished-interior.webp", "Post-construction cleaning")
    + f"""
  <section class="sp mist" aria-labelledby="phases-title">
    <div class="wrap">
      <div class="sp-head"><span class="label">The three phases</span><h2 id="phases-title">Book one phase or all three</h2><p class="lede">These are the industry-standard phases. If your job needs something different, ask for a custom scope.</p></div>
      <div class="phases">
        <article class="phase"><span class="when">During construction</span><h3>Rough clean</h3><p>Clears the way after the heavy trades so finish work can start on a clean site.</p><ul><li>Debris and scrap removal</li><li>Packaging and material waste hauled out</li><li>Floors swept and work areas cleared</li></ul></article>
        <article class="phase"><span class="when">Before turnover</span><h3>Final clean</h3><p>The detailed clean that gets a space ready for the owner, tenant or inspector.</p><ul><li>Dust removed from walls, vents and fixtures</li><li>Windows, frames and sills cleaned</li><li>Labels, paint and adhesive residue removed</li><li>Floors cleaned for their material</li></ul></article>
        <article class="phase"><span class="when">Before move-in</span><h3>Touch-up clean</h3><p>A last pass for the dust and fingerprints that settle after the final clean.</p><ul><li>Settled dust removed</li><li>Fingerprints and smudges wiped</li><li>Last-minute trade marks cleaned</li></ul></article>
      </div>
    </div>
  </section>"""
    + split_block("Who we clean for", "Ready for inspection, turnover or move-in",
        ["General contractors and developers hand us the punch list and the date. Property managers call us between tenants. Homeowners call after a renovation.",
         "Whoever you are, you get one point of contact, a written scope that says what each phase includes, and a crew that works around trades still on site."],
        "assets/photo/finished-interior.webp", "Finished interior space ready for walkthrough")
    + steps_block([
        ("Tell us the date", "Share your inspection, turnover or move-in date and the size of the space."),
        ("Scope and quote", "We confirm which phases you need and send an itemized price."),
        ("Clean and walkthrough", "We clean to the scope and walk it with you before turnover."),
    ], "How it works")
    + related_block(["concrete-restoration", "procurement"])
    + faq_block(pc_faqs, "Cleaning questions")
    + cta_block("Post-construction cleaning", "Have a turnover date coming up?"),
    faqs=pc_faqs))


def build():
    # Home
    main = open("src/home.html").read()
    home_ld = [BUSINESS, {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "Avant Total Solutions"}]
    out = head("Avant Total Solutions | Masonry, Concrete, Hoist Manpower and Cleaning",
               "Masonry, concrete restoration, Local 542 hoist operators, procurement and post-construction cleaning across Maryland, Pennsylvania, New Jersey and Delaware. Free itemized quotes.",
               "", "assets/video/hero.jpg", home_ld, preload="assets/video/hero.jpg") + header(home=True) + "\n" + main + "\n" + footer(home=True)
    open("index.html", "w").write(out)
    urls = [SITE + "/"]
    for p in PAGES:
        out = head(p["title"], p["desc"], p["slug"], p["image"], jsonld_service(p["slug"], p["name"], p["desc"], p["faqs"])) \
            + header(current=p["slug"]) + '\n<main id="main">' + p["body"]() + "\n</main>\n" + footer()
        open(p["slug"] + ".html", "w").write(out)
        urls.append(f"{SITE}/{p['slug']}")
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    open("sitemap.xml", "w").write(sm)
    open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print("built", len(urls), "pages")


if __name__ == "__main__":
    build()
