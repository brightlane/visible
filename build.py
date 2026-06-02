from pathlib import Path
from datetime import date
from html import escape
import json

ROOT = Path(".")
TODAY = date.today().isoformat()

SITE = {
    "name": "Visible USA Offer",
    "base_url": "https://brightlane.github.io/visible",
    "brand_name": "Visible",
    "official_url": "https://www.visible.com/",
    "affiliate_url": "https://convert.ctypy.com/aff_c?offer_id=29563&aff_id=21885",
    "locale": "en-US",
    "country": "US",
    "description": "A data-driven Visible affiliate site for USA visitors."
}
AFF_URL = SITE["affiliate_url"]

HUBS = [
    {"slug": "review", "title": "Visible Review", "description": "A practical review of Visible for USA visitors."},
    {"slug": "faq", "title": "Visible FAQ", "description": "Answers to common Visible questions."},
    {"slug": "alternatives", "title": "Visible Alternatives", "description": "Other wireless options compared with Visible."},
    {"slug": "guide", "title": "Wireless Guides", "description": "Practical wireless plans and usage guides."},
    {"slug": "best", "title": "Best Wireless Picks", "description": "Best-of pages by budget, speed, and usage goal."},
    {"slug": "coverage", "title": "Coverage Pages", "description": "Pages focused on coverage and network questions."},
    {"slug": "deals", "title": "Deal Pages", "description": "Promotional and savings-focused pages."},
    {"slug": "switch", "title": "Switching Pages", "description": "Pages for people changing carriers."},
    {"slug": "data", "title": "Data Plan Pages", "description": "Pages focused on data usage and plan fit."}
]

HOME = {
    "title": "Visible USA Offer | Simple Wireless for USA Visitors",
    "description": "Discover Visible for USA visitors. Simple wireless plans, straightforward pricing, and an easy online signup flow.",
    "h1": "Visible for USA Visitors Who Want Simple Wireless",
    "hero_badge": "Simple plans • Easy signup • USA-only promo",
    "hero_lead": "If you want a wireless plan that feels simple, modern, and easy to manage, Visible is built for that. It keeps the pitch straightforward and makes the offer easy to understand fast."
}

FAQS = [
    ("What is Visible?", "Visible is a wireless service focused on simple plans, online management, and straightforward pricing."),
    ("Who is Visible best for?", "Visible is a strong fit for people who want simple phone service, easy setup, and no-frills plan management."),
    ("Does Visible use a major network?", "Visible runs on Verizon's network ecosystem, which is a key reason many shoppers compare it for coverage."),
    ("Is this site for USA visitors only?", "Yes. The affiliate offer and page targeting are intended for USA visitors."),
    ("Can I switch to Visible easily?", "Many visitors use Visible when they want a simpler mobile plan and a straightforward online signup flow.")
]

PAGE_TYPES = ["best", "guide", "compare", "alternatives", "faq", "coverage", "deals", "switch", "data", "review"]
AUDIENCES = ["budget shoppers", "travelers", "families", "single-line users", "heavy data users", "light data users", "streamers", "remote workers", "seniors", "students"]
PROBLEMS = [
    "want a lower monthly phone bill",
    "need coverage confidence before switching",
    "want simple setup without store visits",
    "need enough data for streaming",
    "want a plan that is easy to manage",
    "are comparing carriers before porting a number",
    "want a no-frills wireless option",
    "need a clean mobile-first buying flow",
    "want to understand tradeoffs quickly",
    "want a plan that fits a specific budget"
]
ANGLES = ["price clarity", "coverage reassurance", "setup simplicity", "data fit", "switching confidence", "mobile convenience", "monthly predictability", "no-store buying", "decision speed", "plan matching"]
EVIDENCE = [
    "Visible positions itself around simple wireless service and online management.",
    "The page explains when the offer fits and when it may not.",
    "The content includes comparisons, caveats, and practical next steps.",
    "The FAQ addresses common purchase questions before the CTA."
]

CSS = """
:root{
  --bg:#07111f;--card:#101a2d;--text:#e5e7eb;--muted:#94a3b8;--line:#23314a;--accent:#22c55e;--shadow:0 24px 70px rgba(0,0,0,.35);--max:1160px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;font-family:Inter,Arial,sans-serif;
  background:linear-gradient(180deg,#07111f 0%,#08101d 100%);
  color:var(--text);line-height:1.6;
}
a{color:inherit;text-decoration:none}
.wrap{max-width:var(--max);margin:0 auto;padding:18px}
.nav{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}
.nav a{padding:8px 12px;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.03);color:#dbeafe}
.hero{border:1px solid var(--line);border-radius:28px;box-shadow:var(--shadow);overflow:hidden;background:linear-gradient(180deg, rgba(16,26,45,.98), rgba(10,18,34,.98))}
.hero-inner{display:grid;grid-template-columns:1.1fr .9fr;gap:24px;padding:34px;align-items:center}
h1{margin:12px 0 14px;font-size:clamp(2rem,5vw,4.25rem);line-height:1.02;letter-spacing:-.04em}
.lead{font-size:1.08rem;color:#cbd5e1;margin:0 0 22px;max-width:62ch}
.pill{display:inline-flex;align-items:center;gap:8px;border:1px solid rgba(34,197,94,.22);background:rgba(34,197,94,.1);color:#bbf7d0;padding:7px 12px;border-radius:999px;font-size:.86rem;font-weight:800}
.btns{display:flex;gap:12px;flex-wrap:wrap}
.btn{min-height:52px;padding:14px 20px;border-radius:16px;font-weight:900;display:inline-flex;align-items:center;justify-content:center;border:1px solid transparent}
.primary{background:linear-gradient(135deg,var(--accent),#16a34a);color:#04120a}
.secondary{background:rgba(255,255,255,.03);border-color:var(--line)}
.grid{margin-top:22px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.card{background:rgba(16,26,45,.96);border:1px solid var(--line);border-radius:24px;padding:22px;box-shadow:0 12px 36px rgba(0,0,0,.16)}
.card p,.card li{color:var(--muted)}
.card ul{margin:0;padding-left:18px}
.faq-item{background:rgba(255,255,255,.03);border:1px solid var(--line);border-radius:16px;padding:14px 16px;margin-top:12px}
.faq-item h3{margin:0 0 8px;font-size:1.02rem}
.faq-item p{margin:0;color:var(--muted)}
.disclosure{margin-top:18px;padding:18px 20px;border-radius:20px;background:rgba(248,113,113,.08);border:1px solid rgba(248,113,113,.18);color:#fecaca;font-size:.95rem}
.footer{padding:22px 4px 8px;color:var(--muted);font-size:.9rem;text-align:center}
.sticky{position:fixed;left:0;right:0;bottom:0;background:rgba(7,17,31,.9);backdrop-filter:blur(14px);border-top:1px solid rgba(35,49,74,.9);padding:12px 16px}
.sticky .inner{max-width:var(--max);margin:0 auto;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.mini{padding:12px 16px;border-radius:14px;background:linear-gradient(135deg,var(--accent),#16a34a);color:#04120a;font-weight:900;display:inline-flex;align-items:center;justify-content:center;min-height:46px}
.meta-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:14px}
.meta{padding:14px;border-radius:18px;border:1px solid var(--line);background:rgba(255,255,255,.03);color:#cbd5e1;font-size:.95rem}
.callout{margin-top:18px;padding:18px;border-left:4px solid var(--accent);background:rgba(34,197,94,.08);border-radius:18px}
.compare{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.compare > div{padding:16px;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.03)}
@media (max-width:900px){.hero-inner,.grid,.meta-row,.compare{grid-template-columns:1fr}.hero-inner{padding:20px}}
@media (max-width:640px){.wrap{padding:14px}h1{font-size:clamp(1.9rem,11vw,3rem)}.btns{display:grid;grid-template-columns:1fr}.btn,.mini{width:100%}.sticky .inner{flex-direction:column;align-items:stretch}}
"""

def base_for(slug):
    return SITE["base_url"].rstrip("/") + "/" if not slug else f'{SITE["base_url"].rstrip("/")}/{slug}/'

def rel(slug):
    return "./" if not slug else f"./{slug}/"

def page_slug(ptype, idx):
    return f"{ptype}/{ptype}-{idx+1:03d}"

PAGES = [{
    "slug": "",
    "kind": "home",
    "title": HOME["title"],
    "description": HOME["description"],
    "h1": HOME["h1"],
    "hero_badge": HOME["hero_badge"],
    "hero_lead": HOME["hero_lead"],
}]

for h in HUBS:
    PAGES.append({
        "slug": h["slug"],
        "kind": "hub",
        "title": f"{h['title']} | {SITE['brand_name']}",
        "description": h["description"],
        "h1": h["title"],
        "hero_badge": "Topic hub",
        "hero_lead": h["description"],
    })

needed = 1000 - len(PAGES)
for i in range(needed):
    ptype = PAGE_TYPES[i % len(PAGE_TYPES)]
    audience = AUDIENCES[i % len(AUDIENCES)]
    problem = PROBLEMS[i % len(PROBLEMS)]
    angle = ANGLES[i % len(ANGLES)]
    slug = page_slug(ptype, i)
    title_map = {
        "best": f"Best Visible Plans for {audience.title()}",
        "guide": f"Visible Guide for {audience.title()}",
        "compare": f"Visible Compared for {audience.title()}",
        "alternatives": f"Visible Alternatives for {audience.title()}",
        "faq": f"Visible FAQ for {audience.title()}",
        "coverage": f"Visible Coverage Questions for {audience.title()}",
        "deals": f"Visible Deals for {audience.title()}",
        "switch": f"Switch to Visible: {audience.title()}",
        "data": f"Visible Data Plan Fit for {audience.title()}",
        "review": f"Visible Review for {audience.title()}",
    }
    title = title_map[ptype]
    PAGES.append({
        "slug": slug,
        "kind": "longtail",
        "ptype": ptype,
        "audience": audience,
        "problem": problem,
        "angle": angle,
        "title": title,
        "description": f"{title} focused on people who {problem}.",
        "h1": title,
        "hero_badge": f"{ptype.title()} page • {audience}",
        "hero_lead": f"This page helps visitors who {problem}. The angle is {angle}, so the page serves a clear decision instead of repeating the same sales copy.",
    })

def render_nav():
    return "".join(f'<a href="{rel(h["slug"])}">{escape(h["title"])}</a>' for h in HUBS)

def render_faq(items):
    return "".join(
        f'<article class="faq-item"><h3>{escape(q)}</h3><p>{escape(a)}</p></article>'
        for q, a in items
    )

def related(page):
    return [
        {"slug": "review", "label": "Visible Review"},
        {"slug": "faq", "label": "Visible FAQ"},
        {"slug": "alternatives", "label": "Visible Alternatives"},
        {"slug": "guide", "label": "Wireless Guides"},
    ] if page["kind"] == "longtail" else []

def render_body(page):
    if page["kind"] == "home":
        items = [
            ("What this site is", "A Visible-focused affiliate site built around distinct user intents, not one repeated pitch."),
            ("How it helps", "It separates coverage, price, switching, and plan-fit questions into different page families."),
            ("Why the CTA is visible", "The offer stays easy to find, but the page still explains the decision before asking for a click."),
        ]
        faq = render_faq(FAQS)
        return f"""
        <section class="meta-row">
          <div class="meta"><strong>Audience</strong><br>USA visitors</div>
          <div class="meta"><strong>Format</strong><br>Decision pages</div>
          <div class="meta"><strong>Goal</strong><br>Answer intent</div>
          <div class="meta"><strong>Scale</strong><br>1000 pages</div>
        </section>
        <section class="grid" id="details">
          {''.join(f'<article class="card"><h2>{escape(t)}</h2><p>{escape(b)}</p></article>' for t, b in items)}
        </section>
        <section class="card" id="faq">
          <h2>Frequently Asked Questions</h2>
          {faq}
        </section>
        """

    if page["kind"] == "hub":
        if page["slug"] == "review":
            return """
            <section class="grid" id="details">
              <article class="card"><h2>What a review should cover</h2><p>Pricing logic, who it fits, where it falls short, and when another plan may be better.</p></article>
              <article class="card"><h2>What makes this page useful</h2><p>It gives readers a quick yes-or-no frame instead of only pushing the CTA.</p></article>
              <article class="card"><h2>Where to go next</h2><p>Use the long-tail review pages for deeper intent matches.</p></article>
            </section>
            """
        return """
        <section class="grid" id="details">
          <article class="card"><h2>Why this hub exists</h2><p>It organizes related intent families so visitors can move from a broad question to a specific answer.</p></article>
          <article class="card"><h2>How to use it</h2><p>Link this hub from relevant long-tail pages and use it to support navigation.</p></article>
          <article class="card"><h2>Why it matters</h2><p>It keeps the site structured, crawlable, and easier to browse.</p></article>
        </section>
        """

    compare = ""
    if page["ptype"] == "compare":
        compare = """
        <section class="card">
          <h2>What this page compares</h2>
          <div class="compare">
            <div><strong>Visible</strong><p>Simple management, a clean mobile buying flow, and a straightforward offer.</p></div>
            <div><strong>Alternative path</strong><p>Another carrier may fit if the visitor needs different coverage, features, or pricing structure.</p></div>
          </div>
        </section>
        """

    rel_pages = related(page)
    related_html = ""
    if rel_pages:
        related_html = '<section class="card"><h2>Related pages</h2><div class="btns">' + "".join(
            f'<a class="btn secondary" href="{rel(x["slug"])}">{escape(x["label"])}</a>'
            for x in rel_pages
        ) + "</div></section>"

    facts = [
        f"Audience fit: {page['audience']}",
        f"Problem addressed: {page['problem']}",
        f"Primary angle: {page['angle']}",
        "CTA included, but not the only value on the page.",
    ]

    return f"""
    <section class="grid" id="details">
      <article class="card"><h2>Who this page is for</h2><p>Visitors who {escape(page['problem'])}.</p></article>
      <article class="card"><h2>Primary angle</h2><p>{escape(page['angle'])}.</p></article>
      <article class="card"><h2>Page facts</h2><ul>{''.join(f'<li>{escape(f)}</li>' for f in facts)}</ul></article>
    </section>
    {compare}
    <section class="card callout">
      <h2>What to know before clicking</h2>
      <p>Visible may fit people who want simple wireless management, but the best choice depends on coverage, data needs, and monthly budget.</p>
      <ul>{''.join(f'<li>{escape(e)}</li>' for e in EVIDENCE)}</ul>
    </section>
    {related_html}
    """

def render_page(page):
    canonical = base_for(page["slug"])
    body = render_body(page)
    graph = [
        {"@type": "Organization", "name": SITE["name"], "url": base_for("")},
        {"@type": "WebSite", "name": SITE["name"], "url": base_for("")},
        {"@type": "WebPage", "name": page["title"], "url": canonical, "description": page["description"], "inLanguage": SITE["locale"]},
    ]
    if page["kind"] == "home":
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in FAQS
            ],
        })

    return f"""<!doctype html>
<html lang="{SITE["locale"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(page["title"])}</title>
  <meta name="description" content="{escape(page["description"])}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{SITE["locale"].replace('-', '_')}">
  <meta property="og:site_name" content="{escape(SITE["name"])}">
  <meta property="og:title" content="{escape(page["title"])}">
  <meta property="og:description" content="{escape(page["description"])}">
  <meta property="og:url" content="{canonical}">
  <style>{CSS}</style>
  <script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
</head>
<body>
  <div class="wrap">
    <nav class="nav">{render_nav()}</nav>
    <main class="hero">
      <div class="hero-inner">
        <section>
          <span class="pill">{escape(page.get("hero_badge", ""))}</span>
          <h1>{escape(page["h1"])}</h1>
          <p class="lead">{escape(page.get("hero_lead", ""))}</p>
          <div class="btns">
            <a class="btn primary" href="{AFF_URL}" rel="sponsored nofollow noopener noreferrer">Start with Visible</a>
            <a class="btn secondary" href="#details">Explore the page</a>
          </div>
        </section>
        <aside class="card">
          <h2>Fast facts</h2>
          <ul>
            <li>Audience: USA visitors.</li>
            <li>Format: Intent-driven affiliate pages.</li>
            <li>Scale: 1000 total pages.</li>
            <li>Goal: Match user intent first.</li>
          </ul>
        </aside>
      </div>
    </main>
    {body}
    <section class="disclosure">
      <strong>Affiliate disclosure:</strong> This page contains affiliate links. If you click and make a purchase, I may earn a commission at no extra cost to you.
    </section>
    <div class="footer">© 2026 • USA-only wireless promo</div>
  </div>
  <div class="sticky">
    <div class="inner">
      <div><strong>Ready to try Visible?</strong><small>Start with the offer below.</small></div>
      <a class="mini" href="{AFF_URL}" rel="sponsored nofollow noopener noreferrer">Start with Visible</a>
    </div>
  </div>
</body>
</html>"""

for page in PAGES:
    out_dir = ROOT if page["slug"] == "" else ROOT / page["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(render_page(page), encoding="utf-8")

(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base_for('')}sitemap.xml\n", encoding="utf-8")
(ROOT / "llms.txt").write_text(f"# {SITE['name']}\n\nA programmatic affiliate site for USA visitors that explains Visible and targets long-tail wireless intent.\n", encoding="utf-8")
(ROOT / "404.html").write_text(f"<!doctype html><html><head><meta charset='utf-8'><meta name='robots' content='noindex,nofollow'><meta http-equiv='refresh' content='5;url={base_for('')}'></head><body><p>Page not found.</p></body></html>", encoding="utf-8")
(ROOT / ".nojekyll").write_text("", encoding="utf-8")

sitemap = ["<?xml version='1.0' encoding='UTF-8'?>", "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>"]
for page in PAGES:
    sitemap.append(f"  <url><loc>{base_for(page['slug'])}</loc><lastmod>{TODAY}</lastmod></url>")
sitemap.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")

print(f"Built {len(PAGES)} pages.")
