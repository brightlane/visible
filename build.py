from pathlib import Path
from datetime import date
from html import escape
import json
import re
import math

ROOT = Path(".")
TODAY = date.today().isoformat()

DATA = json.loads(Path("content.json").read_text(encoding="utf-8"))

SITE = DATA["site"]
HUBS = DATA["hubs"]
HOME = DATA["home"]
FAQS = DATA["faq"]
KEYWORDS = DATA["keywords"]
MODIFIERS = DATA["modifiers"]
PAGE_TYPES = DATA["page_types"]

BASE_URL = SITE["base_url"].rstrip("/")
AFF_URL = SITE["affiliate_url"]
SITE_NAME = SITE["name"]
BRAND_NAME = SITE["brand_name"]

CSS = """
:root{
  --bg:%(bg)s; --card:%(card)s; --text:%(text)s; --muted:#94a3b8; --line:#23314a;
  --accent:%(accent)s; --shadow:0 24px 70px rgba(0,0,0,.35); --max:1160px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;font-family:Inter,Arial,Helvetica,sans-serif;
  background:radial-gradient(circle at top left, rgba(56,189,248,.15), transparent 30%%),
             radial-gradient(circle at top right, rgba(34,197,94,.12), transparent 30%%),
             linear-gradient(180deg,#07111f 0%%,#08101d 100%%);
  color:var(--text);line-height:1.6;text-rendering:optimizeLegibility;
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
@media (max-width:900px){.hero-inner,.grid,.meta-row{grid-template-columns:1fr}.hero-inner{padding:20px}}
@media (max-width:640px){.wrap{padding:14px}h1{font-size:clamp(1.9rem,11vw,3rem)}.btns{display:grid;grid-template-columns:1fr}.btn,.mini{width:100%%}.sticky .inner{flex-direction:column;align-items:stretch}}
""" % SITE["theme"]

def base_for(slug: str) -> str:
    return BASE_URL + "/" if not slug else f"{BASE_URL}/{slug}/"

def rel(url_slug: str) -> str:
    return "./" if not url_slug else f"./{url_slug}/"

def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

def related_links(page):
    links = [{"slug": "", "label": "Home"}]
    for hub in HUBS[:6]:
        links.append({"slug": hub["slug"], "label": hub["title"]})
    if page["kind"] == "longtail":
        links.extend([
            {"slug": "review", "label": "Visible Review"},
            {"slug": "faq", "label": "Visible FAQ"},
            {"slug": "alternatives", "label": "Visible Alternatives"},
        ])
    return links[:9]

def generate_pages():
    pages = [{
        "slug": "",
        "kind": "home",
        "title": HOME["title"],
        "description": HOME["description"],
        "h1": HOME["h1"],
        "hero_badge": HOME["hero_badge"],
        "hero_lead": HOME["hero_lead"],
        "facts": ["Audience: USA visitors", "Format: Affiliate landing page", "Promise: Simple wireless", "Goal: Drive clicks"],
    }]

    for hub in HUBS:
        pages.append({
            "slug": hub["slug"],
            "kind": "hub",
            "title": hub["title"] + " | " + BRAND_NAME,
            "description": hub["description"],
            "h1": hub["title"],
            "hero_badge": "Topic hub",
            "hero_lead": hub["description"],
            "facts": ["Focused topic hub", "Supports internal linking", "Built for search intent", "Useful as a category page"],
        })

    combos = []
    for ptype in PAGE_TYPES:
        for kw in KEYWORDS:
            for mod in MODIFIERS:
                combos.append((ptype, kw, mod))

    target_total = 1000
    needed = target_total - len(pages)
    combos = combos[:max(0, needed)]

    for ptype, kw, mod in combos:
        slug = f"{ptype}/{kw['slug']}-{slugify(mod)}"
        pages.append({
            "slug": slug,
            "kind": "longtail",
            "page_type": ptype,
            "keyword": kw["head_term"],
            "modifier": mod,
            "title": f"{kw['head_term'].title()} {mod.title()} | Visible USA",
            "description": f"Learn about {kw['head_term']} {mod} with Visible.",
            "h1": f"{kw['head_term'].title()} {mod.title()}",
            "hero_badge": f"{ptype.title()} page • USA visitors",
            "hero_lead": f"This page targets {kw['head_term']} {mod} and explains how Visible fits that use case.",
            "facts": [
                f"Service focus: {kw['head_term']}",
                f"Use case: {mod}",
                f"Intent family: {ptype}",
                "Affiliate offer included",
            ],
        })

    return pages

def score_page(page, body_text, links):
    score = 0
    score += 25 if page.get("title") else 0
    score += 20 if page.get("description") else 0
    score += 20 if len(body_text.split()) >= 120 else 0
    score += 15 if len(page.get("facts", [])) >= 3 else 0
    score += 10 if len(links) >= 5 else 0
    score += 10
    return score

def render_body(page):
    if page["kind"] == "home":
        faq_html = "".join(
            f'<article class="faq-item"><h3>{escape(item["question"])}</h3><p>{escape(item["answer"])}</p></article>'
            for item in FAQS
        )
        return f"""
        <section class="meta-row" aria-label="Key facts">
          <div class="meta"><strong>Audience</strong><br>USA visitors</div>
          <div class="meta"><strong>Format</strong><br>Affiliate landing page</div>
          <div class="meta"><strong>Promise</strong><br>Simple wireless</div>
          <div class="meta"><strong>Goal</strong><br>Drive clicks</div>
        </section>
        <section class="grid" id="details">
          <article class="card"><h2>What Visible Does</h2><p>Visible is a wireless service focused on simple plans, straightforward signup, and easy online account management.</p></article>
          <article class="card"><h2>Why Visitors Click</h2><p>The message is simple: one offer, one action, and a clear path to continue.</p></article>
          <article class="card"><h2>What You Get</h2><ul><li>Simple wireless positioning.</li><li>Clear CTA placement.</li><li>Mobile-friendly layout.</li><li>Affiliate disclosure.</li></ul></article>
        </section>
        <section class="card faq" id="faq">
          <h2>Frequently Asked Questions</h2>
          {faq_html}
        </section>
        """
    if page["kind"] == "hub":
        return """
        <section class="grid" id="details">
          <article class="card"><h2>Why this hub exists</h2><p>This hub organizes related long-tail pages and helps visitors move from a broad question to a specific answer.</p></article>
          <article class="card"><h2>How to use it</h2><p>Link this hub from long-tail pages and use it to surface the most relevant pages in the cluster.</p></article>
          <article class="card"><h2>What makes it useful</h2><p>It creates a clean topic map for crawlers and users.</p></article>
        </section>
        """
    facts = "".join(f"<li>{escape(f)}</li>" for f in page["facts"])
    links = "".join(f'<a class="btn secondary" href="{rel(l["slug"])}">{escape(l["label"])}</a>' for l in related_links(page))
    return f"""
    <section class="grid" id="details">
      <article class="card"><h2>Core angle</h2><p>{escape(page['keyword'])} {escape(page['modifier'])} with Visible.</p></article>
      <article class="card"><h2>Why it matters</h2><p>This page targets a specific intent and gives users a fast answer that fits a commercial search.</p></article>
      <article class="card"><h2>Page facts</h2><ul>{facts}</ul></article>
    </section>
    <section class="card">
      <h2>Related pages</h2>
      <div class="btns">{links}</div>
    </section>
    """

def render_page(page):
    canonical = base_for(page["slug"])
    body = render_body(page)
    body_text = re.sub(r"<[^>]+>", " ", body)
    links = related_links(page)
    score = score_page(page, body_text, links)
    indexable = score >= 80
    robots = "index,follow" if indexable else "noindex,nofollow"

    graph = [
        {"@type": "Organization", "name": SITE_NAME, "url": base_for(""), "logo": "https://www.visible.com/favicon.ico"},
        {"@type": "WebSite", "name": SITE_NAME, "url": base_for("")},
        {"@type": "WebPage", "name": page["title"], "url": canonical, "description": page["description"], "inLanguage": SITE["locale"]},
    ]
    if page["kind"] == "home":
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": item["question"], "acceptedAnswer": {"@type": "Answer", "text": item["answer"]}}
                for item in FAQS
            ],
        })

    nav = "".join(f'<a href="{rel(h["slug"])}">{escape(h["title"])}</a>' for h in HUBS)

    return f"""<!doctype html>
<html lang="{SITE["locale"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(page["title"])}</title>
  <meta name="description" content="{escape(page["description"])}">
  <meta name="robots" content="{robots},max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{SITE["locale"].replace('-', '_')}">
  <meta property="og:site_name" content="{escape(SITE_NAME)}">
  <meta property="og:title" content="{escape(page["title"])}">
  <meta property="og:description" content="{escape(page["description"])}">
  <meta property="og:url" content="{canonical}">
  <style>{CSS}</style>
  <script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
</head>
<body>
  <div class="wrap">
    <nav class="nav">{nav}</nav>
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
          <ul>{''.join(f'<li>{escape(f)}</li>' for f in page.get("facts", []))}</ul>
          <p><strong>Quality score:</strong> {score}/100</p>
          <p><strong>Indexable:</strong> {"yes" if indexable else "no"}</p>
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

PAGES = generate_pages()

for page in PAGES:
    out_dir = ROOT if page["slug"] == "" else ROOT / page["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(render_page(page), encoding="utf-8")

(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base_for('')}sitemap.xml\n", encoding="utf-8")
(ROOT / "llms.txt").write_text(f"# {SITE_NAME}\n\nA programmatic affiliate site for USA visitors that explains Visible and targets long-tail wireless intent.\n", encoding="utf-8")
(ROOT / "404.html").write_text(f"<!doctype html><html><head><meta charset='utf-8'><meta name='robots' content='noindex,nofollow'><meta http-equiv='refresh' content='5;url={base_for('')}'></head><body><p>Page not found.</p></body></html>", encoding="utf-8")
(ROOT / ".nojekyll").write_text("", encoding="utf-8")

sitemap = ["<?xml version='1.0' encoding='UTF-8'?>", "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>"]
for page in PAGES:
    sitemap.append(f"  <url><loc>{base_for(page['slug'])}</loc><lastmod>{TODAY}</lastmod></url>")
sitemap.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")

print(f"Built {len(PAGES)} pages.")
