"""Prefix every root-relative link in dist/ with a base path.

GitHub Pages serves a project repository at /<repo-name>/, so links such as
/assets/style.css must become /<repo-name>/assets/style.css. The deploy workflow
runs this automatically; on a custom domain the base path is empty and nothing
changes. Usage: python3 tools/base_path.py /windward-website [dist]
"""
import os, re, sys

base = (sys.argv[1] if len(sys.argv) > 1 else '').rstrip('/')
root = sys.argv[2] if len(sys.argv) > 2 else 'dist'
if not base:
    print('No base path: nothing to do.'); sys.exit(0)
if not base.startswith('/'): base = '/' + base

P = '(?!/)'  # not protocol-relative //
rules = [
    (re.compile(r'((?:href|src|action|poster)=")/' + P), r'\1' + base + '/'),
    (re.compile(r"((?:href|src|action)=')/" + P), r'\1' + base + '/'),
    (re.compile(r'(url\()/' + P), r'\1' + base + '/'),
    (re.compile(r'(url=)/' + P), r'\1' + base + '/'),
    (re.compile(r'(location\.replace\(")/' + P), r'\1' + base + '/'),
    (re.compile(r'("u"\s*:\s*")/' + P), r'\1' + base + '/'),
    (re.compile(r"'/search-index\.json"), "'" + base + "/search-index.json"),
]
n = 0
for dp, _, fs in os.walk(root):
    for f in fs:
        if not f.endswith(('.html', '.css', '.js', '.json', '.webmanifest', '.xml')): continue
        p = os.path.join(dp, f); s = open(p, encoding='utf-8').read(); o = s
        if f.endswith('.webmanifest'):
            s = re.sub(r'("(?:src|start_url|scope)"\s*:\s*")/' + P, r'\1' + base + '/', s)
        elif not f.endswith('.xml'):
            for rx, rep in rules: s = rx.sub(rep, s)
        if s != o: open(p, 'w', encoding='utf-8').write(s); n += 1
print(f'Base path {base} applied to {n} files.')
