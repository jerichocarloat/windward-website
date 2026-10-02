from common import *


def post_card(a, i=0, size='h3'):
    return f'''<a class="post-card" href="/insights/{a["slug"]}/" data-reveal style="--i:{i}"><div class="pic"><img src="/assets/img/{a["image"]}.jpg" alt="" loading="lazy"></div>
<div class="meta"><span class="tag">{e(a["topic"])}</span><span class="tag">{fmt_date(a["date"])}</span></div>
<h3 class="{size}">{e(a["title"])}</h3><p class="small">{e(a["author"])} · {a["minutes"]} min read</p></a>'''


def job_row(j, i=0):
    return f'''<a class="job" href="/jobs/{j["slug"]}/" data-reveal style="--i:{i}"><div><span class="tag">{e(j["family"])}</span><h3 style="margin-top:6px">{e(j["title"])}</h3></div>
<p class="loc small">{ic("Location",16,"ic")} {e(j["place"])}</p><p class="when small mono" style="font-size:13px">Posted {fmt_date(j["date"])}</p><span class="go" aria-hidden="true">{ARROW}</span></a>'''


def team_cards():
    return ''.join(f'''<div class="tm" id="{t["slug"]}" data-reveal style="--i:{i}"><div class="pic"><img src="/assets/img/{t["img"]}" alt="Portrait of {t["name"]}" loading="lazy"></div><div class="tm-b"><h3 class="h3">{t["name"]}</h3><p class="small">{t["role"]}</p>
<div class="tm-l"><a href="tel:{t["phone"]}">{ic("Phone",16,"")}<span>{t["phone"]}</span></a><a href="mailto:{t["email"]}">{ic("Email",16,"")}<span>{t["email"].replace("@","<wbr>@")}</span></a></div></div></div>''' for i, t in enumerate(TEAM))


def proof(white=False):
    items = [('45+', 'years', 'Combined recruiting experience across our team.'), ('500+', '', 'Executives placed in permanent roles.'), ('92%', '', 'Of the people we place stay seven years or more.'), ('9', '', 'Specialist practice areas across wealth and finance.')]
    cells = ''.join(f'<div class="pf" data-reveal style="--i:{i}"><span class="n">{n}</span><p>{t}</p></div>' for i, (n, u, t) in enumerate(items))
    return f'''<section class="sec proof{" white" if white else ""}"><div class="wrap"><div class="proof-head"><div class="proof-l"><p class="lab" data-reveal>Track record</p><p class="proof-t" data-reveal>The right hire should still feel right <span class="second">years later.</span></p></div><p class="proof-s" data-reveal>That is why we judge every search over years, not weeks. Here is what more than four decades of combined experience in wealth management and financial services adds up to.</p></div><div class="proof-row">{cells}</div></div></section>'''


def home(arts, jobs):
    statsh = proof()
    pillars = ''.join(f'''<div class="card pillar" data-reveal style="--i:{i}"><div style="display:flex;justify-content:space-between;align-items:center"><span class="roman">{ROMAN[i]}</span>{ic(icn,28)}</div>
<p class="lab" style="margin-top:22px">{k}</p><h3 class="h3">{t}</h3><p class="body small" style="color:var(--body)">{d}</p></div>''' for i, (k, t, d, icn) in enumerate(PILLARS))
    specs = ''.join(f'''<a class="spec card link" href="/employers/#{slugify(n)}" data-reveal style="--i:{i%3}"><div class="top">{ic(icn,30)}<span class="lab">{i+1:02d}</span></div><h3 class="h4" style="margin-top:14px">{n}</h3><p class="small">{d}</p></a>''' for i, (n, d, icn) in enumerate(SPECIALTIES))
    reasons = ''.join(f'''<li data-reveal style="--i:{i%2}"><span class="lab">{i+1:02d}</span><div style="display:flex;gap:14px;align-items:flex-start">{ic(icn,26)}<h3 class="h4">{n}</h3></div><p class="body">{d}</p></li>''' for i, (n, s, d, icn) in enumerate(REASONS))
    steps = [('Understand the ambition', 'We start with your goals, business context and culture. For a candidate, that means understanding where you want to go and what a better opportunity looks like.'),
             ('Find the right alignment', 'Specialist networks, proactive outreach and careful evaluation identify the people whose skills and expectations truly match the opportunity.'),
             ('Build for what comes next', 'We bring firm and candidate into a considered conversation, support the offer, and stay in touch long after the start date.')]
    approach = ''.join(f'''<div class="acc-item{" open" if i==0 else ""}" data-reveal style="--i:{i}"><h3><button class="acc-q" type="button" aria-expanded="{"true" if i==0 else "false"}" aria-controls="ap{i}"><span><span class="num">{i+1:02d}</span>{t}</span><span class="pm" aria-hidden="true"></span></button></h3><div class="acc-a" id="ap{i}" role="region"><div><div class="in body">{d}</div></div></div></div>''' for i, (t, d) in enumerate(steps))
    posts = ''.join(post_card(a, i) for i, a in enumerate(arts[:3]))
    jobsh = ''.join(job_row(j, i) for i, j in enumerate(sorted(jobs, key=lambda j: j['date'], reverse=True)[:5]))
    team = team_cards()
    body = f'''
<section class="hero"><div class="bg" style="background-image:url(/assets/img/hero.jpg)"></div><div class="shade"></div><div class="wrap"><div class="inner">
<p class="lab" style="color:#CBCDCF" data-fade>Executive search &amp; recruitment</p>
<h1 class="display"><span class="hl"><span style="--i:0">The right talent</span></span><span class="hl"><span class="second" style="--i:1">moves business forward.</span></span></h1>
<p class="pos" data-fade style="--i:1"><strong>Specialist recruiters for wealth management and financial services.</strong> We find the advisors, planners and leaders that RIAs, family offices, trust companies and asset managers build on.</p>
<div class="actions" data-fade style="--i:2"><a class="btn light" href="/employers/">Hire with Windward {ARROW}</a><a class="btn ghost" href="/jobs/">Find your next role</a></div></div>
<div class="rail" data-fade style="--i:3"><span>A member of Sanford Rose Associates®, the executive search network founded in 1959</span><a class="num" href="tel:{PHONE}">{PHONE}</a></div></div></section>

{statsh}

<section class="sec" style="padding-top:0"><div class="wrap split">
<div class="head"><p class="lab" data-reveal>01 / What we do</p><h2 class="h2" data-reveal>Executive search,<br><span class="second">built for wealth management.</span></h2></div>
<div style="display:flex;flex-direction:column;gap:18px"><p class="lede" style="color:var(--ink)" data-reveal>We recruit for one industry: the firms that look after other people’s money. That focus means we already know the people, the roles and the market before your search begins.</p>
<p class="body" data-reveal>From senior wealth advisors and planners to trust officers, operations leaders and executives, we find people whose skills and values fit your firm, including the many who are not actively looking. Firms also call us for an honest read on who is available, what a role should pay and what competitors are doing.</p>
<div class="actions" data-reveal><a class="tlink" href="/about/">More about Windward {ARROW}</a></div></div></div></section>

<section class="sec white"><div class="wrap">
<div class="head row"><div class="head" style="margin:0"><p class="lab" data-reveal>02 / Two doors</p><h2 class="h2" data-reveal>Two sides to every search.<br><span class="second">We work for both.</span></h2></div><p class="lede" style="max-width:44ch" data-reveal>A firm with a plan to grow, and a person with a career to build. The right hire works for both.</p></div>
<div class="grid g2">
 <div class="door" data-reveal><div class="pic"><img src="/assets/img/handshake.jpg" alt="Two professionals shaking hands after agreeing a hire" loading="lazy"></div><div class="txt"><p class="lab">For firms</p><h3 class="h3">Hire with the whole market in view.</h3><p class="body small">For RIAs, family offices, trust companies and financial services firms planning a critical hire, a successor or a growing team.</p><ul class="blist small"><li>{DIAM}A curated shortlist, not a stack of résumés</li><li>{DIAM}Honest reads on fit and compensation</li><li>{DIAM}Confidential searches when it matters</li></ul><div class="actions"><a class="btn" href="/employers/">Start a search {ARROW}</a></div></div></div>
 <div class="door" data-reveal style="--i:1"><div class="pic"><img src="/assets/img/next-move.jpg" alt="A professional crossing a city street on his way to work" loading="lazy"></div><div class="txt"><p class="lab">For professionals</p><h3 class="h3">Find a role worth moving for.</h3><p class="body small">For advisors, planners and wealth professionals who are ready for a new role, or simply open to hearing about the right one.</p><ul class="blist small"><li>{DIAM}A clear picture of the firm and the role</li><li>{DIAM}Your name shared only with your permission</li><li>{DIAM}Advice that puts your goals first</li></ul><div class="actions"><a class="btn" href="/candidates/">Share your résumé {ARROW}</a><a class="btn line" href="/jobs/">See open jobs</a></div></div></div>
</div></div></section>

<section class="sec"><div class="wrap">
<div class="head row"><div class="head" style="margin:0"><p class="lab" data-reveal>03 / Our promise</p><h2 class="h2" data-reveal>Good connections.<br><span class="second">Lasting impact.</span></h2></div><p class="lede" style="max-width:46ch" data-reveal>Four promises we keep in every search and every conversation.</p></div>
<div class="grid g4">{pillars}</div></div></section>

<section class="sec dark"><div class="wrap">
<div class="head row"><div class="head" style="margin:0"><p class="lab" data-reveal>04 / Expertise</p><h2 class="h2" data-reveal>Specialists in the roles<br><span class="second">that shape your business.</span></h2></div><a class="btn ghost" href="/employers/#expertise" data-reveal>See what we recruit {ARROW}</a></div>
<div class="grid g3">{specs}</div></div></section>

<section class="sec white"><div class="wrap split">
<div class="head" style="position:sticky;top:calc(var(--header) + 24px)"><p class="lab" data-reveal>05 / Why Windward</p><h2 class="h2" data-reveal>The details<br><span class="second">make the difference.</span></h2><p class="body" data-reveal>Six reasons firms trust us with the hires that matter most.</p><div class="actions" data-reveal><a class="btn" href="/employers/">Discuss your search {ARROW}</a></div></div>
<ul class="rows">{reasons}</ul></div></section>

<section class="sec"><div class="wrap split">
<div class="pic ratio-45" data-reveal><img src="/assets/img/conversation.jpg" alt="Two colleagues in conversation in a bright office" loading="lazy"></div>
<div><div class="head"><p class="lab" data-reveal>06 / Our approach</p><h2 class="h2" data-reveal>Listen closely. Look deeper.<br><span class="second">Connect thoughtfully.</span></h2><p class="lede" data-reveal>A deliberate process for a decision with lasting consequences.</p></div>
<div class="acc">{approach}</div><div class="actions" style="margin-top:28px" data-reveal><a class="btn" href="/contact/">Let’s talk about your search {ARROW}</a></div></div></div></section>

<section class="sec white"><div class="wrap">
<div class="head row"><div class="head" style="margin:0"><p class="lab" data-reveal>07 / Jobs</p><h2 class="h2" data-reveal>Open roles in<br><span class="second">wealth management.</span></h2></div><a class="btn line" href="/jobs/" data-reveal>See all {len(jobs)} jobs {ARROW}</a></div>
<div style="background:var(--fog);padding:8px">{jobsh.replace('class="job"','class="job" style="background:#fff"')}</div></div></section>

<section class="sec"><div class="wrap">
<div class="head row"><div class="head" style="margin:0"><p class="lab" data-reveal>08 / Windward Perspectives</p><h2 class="h2" data-reveal>What we’re seeing.<br><span class="second">What it means for you.</span></h2></div><a class="btn line" href="/insights/" data-reveal>All insights {ARROW}</a></div>
<div class="grid g3" style="gap:28px 16px">{posts}</div></div></section>

<section class="sec white"><div class="wrap">
<div class="head row"><div class="head" style="margin:0"><p class="lab" data-reveal>09 / The team</p><h2 class="h2" data-reveal>Meet the people<br><span class="second">behind the connections.</span></h2></div><a class="btn line" href="/about/#team" data-reveal>Contact the team {ARROW}</a></div>
<div class="grid g4 team-grid">{team}</div></div></section>

{faq_block()}
{cta_band()}'''
    page('/', 'Windward Recruiting | Executive Search for Wealth Management & Financial Services', 'Windward Recruiting is a specialist executive search firm for wealth management and financial services. The right talent moves business forward.', body, active='/', over=True,
         jsonld={"@context": "https://schema.org", "@type": "EmploymentAgency", "name": "Windward Recruiting", "url": SITE, "telephone": "+1-414-939-8700", "slogan": TAGLINE, "logo": SITE + "/assets/img/logo.png", "sameAs": [LINKEDIN], "description": "Executive search and recruitment for wealth management and financial services.", "memberOf": {"@type": "Organization", "name": "Sanford Rose Associates"}})


def about():
    team = team_cards()
    pillars = ''.join(f'''<li data-reveal style="--i:{i%2}"><span class="roman">{ROMAN[i]}</span><h3 class="h4">{k}<br><span class="second" style="font-weight:400">{t}</span></h3><p class="body">{d}</p></li>''' for i, (k, t, d, icn) in enumerate(PILLARS))
    std = [('Listen first.', 'Understand the ambition before recommending anything.'), ('Bring the market.', 'Arrive with context: talent availability, compensation, competition.'), ('Say the hard part.', 'Name the gap or the risk while it can still be addressed.'), ('Protect the name.', 'Anonymize by default. Share only with permission.'), ('Respect the time.', 'Short, structured, useful. No filler.'), ('Follow through.', 'Every candidate gets an answer. Every client gets an update.'), ('Influence, never pressure.', 'Persuade with clarity, never urgency.'), ('Think long term.', 'Every placement is an investment in continuity.')]
    stdh = ''.join(f'<div class="card" data-reveal style="--i:{i%4}"><span class="lab">{i+1:02d}</span><h3 class="h4" style="margin-top:10px">{t}</h3><p class="small">{d}</p></div>' for i, (t, d) in enumerate(std))
    body = intro('About Windward', 'A people business.', 'With a specialist’s perspective.', 'Windward Recruiting is an executive search and recruitment firm for wealth management and financial services. We bring deep industry context and a down-to-earth approach to the decisions that change firms and careers.', f'<a class="btn" href="#team">Meet the team {ARROW}</a><a class="btn line" href="{CAL}" target="_blank" rel="noopener">Book a call</a>', [('Home', '/'), ('About', None)]) + f'''
<div class="wrap"><div class="banner" data-reveal><img src="/assets/img/silhouette.jpg" alt="A professional silhouetted against office windows"></div></div>

<section class="sec"><div class="wrap split">
<div class="head"><p class="lab" data-reveal>01 / Our story</p><h2 class="h2" data-reveal>We know the market.<br><span class="second">We get to know you.</span></h2></div>
<div style="display:flex;flex-direction:column;gap:18px">
<p class="lede" style="color:var(--ink)" data-reveal>Windward Recruiting provides expert executive search and recruitment for the wealth management, legal and financial services industries, with a deep, national view of the recruiting landscape.</p>
<p class="body" data-reveal>We create deep, lasting relationships that yield distinct, prosperous results for our clients. We offer a thorough understanding and commitment to your needs, with a down-to-earth approach. Our diverse network and wide reach give us a unique insight that helps our clients hire the right people, at the right time. We never quit.</p>
<p class="body" data-reveal>We are not simply in the business of filling positions. We are in the business of understanding people, firms, markets and the relationships between them. Because we spend our time talking to the people who shape the industry, we bring our clients something a database cannot: context.</p>
<p class="h3" data-reveal style="margin-top:8px">Moving you forward.<br><span class="second">It’s what we do.</span></p></div></div></section>

{proof(white=True)}

<section class="sec" id="team"><div class="wrap">
<div class="head row"><div class="head" style="margin:0"><p class="lab" data-reveal>02 / The team</p><h2 class="h2" data-reveal>Meet the people<br><span class="second">behind the connections.</span></h2></div><p class="lede" style="max-width:40ch" data-reveal>Call or email any of us directly. You will always speak to a specialist.</p></div>
<div class="grid g4 team-grid">{team}</div></div></section>

<section class="sec dark"><div class="wrap split">
<div class="head"><p class="lab" data-reveal>03 / What we believe</p><h2 class="h2" data-reveal>Four promises<br><span class="second">you can hold us to.</span></h2><p class="body" data-reveal>Each one is something you can check. If a message, a search or a conversation does not live up to them, it is not Windward.</p></div>
<ul class="rows">{pillars}</ul></div></section>

<section class="sec"><div class="wrap">
<div class="head"><p class="lab" data-reveal>04 / The Windward standard</p><h2 class="h2" data-reveal>Every conversation<br><span class="second">should leave you glad you called.</span></h2></div>
<div class="grid g4">{stdh}</div></div></section>

<section class="sec white tight" id="network"><div class="wrap sra" data-reveal><p class="lab">05 / Our network</p><p class="sra-t">Windward is a member of <strong>Sanford Rose Associates®</strong>, a national network of independent executive search firms founded in 1959. You get personal service from our team, with national reach behind every search.</p></div></section>
{faq_block()}{cta_band()}'''
    page('/about/', 'About Windward Recruiting', 'Windward Recruiting is a relationship-driven executive search firm for wealth management, legal and financial services. Meet our team.', body, active='/about/')


