import json, shutil, os, re, datetime
from common import *
import pages_a, pages_b

SRC = os.path.dirname(os.path.abspath(__file__))
arts = json.load(open(os.path.join(SRC, '..', 'data', 'articles.json')))
jobs = pages_b.prep_jobs(json.load(open(os.path.join(SRC, '..', 'data', 'jobs.json'))))
ART_IMG = ['glasses-talk', 'interview-smile', 'notebook', 'high-rise', 'laptop-talk', 'focus', 'glass-roof', 'tower-up', 'clients', 'cafe-talk', 'glass-building', 'window-woman', 'library-exec', 'planning', 'coffee-talk', 'handshake-close', 'documents', 'advisor-meeting', 'street-walk', 'tax-docs', 'deal', 'desk-docs']
for a, im in zip(arts, ART_IMG): a['image'] = im

# clean dist (keep assets/img + fonts)
for p in os.listdir(DIST):
    if p not in ('assets','favicon-32.png','apple-touch-icon.png','icon-512.png','.nojekyll','CNAME'): shutil.rmtree(os.path.join(DIST, p)) if os.path.isdir(os.path.join(DIST, p)) else os.remove(os.path.join(DIST, p))
shutil.copy(f'{SRC}/style.css', f'{DIST}/assets/style.css')
shutil.copy(f'{SRC}/app.js', f'{DIST}/assets/app.js')

pages_a.home(arts, jobs); pages_a.about()
pages_b.employers(); pages_b.candidates(jobs); pages_b.contact(); pages_b.opportunities(jobs); pages_b.insights(arts)

# ---- search page
body = intro('Search', 'Find what', 'you need.', '', '', [('Home', '/'), ('Search', None)]) + f'''
<section class="sec" style="padding-top:0"><div class="wrap" data-site-search><div class="toolbar"><div class="field-search" style="flex:1;max-width:640px">{ic("Search",18,"")}<label class="sr" for="sq">Search the site</label><input id="sq" type="search" placeholder="Search pages, articles and jobs" autofocus></div><p class="lab" data-count role="status">Type to search pages, articles and roles</p></div><div data-results style="display:flex;flex-direction:column;gap:8px"></div></div></section>'''
page('/search/', 'Search', 'Search the Windward Recruiting website.', body)

# ---- privacy
pv = [('Who we are', 'Windward Recruiting is an executive search and recruitment firm for wealth management and financial services, and a member of the Sanford Rose Associates® network. You can reach us on 414-939-8700.'),
      ('What we collect', 'When you contact us, submit a search request or share your résumé, we collect the details you choose to give us: your name, contact details, employment information, the documents you upload and any message you write.'),
      ('How we use it', 'We use your information only to respond to you, to consider you for suitable opportunities, or to carry out a search you have asked us to run. We do not sell your information.'),
      ('Confidentiality for candidates', 'We never share your name or résumé with a hiring firm without your permission.'),
      ('Third-party services', 'Applications for specific roles are handled through our applicant tracking system, PCRecruiter. Call scheduling is handled by Calendly. These services process your information under their own privacy policies.'),
      ('Your choices', 'You can ask us at any time to see, correct or delete the information we hold about you. Call 414-939-8700 or email any member of our team.')]
body = intro('Privacy', 'Your information,', 'handled with care.', 'Discretion is one of our core promises. This notice explains, in plain words, what we collect and how we use it.', '', [('Home', '/'), ('Privacy', None)]) + '<section class="sec" style="padding-top:0"><div class="wrap"><ul class="rows">' + ''.join(f'<li><span class="lab">{i+1:02d}</span><h2 class="h4">{t}</h2><p class="body">{d}</p></li>' for i, (t, d) in enumerate(pv)) + '</ul></div></section>'
page('/privacy/', 'Privacy', 'How Windward Recruiting collects and uses personal information.', body)

# ---- site map page
groups = [('Windward', [('Home', '/'), ('About', '/about/'), ('Contact', '/contact/'), ('Search', '/search/'), ('Privacy', '/privacy/')]),
          ('Work with us', [('For employers', '/employers/'), ('For candidates', '/candidates/'), ('Jobs', '/jobs/')] + [(f'{j["title"]}, {j["place"]}', f'/jobs/{j["slug"]}/') for j in jobs]),
          ('Insights', [('All insights', '/insights/')] + [(a['title'], f'/insights/{a["slug"]}/') for a in arts])]
body = intro('Site map', 'Every page,', 'in one place.', '', '', [('Home', '/'), ('Site map', None)]) + '<section class="sec" style="padding-top:0"><div class="wrap grid g3" style="gap:40px">' + ''.join(f'<div><p class="lab" style="margin-bottom:14px">{g}</p><ul class="blist small">' + ''.join(f'<li>{DIAM}<a href="{u}">{e(n)}</a></li>' for n, u in items) + '</ul></div>' for g, items in groups) + '</div></section>'
page('/sitemap/', 'Site map', 'All pages on the Windward Recruiting website.', body)

# ---- 404
body = f'''<section class="sec"><div class="wrap" style="min-height:52vh;display:flex;flex-direction:column;justify-content:center;gap:22px"><p class="lab">Error 404</p><h1 class="display">This page has moved.<br><span class="second">Let’s find your way.</span></h1>
<p class="lede">The page you were looking for is not here. Try one of these, or search the site.</p><div class="actions"><a class="btn" href="/">Home {ARROW}</a><a class="btn line" href="/jobs/">Jobs</a><a class="btn line" href="/insights/">Insights</a><a class="btn line" href="/search/">Search</a></div></div></section>'''
page('/404.html', 'Page not found', 'Page not found.', body)
os.rename(f'{DIST}/404.html', f'{DIST}/404.html') if os.path.exists(f'{DIST}/404.html') else None

# ---- legacy redirects (old WordPress URLs -> new pages on the same domain)
LEG = {'/wealth-management/': '/contact/', '/financial-recruiting/': '/about/', '/executive-search/': '/employers/', '/search-request/': '/employers/', '/submit-resume/': '/candidates/',
       '/financial-positions/': '/jobs/', '/about-sanford-rose-associates/': '/about/#network', '/network/': '/about/#network', '/expertise/': '/employers/#expertise', '/opportunities/': '/jobs/', '/blog/': '/insights/', '/blog/page/2/': '/insights/', '/blog/page/3/': '/insights/', '/blog/page/4/': '/insights/',
       '/news_insights/': '/insights/', '/category/featured/': '/insights/', '/category/financial-services-insights/': '/insights/', '/category/windward-recruiting-blog/': '/insights/', '/category/windward-recruiting-blog/page/2/': '/insights/',
       '/category/windward-recruiting-blog/finance/': '/insights/', '/category/windward-recruiting-blog/finance/page/2/': '/insights/', '/category/uncategorized/': '/insights/',
       '/author/chris-windward/': '/insights/?author=chris-bisenius', '/author/chris-windward/page/2/': '/insights/?author=chris-bisenius', '/author/julianna/': '/insights/?author=julianna-king', '/author/andrewnextlevelexchange-com/': '/insights/?author=andrew-miller',
       '/tag/wealth-management/': '/insights/', '/tag/women/': '/insights/?topic=women-in-wealth', '/slide-page/why-choose-us/': '/#main', '/fusion_tb_category/page_title_bar/': '/', '/home/': '/', '/news-insights/': '/insights/'}
for j in jobs: LEG[f'/opportunities/{j["slug"]}/'] = f'/jobs/{j["slug"]}/'
for a in arts: LEG[f'/{a["slug"]}/'] = f'/insights/{a["slug"]}/'
for old, new in LEG.items():
    d = DIST + old; os.makedirs(d, exist_ok=True)
    open(d + 'index.html', 'w').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Redirecting…</title><meta name="robots" content="noindex"><link rel="canonical" href="{SITE}{new.split("?")[0].split("#")[0]}"><meta http-equiv="refresh" content="0; url={new}"><script>location.replace("{new}"+location.hash)</script></head><body style="font-family:system-ui;padding:40px">This page has moved to <a href="{new}">{new}</a>.</body></html>')
open(f'{DIST}/_redirects', 'w').write('\n'.join(f'{o}  {n}  301' for o, n in LEG.items()) + '\n/feed/  /insights/  301\n')
open(f'{DIST}/.htaccess', 'w').write('ErrorDocument 404 /404.html\nRewriteEngine On\n' + '\n'.join(f'RewriteRule ^{re.escape(o.strip("/"))}/?$ {n} [R=301,L,NE]' for o, n in LEG.items()) + '\n')

# ---- search index
idx = []
core = [('Home', '/', 'Executive search for wealth management and financial services.'), ('About Windward', '/about/', 'Our story, team, promises, standards and the Sanford Rose Associates network.'),
        ('For employers', '/employers/', 'What we recruit, how a search works and the search request.'), ('For candidates', '/candidates/', 'Submit your résumé in confidence.'), ('Jobs', '/jobs/', 'All open jobs.'), ('Insights', '/insights/', 'All articles.'),
        ('Contact', '/contact/', 'Book a 30-minute call, phone, forms and the team.'), ('Privacy', '/privacy/', 'How we handle your information.')]
for t, u, d in core:
    raw = open(DIST + u + 'index.html').read(); txt = ' '.join(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style|header|footer)[\s\S]*?</\1>', '', raw)).split())
    idx.append(dict(k='Page', t=t, u=u, d=d, b=txt[:4000]))
for t in TEAM: idx.append(dict(k='Team', t=t['name'], u=f'/about/#{t["slug"]}', d=f'{t["role"]} · {t["phone"]} · {t["email"]}', b=''))
for n, d, _ in SPECIALTIES: idx.append(dict(k='Expertise', t=n, u=f'/employers/#{slugify(n)}', d=d, b=''))
for a in arts: idx.append(dict(k='Article', t=a['title'], u=f'/insights/{a["slug"]}/', d=f'{a["author"]} · {fmt_date(a["date"])} · {a["excerpt"][:140]}', b=' '.join(re.sub(r'<[^>]+>', ' ', a['html']).split())[:6000]))
for j in jobs: idx.append(dict(k='Job', t=j['title'], u=f'/jobs/{j["slug"]}/', d=f'{j["place"]} · Posted {fmt_date(j["date"])}', b=' '.join(re.sub(r'<[^>]+>', ' ', j['html']).split())[:3000]))
json.dump(idx, open(f'{DIST}/search-index.json', 'w'), ensure_ascii=False)

# ---- sitemap.xml + robots
today = datetime.date.today().isoformat()
urls = [p for p in PAGES if p not in ('/404.html',)]
lm = {f'/insights/{a["slug"]}/': (a['modified'] or a['date']) for a in arts}
open(f'{DIST}/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{SITE}{u}</loc><lastmod>{lm.get(u, today)}</lastmod></url>\n' for u in urls) + '</urlset>\n')
open(f'{DIST}/robots.txt', 'w').write(f'User-agent: *\nAllow: /\nDisallow: /search/\nSitemap: {SITE}/sitemap.xml\n')

# ---- icons, manifest
open(f'{DIST}/favicon.svg', 'w').write(LG.tile_svg(S=64, r=0.74, mode='one'))
open(f'{DIST}/site.webmanifest', 'w').write(json.dumps({"name": "Windward Recruiting", "short_name": "Windward", "icons": [{"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}], "theme_color": "#0B0C0E", "background_color": "#F1F1F0", "display": "standalone"}))
print(len(PAGES), 'pages,', len(LEG), 'redirects,', len(idx), 'search entries')

open(os.path.join(DIST, '.nojekyll'), 'w').close()  # GitHub Pages: serve files as-is
