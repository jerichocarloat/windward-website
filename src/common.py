import sys, html, json, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import logo as LG
from icons import ICONS

SITE = 'https://windwardrecruiting.com'
PHONE = '414-939-8700'
CAL = 'https://calendly.com/windwardrecruiting/30min'
LINKEDIN = 'https://www.linkedin.com/company/windward-recruiting/'
JOBBOARD = 'https://host.pcrecruiter.net/pcrbin/jobboard.aspx?uid=chris%20bisenius.chrisbisenius'
TAGLINE = 'The right talent moves business forward.'
DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dist')
e = html.escape


def svg_logo(sub=False, cls=''):
    s, w, h = LG.lockup(fg='currentColor', mode='one', sub=sub)
    return f'<svg class="{cls}" viewBox="0 0 {w:.1f} {h:.1f}" role="img" aria-label="Windward Recruiting"><title>Windward Recruiting</title>{s}</svg>'


def svg_symbol(size=40, color='currentColor'):
    return f'<svg viewBox="0 0 {LG.SW} {LG.SH}" width="{size*LG.SW/LG.SH:.0f}" height="{size}" aria-hidden="true">{LG.sym_inner(color, color, "one")}</svg>'


def ic(name, size=28, cls='ic'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" stroke-linejoin="miter" aria-hidden="true">{ICONS[name]}</svg>'


ARROW = '<svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3 11 11 3M4.5 3H11v6.5"/></svg>'
DIAM = '<svg class="diam" viewBox="0 0 6 10" aria-hidden="true"><polygon points="3,.6 5.4,5 3,9.4 .6,5" fill="none" stroke="currentColor" stroke-width=".8"/></svg>'
LI_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05C20.6 8.65 21 11.3 21 14.7V21h-4v-5.6c0-1.34-.03-3.06-1.86-3.06-1.87 0-2.15 1.46-2.15 2.96V21H9z"/></svg>'
MAIL_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="3" y="5.5" width="18" height="13"/><path d="M3 6l9 7 9-7"/></svg>'
LINK_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></svg>'

ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI']

TEAM = [
    dict(name='Chris Bisenius', slug='chris-bisenius', role='Wealth Management & Financial Services', email='chris@windwardrecruiting.com', phone='414-909-8505', img='team-0.jpg'),
    dict(name='Julianna King', slug='julianna-king', role='Wealth Management & Financial Services', email='julianna@windwardrecruiting.com', phone='414-909-8574', img='team-1.jpg'),
    dict(name='Jon Richio', slug='jon-richio', role='Wealth Management & Financial Services', email='jon@windwardrecruiting.com', phone='414-909-8540', img='team-2.jpg'),
    dict(name='Nick Chiappa', slug='nick-chiappa', role='Wealth Management & Financial Services', email='nick@windwardrecruiting.com', phone='414-909-8515', img='team-3.jpg'),
]

SPECIALTIES = [
    ('Wealth Management', 'Advisors, planners and leaders who connect financial expertise with lasting client relationships.', 'Growth'),
    ('Estate Planning', 'Specialists who understand complex planning needs and the families behind them.', 'Document'),
    ('Tax Planning', 'Tax professionals who bring planning expertise into a broader wealth strategy.', 'Compensation'),
    ('Retirement Planning', 'People who help clients and plan sponsors prepare for the next stage of life.', 'Time'),
    ('Investment Management', 'Investment professionals aligned with your philosophy, process and clients.', 'Market data'),
    ('Relationship Management', 'People who build confidence, continuity and trust with every client.', 'Conversation'),
    ('Accounting', 'Skilled professionals who bring clarity and discipline to financial operations.', 'Shortlist'),
    ('Finance', 'Finance leaders and specialists who support your goals and growth.', 'Insight'),
    ('Trust', 'Experienced talent for trust companies, family offices and their clients.', 'Trust'),
]

REASONS = [
    ('Expertise in wealth management and financial services', 'Uncover hidden talent pools.', 'We focus on one industry, so we know the firms, the roles and the people. That depth helps us find talent that fits your goals, not just your job description.', 'Insight'),
    ('Extensive candidate screening', 'Beyond the surface.', 'We go beyond the résumé. In-depth interviews, skills assessments and background checks confirm experience, qualifications and cultural fit before anyone reaches your desk.', 'Shortlist'),
    ('Customized solutions', 'Tailored to fit your vision.', 'We learn your requirements, culture and business objectives first, then present a curated shortlist of people who share your values and long-term direction.', 'Fit'),
    ('Access to top talent', 'Unlock unparalleled expertise.', 'Our network and proactive outreach reach high-caliber professionals, including passive candidates who are not applying anywhere else.', 'Network'),
    ('Time and cost efficiency', 'Speed up your success.', 'A focused process and efficient screening fill critical roles faster, without cutting corners, so you can stay focused on running the business.', 'Time'),
    ('Long-term partnerships', 'Your success, our commitment.', 'Many clients trust us with search after search. We measure success by the relationship, not the transaction.', 'Trust'),
]

PILLARS = [
    ('Specialist insight', 'We know the market.', 'Wealth management and financial services is all we do. We see the nuances between firms, roles, markets and people that generalists miss.', 'Insight'),
    ('Considered judgment', 'We say what we see.', 'Risks, gaps and concerns are raised early and constructively. A disciplined process keeps every search fair, efficient and reliable.', 'Judgment'),
    ('Lasting relationships', 'We stay in touch.', 'Our network is built through conversation, referral and years of contact, including when there is no placement attached.', 'Network'),
    ('Discretion', 'We protect every name.', 'Confidentiality is a principle, not a guideline. Candidates stay anonymous and searches stay quiet until the right moment.', 'Discretion'),
]

FAQ = [
    ('What kinds of firms do you work with?', 'We focus on wealth management and financial services: registered investment advisers (RIAs), family offices, trust companies, asset managers and other financial services organizations. Our recruiting experience also includes the legal industry.'),
    ('Which roles can Windward help fill?', 'Executive and specialist roles across wealth management, estate, tax and retirement planning, investment and relationship management, accounting, finance and trust. Our open jobs also include operations, service and business development roles.'),
    ('How do you assess fit?', 'We go beyond the résumé with in-depth interviews, skills assessments and background checks. Understanding your culture, goals and long-term vision matters as much as checking experience.'),
    ('I am not actively looking. Should I still talk to you?', 'Yes. Many of the people we place were not looking when we first spoke. A confidential conversation costs nothing, and we never share your name without your permission.'),
    ('How do I share a hiring need or my résumé?', 'Use the forms on our For employers and For candidates pages. Both accept documents up to 50 MB. You can also call us on 414-939-8700 or book a 30-minute call.'),
    ('Where can I see open jobs?', 'Every open role is listed on our Jobs page with the full description. Roles change often, so new ones appear there as soon as they open.'),
]

NAV = [('About', '/about/'), ('Employers', '/employers/'), ('Candidates', '/candidates/'), ('Jobs', '/jobs/'), ('Insights', '/insights/')]

FONT_PRELOAD = ''.join(f'<link rel="preload" href="/assets/fonts/{f}.woff2" as="font" type="font/woff2" crossorigin>' for f in ['Geist-400', 'Switzer-400', 'Switzer-500'])


def head_tags(title, desc, path, img='/assets/img/og.jpg', kind='website', extra=''):
    full = title if title.startswith('Windward') else f'{title} | Windward Recruiting'
    url = SITE + path
    return f'''<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(full)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="{kind}"><meta property="og:site_name" content="Windward Recruiting"><meta property="og:title" content="{e(full)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}{img}"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0B0C0E"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
{FONT_PRELOAD}<link rel="stylesheet" href="/assets/style.css?v=1">{extra}
<script>document.documentElement.classList.add('js')</script>'''


def header(active, over):
    links = ''.join(f'<a class="nl" href="{u}"{" aria-current=page" if active==u else ""}>{n}</a>' for n, u in NAV)
    mlinks = ''.join(f'<a class="ml" style="--i:{i}" href="{u}">{n}<span aria-hidden="true">{ARROW.replace("<svg", "<svg width=18 height=18")}</span></a>' for i, (n, u) in enumerate(NAV + [('Contact', '/contact/')]))
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr{" over" if over else ""}" data-over="{1 if over else 0}"><div class="wrap">
<a class="brand" href="/" aria-label="Windward Recruiting home">{svg_logo()}</a>
<nav class="nav" aria-label="Main">{links}<a class="btn sm cta" href="/contact/">Book a call {ARROW}</a></nav>
<button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mnav"><span></span></button>
</div></header>
<div class="mnav" id="mnav" aria-hidden="true">{mlinks}
<div class="mfoot"><a class="btn light" href="{CAL}" target="_blank" rel="noopener">Book a 30-minute call {ARROW}</a><a class="lab" href="tel:{PHONE}" style="color:#CBCDCF">{PHONE}</a></div></div>'''


def footer():
    return f'''<footer class="ftr"><div class="wrap">
<div class="top">
 <div style="display:flex;flex-direction:column;gap:22px;max-width:420px"><a class="brand" href="/" aria-label="Windward Recruiting home" style="height:auto">{svg_logo(sub=True)}</a>
  <p class="big">The right talent<br><span class="second">moves business forward.</span></p>
  <div class="actions"><a class="btn light sm" href="{CAL}" target="_blank" rel="noopener">Book a 30-minute call {ARROW}</a><a class="btn ghost sm" href="tel:{PHONE}">{PHONE}</a></div></div>
 <div><h4>Windward</h4><ul><li><a href="/about/">About us</a></li><li><a href="/about/#team">Our team</a></li><li><a href="/employers/#expertise">What we recruit</a></li><li><a href="/about/#network">Sanford Rose Associates®</a></li><li><a href="/insights/">Insights</a></li></ul></div>
 <div><h4>Work with us</h4><ul><li><a href="/employers/">Hire with Windward</a></li><li><a href="/candidates/">Share your résumé</a></li><li><a href="/jobs/">Jobs</a></li><li><a href="/contact/">Contact</a></li><li><a href="/search/">Search the site</a></li></ul></div>
 <div><h4>Connect</h4><ul><li><a href="tel:{PHONE}">{PHONE}</a></li><li><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></li><li><a href="{CAL}" target="_blank" rel="noopener">Book a call</a></li></ul></div>
</div>
<div class="bot"><span>© <span data-year>2026</span> Windward Recruiting. A member of the Sanford Rose Associates® executive search network.</span><span><a href="/privacy/">Privacy</a> · <a href="/sitemap/">Site map</a></span></div>
</div></footer>'''


def page(path, title, desc, body, active=None, over=False, img='/assets/img/og.jpg', kind='website', extra_head='', jsonld=None, progress=False):
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ''
    doc = f'''<!doctype html><html lang="en"><head>{head_tags(title, desc, path, img, kind, extra_head)}{ld}</head>
<body class="{"has-over-hdr" if over else ""}">{'<div class="progress" aria-hidden="true"></div>' if progress else ''}{header(active, over)}
<main id="main">{body}</main>{footer()}
<script src="/assets/app.js?v=1" defer></script></body></html>'''
    def _merge(m):
        tag = m.group(0)
        styles = re.findall(r' style="([^"]*)"', tag)
        if len(styles) < 2: return tag
        tag = re.sub(r' style="[^"]*"', '', tag)
        merged = ';'.join(x.strip(';') for x in styles)
        return re.sub(r'^<(\w[\w-]*)', lambda mm: f'<{mm.group(1)} style="{merged}"', tag)
    doc = re.sub(r'<[a-zA-Z][^<>]*>', _merge, doc)
    out = DIST + path + ('index.html' if path.endswith('/') else '')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(doc)
    PAGES.append(path)


PAGES = []


def intro(label_html, title_l1, title_l2, lede='', actions='', crumbs=None):
    cr = ''
    if crumbs:
        cr = '<nav class="crumbs lab" aria-label="Breadcrumb">' + ' <span aria-hidden="true">/</span> '.join(f'<a href="{u}">{e(n)}</a>' if u else f'<span aria-current="page">{e(n)}</span>' for n, u in crumbs) + '</nav>'
    return f'''<section class="intro"><div class="wrap">{cr}<p class="lab" data-reveal>{label_html}</p>
<h1 class="h1" style="margin-top:16px;max-width:20ch;--i:1" data-reveal>{title_l1}{"<br><span class=second>"+title_l2+"</span>" if title_l2 else ""}</h1>
<div class="bottom">{f'<p class="lede" data-reveal style="--i:2">{lede}</p>' if lede else '<span></span>'}{f'<div class="actions" style="justify-content:flex-end;--i:3" data-reveal>{actions}</div>' if actions else ''}</div></div></section>'''


def cta_band(l1='Let’s move forward,', l2='together.', text='A critical hire or a career-defining move. Tell us what comes next and we will take it from there.', img='deal-wide.jpg'):
    return f'''<section class="ctaband"><div class="bg" style="background-image:url(/assets/img/{img})"></div><div class="wrap">
<p class="lab" style="color:var(--steel)" data-reveal>The next chapter starts with a conversation</p>
<h2 class="display" style="max-width:14ch;--i:1" data-reveal>{l1}<br><span class="second">{l2}</span></h2>
<p class="lede" style="color:#B9BCBE" data-reveal>{text}</p>
<div class="actions" data-reveal><a class="btn light" href="{CAL}" target="_blank" rel="noopener">Book a 30-minute call {ARROW}</a><a class="btn ghost" href="/contact/">Contact the team</a></div></div></section>'''


def faq_block(items=FAQ, dark=False, title1='A little clarity', title2='before we begin.'):
    acc = ''.join(f'''<div class="acc-item" data-reveal style="--i:{i}"><h3><button class="acc-q" type="button" aria-expanded="false" aria-controls="faq{i}"><span><span class="num">{i+1:02d}</span>{e(q)}</span><span class="pm" aria-hidden="true"></span></button></h3><div class="acc-a" id="faq{i}" role="region"><div><div class="in body">{a}</div></div></div></div>''' for i, (q, a) in enumerate(items))
    return f'''<section class="sec{" dark" if dark else ""}"><div class="wrap split">
<div class="head" style="position:sticky;top:calc(var(--header) + 24px)"><p class="lab" data-reveal>Questions and answers</p><h2 class="h2" data-reveal>{title1}<br><span class="second">{title2}</span></h2>
<p class="body" data-reveal>Still have a question? Call us on <a class="tlink" href="tel:{PHONE}">{PHONE}</a></p></div>
<div class="acc">{acc}</div></div></section>'''


def fmt_date(iso):
    import datetime
    d = datetime.date.fromisoformat(iso[:10])
    return d.strftime('%-d %b %Y')


def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
