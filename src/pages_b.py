from common import *
from pages_a import post_card, job_row, team_cards


def fld(name, label, kind='text', req=True, full=False, ph='', auto='', opts=None, hint='', val=''):
    r = ' required' if req else ''
    star = ' <span class="req">(required)</span>' if req else ' <span class="req">(optional)</span>'
    cls = 'fld full' if full else 'fld'
    if kind == 'textarea':
        ctrl = f'<textarea id="{name}" name="{name}"{r} placeholder="{e(ph)}">{e(val)}</textarea>'
    elif kind == 'select':
        ctrl = f'<select id="{name}" name="{name}"{r}><option value="">Choose one</option>' + ''.join(f'<option{" selected" if o==val else ""}>{e(o)}</option>' for o in opts) + '</select>'
    elif kind == 'radio':
        ctrl = '<div class="radios">' + ''.join(f'<label><input type="radio" name="{name}" value="{o}"{r}> {o}</label>' for o in opts) + '</div>'
        return f'<fieldset class="{cls}" style="border:0;padding:0;margin:0"><legend>{label}{star}</legend>{ctrl}<span class="err" role="alert"></span></fieldset>'
    elif kind == 'file':
        ctrl = f'<label class="file" for="{name}">{ic("Document",24,"")}<span><span data-file-label data-default="Choose a file or drag it here">Choose a file or drag it here</span><br><span class="hint">PDF, Word or image. Max. file size 50 MB.</span></span><input id="{name}" name="{name}" type="file" accept=".pdf,.doc,.docx,.rtf,.txt,.png,.jpg,.jpeg"{r}></label>'
        return f'<div class="{cls}"><span style="font-size:14px;font-weight:500">{label}{star}</span>{ctrl}<span class="err" role="alert"></span></div>'
    else:
        ctrl = f'<input id="{name}" name="{name}" type="{kind}"{r} placeholder="{e(ph)}" autocomplete="{auto}" value="{e(val)}">'
    return f'<div class="{cls}"><label for="{name}">{label}{star}</label>{ctrl}{f"<span class=hint>{hint}</span>" if hint else ""}<span class="err" role="alert"></span></div>'


def form(fid, subject, fields, submit, done_title, done_text):
    return f'''<div class="form-wrap"><form class="form" data-form name="{fid}" method="POST" enctype="multipart/form-data" data-netlify="true" netlify-honeypot="bot-field" data-subject="{e(subject)}">
<input type="hidden" name="form-name" value="{fid}"><p class="sr"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
{fields}
<div class="full submit"><button class="btn" type="submit">{submit} {ARROW}</button><p class="small">Your details are confidential and only used to respond to you. <a class="tlink" href="/privacy/">Privacy</a></p></div></form>
<div class="form-done" role="status" aria-live="polite">{svg_symbol(28)}<h3 class="h3">{done_title}</h3><p class="body" data-ok>{done_text}</p><p class="body" data-mail>Your email app has opened with your details filled in. Press send to reach us, and attach your file if you added one. Prefer to talk? Call <a class="tlink" href="tel:{PHONE}">{PHONE}</a>.</p></div></div>'''


def employer_form(role=''):
    roles = [n for n, _, _ in SPECIALTIES] + ['Operations', 'Compliance', 'Executive leadership', 'Other']
    f = (fld('first_name', 'First name', auto='given-name') + fld('last_name', 'Last name', auto='family-name') + fld('phone', 'Phone', 'tel', auto='tel') + fld('email', 'Email', 'email', auto='email') +
         fld('company', 'Company name', auto='organization') + fld('position_type', 'Type of position you are looking to fill', 'select', opts=roles, val=role) +
         fld('job_description', 'Upload the job description', 'file', req=False, full=True) +
         fld('message', 'Anything else we should know?', 'textarea', req=False, full=True, ph='Timing, location, confidentiality, team context…'))
    return form('search-request', 'Search request', f, 'Send search request', 'Thank you. Your request is with us.', 'A Windward specialist will be in touch within one business day to talk through the role. If it is urgent, call us on 414-939-8700.')


def candidate_form(role=''):
    f = (fld('first_name', 'First name', auto='given-name') + fld('last_name', 'Last name', auto='family-name') + fld('phone', 'Phone', 'tel', auto='tel') + fld('email', 'Email', 'email', auto='email') +
         fld('currently_employed', 'Are you currently employed?', 'radio', opts=['Yes', 'No'], full=True) +
         fld('role_sought', 'What kind of role are you looking for?', 'text', req=False, full=True, ph='For example: Senior Wealth Advisor, Chicago or remote', val=role) +
         fld('resume', 'Upload your résumé', 'file', req=True, full=True) +
         fld('message', 'Anything else you would like us to know?', 'textarea', req=False, full=True, ph='Location preferences, timing, what matters in your next move…'))
    return form('submit-resume', 'Résumé submission' + (f' - {role}' if role else ''), f, 'Submit résumé', 'Thank you. Your résumé is with us.', 'A recruiter will review your experience and contact you about suitable opportunities. Your details stay confidential.')


def contact_form():
    f = (fld('c_name', 'Your name', auto='name') + fld('c_email', 'Email', 'email', auto='email') + fld('c_phone', 'Phone', 'tel', req=False, auto='tel') +
         fld('c_topic', 'How can we help?', 'select', opts=['I am looking to hire', 'I am looking for my next role', 'Market or compensation question', 'Something else']) +
         fld('c_message', 'Message', 'textarea', full=True))
    return form('contact', 'Website enquiry', f, 'Send message', 'Thank you. We have your message.', 'We reply to every message, usually within one business day.')


def employers():
    areas = [('Wealth management', 'The people behind financial confidence.', 'Advisors, planners and leaders for RIAs, family offices, trust companies and asset managers. People who understand your clients as well as your business.', 'advisor-meeting.jpg'),
             ('Financial services', 'Specialized roles, considered connections.', 'Accounting, finance, investment management and trust, plus operations and compliance. Our wider experience also includes the legal industry.', 'documents.jpg'),
             ('Executive search', 'A thoughtful search for a lasting decision.', 'Engaged search for senior and critical hires, shaped around your requirements, culture and business goals, with detailed screening at every step.', 'deal.jpg')]
    areash = ''.join(f'''<div class="area" data-reveal style="--i:{i}"><div class="pic"><img src="/assets/img/{img}" alt="" loading="lazy"></div><p class="lab">{i+1:02d} / {l}</p><h3 class="h3">{t}</h3><p class="body small">{d}</p></div>''' for i, (l, t, d, img) in enumerate(areas))
    specs = ''.join(f'''<div class="spec" id="{slugify(n)}" data-reveal style="--i:{i%3}"><div class="top">{ic(icn,30)}<span class="lab">{i+1:02d}</span></div><h3 class="h4" style="margin-top:14px">{n}</h3><p class="small">{d}</p><a class="tlink small" style="margin-top:8px;align-self:flex-start;color:var(--ink)" href="/employers/?role={slugify(n)}#search">Discuss this specialty {ARROW}</a></div>''' for i, (n, d, icn) in enumerate(SPECIALTIES))
    proc = [('Search', 'Tell us about the role', 'Share the job description or simply describe the need. A specialist calls to understand the role, team, culture and timeline.'), ('Network', 'We search the whole market', 'We reach beyond active job seekers into our network of passive candidates and industry relationships.'), ('Shortlist', 'Meet a curated shortlist', 'Interviewed, assessed and referenced candidates, each with an honest note on strengths and gaps.'), ('Trust', 'Hire with confidence', 'We support interviews, offers and the start date, and stay in touch to make sure the placement lasts.')]
    proch = ''.join(f'<div class="card" data-reveal style="--i:{i}"><div style="display:flex;justify-content:space-between">{ic(icn,30)}<span class="lab">Step {i+1:02d}</span></div><h3 class="h3" style="margin-top:20px">{t}</h3><p class="small" style="color:#B9BCBE">{d}</p></div>' for i, (icn, t, d) in enumerate(proc))
    reasons = ''.join(f'''<li data-reveal style="--i:{i%2}"><span class="lab">{i+1:02d}</span><div style="display:flex;gap:14px;align-items:flex-start">{ic(icn,26)}<h3 class="h4">{n}</h3></div><p class="body">{d}</p></li>''' for i, (n, s, d, icn) in enumerate(REASONS))
    body = intro('For employers', 'Hire with the whole', 'market in view.', 'Executive search and recruitment for wealth management and financial services firms. From a single critical hire to a growing team, we find the people who help your firm grow, lead and serve clients well.', f'<a class="btn" href="#search">Start a search request {ARROW}</a><a class="btn line" href="/contact/">Book a call</a>', [('Home', '/'), ('Employers', None)]) + f'''
<section class="sec" style="padding-top:8px"><div class="wrap"><div class="grid g3">{areash}</div></div></section>
<section class="sec white" id="expertise"><div class="wrap"><div class="head row"><div class="head" style="margin:0"><p class="lab" data-reveal>What we recruit</p><h2 class="h2" data-reveal>Nine practice areas.<br><span class="second">One industry.</span></h2></div><p class="lede" style="max-width:42ch" data-reveal>Specialists in the roles that shape a wealth management firm.</p></div>
<div class="grid g3">{specs.replace('class="spec"','class="spec" style="background:var(--fog)"')}</div></div></section>
<section class="sec dark"><div class="wrap"><div class="head row"><div class="head" style="margin:0"><p class="lab" data-reveal>How a search works</p><h2 class="h2" data-reveal>Four steps.<br><span class="second">No surprises.</span></h2></div><a class="btn ghost" href="#search" data-reveal>Start a search {ARROW}</a></div><div class="grid g4">{proch}</div></div></section>
<section class="sec"><div class="wrap split">
<div class="head" style="position:sticky;top:calc(var(--header) + 24px)"><p class="lab" data-reveal>Why Windward</p><h2 class="h2" data-reveal>What a focused search<br><span class="second">brings to your firm.</span></h2><p class="body" data-reveal>Six reasons firms trust us with the hires that matter most.</p></div>
<ul class="rows">{reasons}</ul></div></section>
<section class="sec white" id="search"><div class="wrap split">
<div class="head" style="position:sticky;top:calc(var(--header) + 24px)"><p class="lab" data-reveal>Search request</p><h2 class="h2" data-reveal>Tell us what<br><span class="second">you need.</span></h2><p class="body" data-reveal>The more context you share, the faster we can help. Everything you send is treated in confidence.</p>
<ul class="blist small" data-reveal><li>{DIAM}A specialist replies within one business day</li><li>{DIAM}Engaged search options for critical hires</li><li>{DIAM}Market and compensation insight included</li></ul>
<p class="small" data-reveal>Prefer to talk? <a class="tlink" href="/contact/">Book a 30-minute call</a> or call <a class="tlink" href="tel:{PHONE}">{PHONE}</a></p></div>
<div data-reveal>{employer_form()}</div></div></section>
{faq_block()}{cta_band()}'''
    page('/employers/', 'Executive Search for Employers', 'Executive search and recruitment for wealth management and financial services firms: nine practice areas, a four-step search and a confidential search request.', body, active='/employers/')


def candidates(jobs):
    tips = ''.join(f'<div class="card" data-reveal style="--i:{i}">{ic(icn,30)}<h3 class="h4" style="margin-top:10px">{t}</h3><p class="small" style="color:var(--body)">{d}</p></div>' for i, (icn, t, d) in enumerate([
        ('Discretion', 'Confidential by default', 'Your name and details are never shared with a firm without your permission.'),
        ('Conversation', 'An honest conversation', 'We tell you what we know about the firm, the role and the market, including the parts that matter most.'),
        ('Fit', 'Fit before speed', 'We look for the move that still makes sense years from now. 92% of our candidates stay in post for seven years or more.')]))
    body = intro('For candidates', 'Find a role', 'worth moving for.', 'For advisors, planners and wealth management professionals. Whether you are actively looking or simply curious, share your résumé in confidence and we will match you with roles that fit your goals.', f'<a class="btn" href="#submit">Submit your résumé {ARROW}</a><a class="btn line" href="/jobs/">See {len(jobs)} open jobs</a>', [('Home', '/'), ('Candidates', None)]) + f'''
<section class="sec" style="padding-top:8px"><div class="wrap"><div class="grid g3">{tips}</div></div></section>
<section class="sec white" id="submit"><div class="wrap split">
<div class="head" style="position:sticky;top:calc(var(--header) + 24px)"><p class="lab" data-reveal>Submit your résumé</p><h2 class="h2" data-reveal>Tell us where<br><span class="second">you want to go.</span></h2><p class="body" data-reveal>A recruiter who specializes in your field reviews every submission personally.</p>
<div class="pic ratio-43" data-reveal style="margin-top:8px"><img src="/assets/img/walk-briefcase.jpg" alt="A professional walking to work with a briefcase" loading="lazy"></div></div>
<div data-reveal>{candidate_form()}</div></div></section>
{faq_block()}{cta_band()}'''
    page('/candidates/', 'Submit Your Résumé', 'Share your résumé with Windward Recruiting and explore confidential opportunities in wealth management and financial services.', body, active='/candidates/')


def contact():
    team = team_cards()
    body = f'''<section class="intro contact-top"><div class="wrap"><nav class="crumbs lab" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <span aria-current="page">Contact</span></nav>
<div class="book">
<div class="book-t"><p class="lab" data-reveal>The fastest way to start</p><h1 class="h1" data-reveal style="--i:1">Book a <span style="white-space:nowrap">30-minute</span> call<br><span class="second">with a specialist.</span></h1>
<p class="lede" data-reveal style="--i:2">Hiring for a critical role, or thinking about your next move? Pick a time that suits you. You will speak with a recruiter who knows wealth management and financial services.</p>
<ul class="blist" data-reveal style="--i:3"><li>{DIAM}30 minutes, by phone or video</li><li>{DIAM}Confidential, with no obligation</li><li>{DIAM}Honest advice on the market, pay and fit</li></ul>
<div class="actions" data-reveal style="--i:4"><a class="btn" href="{CAL}" target="_blank" rel="noopener">Choose a time {ARROW}</a><a class="btn line" href="tel:{PHONE}">Call {PHONE}</a></div></div>
<div class="book-cal" data-reveal style="--i:2" data-cal="{CAL}"><div class="cal-fallback">{ic("Calendar",36,"")}<p class="h3">Pick a time that works for you.</p><p class="small">Our calendar opens in a new tab. It takes under a minute.</p><a class="btn light" href="{CAL}" target="_blank" rel="noopener">Open the calendar {ARROW}</a></div></div>
</div></div></section>
<section class="sec white" id="forms"><div class="wrap split">
<div class="head" style="position:sticky;top:calc(var(--header) + 24px)"><p class="lab" data-reveal>Prefer to write?</p><h2 class="h2" data-reveal>Send us the details.<br><span class="second">We reply within a day.</span></h2><p class="body" data-reveal>Share a hiring need, your résumé or a question. Every message is read by a specialist and treated in confidence.</p>
<p class="small" data-reveal>Follow us on <a class="tlink" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a> for jobs and market insight.</p></div>
<div data-reveal><div class="tabs" role="tablist" aria-label="Choose a form">
<button role="tab" id="t-hire" aria-controls="p-hire" aria-selected="true" data-hash="hire">Looking to hire?</button><button role="tab" id="t-work" aria-controls="p-work" aria-selected="false" tabindex="-1" data-hash="work">Looking for work?</button><button role="tab" id="t-other" aria-controls="p-other" aria-selected="false" tabindex="-1" data-hash="message">Something else</button></div>
<div role="tabpanel" id="p-hire" aria-labelledby="t-hire">{employer_form()}</div>
<div role="tabpanel" id="p-work" aria-labelledby="t-work" hidden>{candidate_form().replace('id="', 'id="w_').replace('for="', 'for="w_').replace('aria-controls="w_', 'aria-controls="')}</div>
<div role="tabpanel" id="p-other" aria-labelledby="t-other" hidden>{contact_form()}</div></div></div></section>
<section class="sec" id="team"><div class="wrap"><div class="head row"><div class="head" style="margin:0"><p class="lab" data-reveal>Direct lines</p><h2 class="h2" data-reveal>Speak to the team<br><span class="second">directly.</span></h2></div><p class="lede" style="max-width:38ch" data-reveal>Call or email any of us. You will always reach a specialist, never a switchboard.</p></div><div class="grid g4 team-grid">{team}</div></div></section>
{faq_block()}'''
    page('/contact/', 'Contact Windward Recruiting', 'Book a 30-minute call with a Windward Recruiting specialist, call 414-939-8700, or send a hiring request or résumé.', body, active='/contact/')


FAMILIES = [('Advisory', ['advisor', 'wealth manager', 'lead advisor']), ('Planning', ['planning', 'planner', 'strategist', 'estate']), ('Client service', ['service', 'client relationship', 'client services']), ('Business development', ['business development', 'regional', 'rvp', 'm&a']), ('Leadership', ['director'])]


def job_family(t):
    tl = t.lower()
    for f, keys in [('Leadership', ['director of']), ('Business development', ['business development', 'regional vp', 'rvp', 'm&a', 'regional director']), ('Planning', ['planning', 'strategist']), ('Client service', ['service', 'client relationship', 'client services']), ('Advisory', ['advisor', 'wealth manager'])]:
        if any(k in tl for k in keys): return f
    return 'Advisory'


def prep_jobs(raw):
    out = []; used = set()
    for j in raw:
        place = re.sub(r'\s*\d{5}\s*$', '', j['loc']).strip().rstrip(',').strip()
        place = place.replace('Col. Springs, Nashville, Phx.', 'Colorado Springs, Nashville or Phoenix')
        st = re.search(r',\s*([A-Z]{2})$', place)
        region = st.group(1) if st else ('Remote' if 'remote' in place.lower() else 'Multiple')
        slug = slugify(j['title'] + ' ' + place)
        while slug in used: slug += '-2'
        used.add(slug)
        out.append(dict(j, place=place, region=region, slug=slug, family=job_family(j['title'])))
    return sorted(out, key=lambda x: x['date'], reverse=True)


def opportunities(jobs):
    from urllib.parse import quote
    fams = sorted(set(j['family'] for j in jobs))
    regs = sorted(set(j['region'] for j in jobs))
    chips = '<button class="chip" type="button" data-group="family" data-chip="all">All roles</button>' + ''.join(f'<button class="chip" type="button" data-group="family" data-chip="{slugify(f)}">{f}</button>' for f in fams)
    regsel = ''.join(f'<button class="chip" type="button" data-group="region" data-chip="{slugify(r)}">{r}</button>' for r in regs)
    rows = ''
    for i, j in enumerate(jobs):
        r = job_row(j, i % 6)
        srch = e(' '.join([j['title'], j['place'], j['family'], j['region']]).lower())
        r = r.replace('<a class="job"', f'<a class="job" data-item data-search="{srch}" data-family="{slugify(j["family"])}" data-region="{slugify(j["region"])}"', 1)
        rows += r
    body = intro('Open jobs', 'A better fit.', 'A bigger possibility.', 'Open jobs in wealth management and financial services. Every listing has the full description, and you can apply in a few minutes.', f'<a class="btn" href="/candidates/">Share your résumé {ARROW}</a>', [('Home', '/'), ('Jobs', None)]) + f'''
<section class="sec" style="padding-top:8px"><div class="wrap" data-filter-root data-noun="jobs">
<div class="toolbar"><div class="field-search">{ic("Search",18,"")}<label class="sr" for="jq">Search roles or locations</label><input id="jq" type="search" data-filter-input placeholder="Search roles or locations"></div><p class="lab" data-count role="status">{len(jobs)} jobs</p></div>
<div style="display:flex;flex-direction:column;gap:10px;margin-bottom:24px"><div class="chips" aria-label="Filter by role type">{chips}</div><div class="chips" aria-label="Filter by location"><button class="chip" type="button" data-group="region" data-chip="all">All locations</button>{regsel}</div></div>
<div>{rows}</div><p class="empty is-hidden" data-empty>No roles match that search yet. <a class="tlink" href="/candidates/">Share your résumé</a> and we will contact you when the right role opens.</p>
</div></section>
<section class="sec white"><div class="wrap split even" style="align-items:center"><div class="head" style="margin:0"><p class="lab" data-reveal>Don’t see the right role?</p><h2 class="h2" data-reveal>Many of our best roles<br><span class="second">are never advertised.</span></h2><p class="body" data-reveal>Share your résumé in confidence and we will reach out when an opportunity fits your goals.</p><div class="actions" data-reveal><a class="btn" href="/candidates/">Submit your résumé {ARROW}</a><a class="btn line" href="{CAL}" target="_blank" rel="noopener">Book a call</a></div></div>
<div class="pic ratio-32" data-reveal><img src="/assets/img/interview-smile.jpg" alt="A candidate shaking hands with a hiring manager" loading="lazy"></div></div></section>{faq_block()}'''
    page('/jobs/', 'Jobs', f'{len(jobs)} open jobs in wealth management and financial services, from wealth advisors to planning, service and leadership roles.', body, active='/jobs/')
    for j in jobs:
        apply = f'{JOBBOARD}&action=detail&recordid={j["id"]}&apply=y'
        others = [x for x in jobs if x['slug'] != j['slug'] and x['family'] == j['family']][:3] or [x for x in jobs if x['slug'] != j['slug']][:3]
        ld = {"@context": "https://schema.org", "@type": "JobPosting", "title": j['title'], "description": j['html'], "datePosted": j['date'][:10], "hiringOrganization": {"@type": "Organization", "name": "Windward Recruiting", "sameAs": SITE}, "jobLocation": {"@type": "Place", "address": {"@type": "PostalAddress", "addressLocality": j['place'], "addressCountry": "US"}}}
        if 'remote' in j['place'].lower(): ld["jobLocationType"] = "TELECOMMUTE"
        body = f'''<section class="intro"><div class="wrap"><nav class="crumbs lab" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <a href="/jobs/">Jobs</a> <span aria-hidden="true">/</span> <span aria-current="page">{e(j["family"])}</span></nav>
<p class="lab" style="margin-top:22px" data-reveal>{e(j["family"])} · {e(j["place"])}</p><h1 class="h1" style="margin-top:14px;max-width:22ch" data-reveal>{e(j["title"])}</h1></div></section>
<section class="sec" style="padding-top:0"><div class="wrap job-detail">
<article class="prose" data-reveal>{j["html"]}</article>
<aside data-reveal><div class="card" style="gap:18px"><dl class="facts"><div><dt>Location</dt><dd>{e(j["place"])}</dd></div><div><dt>Role type</dt><dd>{e(j["family"])}</dd></div><div><dt>Posted</dt><dd>{fmt_date(j["date"])}</dd></div><div><dt>Reference</dt><dd class="mono" style="font-size:13px">{j["id"][-6:]}</dd></div></dl>
<a class="btn" href="{apply}" target="_blank" rel="noopener" style="justify-content:center">Apply for this role {ARROW}</a><a class="btn line" href="/candidates/?role={quote(j["title"]+", "+j["place"])}#submit" style="justify-content:center">Send us your résumé</a>
<p class="small">Questions about this role? Call <a class="tlink" href="tel:{PHONE}">{PHONE}</a>. Client names are shared once we have spoken.</p></div></aside></div></section>
<section class="sec white"><div class="wrap"><div class="head row"><div class="head" style="margin:0"><p class="lab">More jobs</p><h2 class="h2">Other roles<br><span class="second">you may like.</span></h2></div><a class="btn line" href="/jobs/">All jobs {ARROW}</a></div>
<div style="background:var(--fog);padding:8px">{"".join(job_row(o, i) for i, o in enumerate(others)).replace('class="job"', 'class="job" style="background:#fff"')}</div></div></section>{cta_band()}'''
        desc = re.sub(r'<[^>]+>', ' ', j['html']); desc = ' '.join(desc.split())[:155]
        page(f'/jobs/{j["slug"]}/', f'{j["title"]}, {j["place"]}', desc, body, active='/jobs/', jsonld=ld)


AUTHORS = {'Chris Bisenius': ('chris-bisenius', 'team-0.jpg', 'Wealth Management & Financial Services recruiter at Windward Recruiting.'), 'Julianna King': ('julianna-king', 'team-1.jpg', 'Wealth Management & Financial Services recruiter at Windward Recruiting.'), 'Andrew Miller': ('andrew-miller', None, 'Guest contributor, Next Level Exchange, a Sanford Rose Associates affiliate.')}


def insights(arts):
    topics = sorted(set(a['topic'] for a in arts))
    authors = sorted(set(a['author'] for a in arts))
    chips = '<button class="chip" type="button" data-group="topic" data-chip="all">All topics</button>' + ''.join(f'<button class="chip" type="button" data-group="topic" data-chip="{slugify(t)}">{t}</button>' for t in topics)
    achips = '<button class="chip" type="button" data-group="author" data-chip="all">All authors</button>' + ''.join(f'<button class="chip" type="button" data-group="author" data-chip="{slugify(a)}">{a}</button>' for a in authors)
    f = arts[0]
    feat = f'''<a class="feature" href="/insights/{f["slug"]}/" data-reveal><div class="pic"><img src="/assets/img/{f["image"]}.jpg" alt=""></div><div class="txt"><p class="lab">Latest · {e(f["topic"])}</p><h2 class="h2" style="font-size:clamp(28px,2.8vw,40px)">{e(f["title"])}</h2><p class="body">{e(f["excerpt"])}</p><div class="foot"><p class="small">{e(f["author"])} · {fmt_date(f["date"])} · {f["minutes"]} min read</p><span class="tlink" style="margin-top:14px">Read the article {ARROW}</span></div></div></a>'''
    cards = ''
    for i, a in enumerate(arts):
        c = post_card(a, i % 3)
        srch = e(' '.join([a['title'], a['excerpt'], a['author'], a['topic']]).lower())
        cards += c.replace('<a class="post-card"', f'<a class="post-card" data-item data-search="{srch}" data-topic="{slugify(a["topic"])}" data-author="{slugify(a["author"])}"', 1)
    body = intro('Windward Perspectives', 'What we’re seeing.', 'What it means for you.', 'Market insight, hiring advice and career thinking for wealth management and financial services, written by the Windward team.', '', [('Home', '/'), ('Insights', None)]) + f'''
<section class="sec" style="padding-top:8px"><div class="wrap">{feat}</div></section>
<section class="sec white" style="padding-top:clamp(40px,5vw,64px)"><div class="wrap" data-filter-root data-noun="articles">
<div class="toolbar"><div class="field-search">{ic("Search",18,"")}<label class="sr" for="aq">Search articles</label><input id="aq" type="search" data-filter-input placeholder="Search articles"></div><p class="lab" data-count role="status">{len(arts)} articles</p></div>
<div style="display:flex;flex-direction:column;gap:10px;margin-bottom:32px"><div class="chips" aria-label="Filter by topic">{chips}</div><div class="chips" aria-label="Filter by author">{achips}</div></div>
<div class="grid g3" style="gap:36px 16px">{cards}</div><p class="empty is-hidden" data-empty>No articles match that search.</p></div></section>{cta_band()}'''
    page('/insights/', 'Insights', 'Windward Perspectives: market insight, hiring advice and career thinking for wealth management and financial services.', body, active='/insights/')

    for idx, a in enumerate(arts):
        slug, img, bio = AUTHORS.get(a['author'], ('', None, ''))
        av = f'<img src="/assets/img/{img}" alt="">' if img else f'<span class="ph">{a["author"][0]}</span>'
        url = SITE + f'/insights/{a["slug"]}/'
        from urllib.parse import quote
        share = f'''<div class="share"><a href="https://www.linkedin.com/sharing/share-offsite/?url={quote(url, safe="")}" target="_blank" rel="noopener" aria-label="Share on LinkedIn">{LI_ICON}</a><a href="mailto:?subject={quote(a["title"])}&amp;body={quote(url)}" aria-label="Share by email">{MAIL_ICON}</a><button type="button" data-copy aria-label="Copy link">{LINK_ICON}</button></div><span class="small tip" aria-live="polite" style="min-height:1em"></span>'''
        related = [x for x in arts if x['slug'] != a['slug'] and x['topic'] == a['topic']][:3]
        if len(related) < 3: related += [x for x in arts if x['slug'] != a['slug'] and x not in related][:3 - len(related)]
        prev_a = arts[idx + 1] if idx + 1 < len(arts) else None
        next_a = arts[idx - 1] if idx > 0 else None
        nav = '<div class="grid g2" style="margin-top:48px">' + (f'<a class="card link" href="/insights/{prev_a["slug"]}/"><span class="lab">Previous</span><span class="h4">{e(prev_a["title"])}</span></a>' if prev_a else '<span></span>') + (f'<a class="card link" href="/insights/{next_a["slug"]}/" style="text-align:right"><span class="lab">Next</span><span class="h4">{e(next_a["title"])}</span></a>' if next_a else '<span></span>') + '</div>'
        ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a['title'], "datePublished": a['date'], "dateModified": a['modified'] or a['date'], "author": {"@type": "Person", "name": a['author']}, "publisher": {"@type": "Organization", "name": "Windward Recruiting"}, "image": SITE + f'/assets/img/{a["image"]}.jpg', "mainEntityOfPage": url, "description": a['excerpt']}
        body = f'''<section class="article-hero"><div class="wrap"><nav class="crumbs lab" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <a href="/insights/">Insights</a> <span aria-hidden="true">/</span> <a href="/insights/?topic={slugify(a["topic"])}">{e(a["topic"])}</a></nav>
<h1 class="h1" style="margin-top:22px" data-reveal>{e(a["title"])}</h1>
<div class="article-meta" data-reveal><span class="lab">{e(a["author"])}</span><span class="lab">{fmt_date(a["date"])}</span><span class="lab">{a["minutes"]} min read</span></div></div></section>
<div class="wrap"><div class="pic article-img" data-reveal><img src="/assets/img/{a["image"]}.jpg" alt=""></div></div>
<div class="wrap article-layout">
<aside class="left"><div class="author">{av}<div><p class="h4" style="font-size:16px">{e(a["author"])}</p><p class="small">{e(bio)}</p></div></div><div><p class="lab" style="margin-bottom:10px">Share</p>{share}</div></aside>
<div><article class="prose">{a["html"]}</article>{nav}</div>
<aside class="right"><div class="card" style="background:#fff"><p class="lab">Talk to Windward</p><p class="h4">Hiring, or thinking about your next move?</p><p class="small">A confidential conversation with a specialist, on your schedule.</p><a class="btn sm" href="{CAL}" target="_blank" rel="noopener" style="align-self:flex-start;margin-top:6px">Book a call {ARROW}</a></div></aside></div>
<section class="sec white"><div class="wrap"><div class="head row"><div class="head" style="margin:0"><p class="lab">Keep reading</p><h2 class="h2">More from<br><span class="second">Windward Perspectives.</span></h2></div><a class="btn line" href="/insights/">All insights {ARROW}</a></div>
<div class="grid g3" style="gap:28px 16px">{"".join(post_card(r, i) for i, r in enumerate(related))}</div></div></section>{cta_band()}'''
        page(f'/insights/{a["slug"]}/', a['title'], a['excerpt'][:158], body, active='/insights/', img=f'/assets/img/{a["image"]}.jpg', kind='article', jsonld=ld, progress=True)
