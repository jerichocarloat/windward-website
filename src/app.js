/* Windward Recruiting — interactions. Plain JS, no dependencies. */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Form delivery settings ------------------------------------------------
     FORM_ENDPOINT: set to your form service URL (for example Formspree, Basin or
     your own handler) to receive submissions including uploaded files.
     If the site is hosted on Netlify, the forms are also detected automatically.
     Without either, the form falls back to opening an email to FORM_EMAIL.      */
  var FORM_ENDPOINT = '';
  var FORM_EMAIL = 'chris@windwardrecruiting.com';

  /* ---- header state */
  var hdr = d.querySelector('.hdr');
  var hero = d.querySelector('.hero');
  function onScroll() {
    var y = window.scrollY || 0;
    if (hdr) {
      hdr.classList.toggle('scrolled', y > 8);
      if (hero && hdr.dataset.over === '1') {
        var limit = hero.offsetHeight - 72;
        hdr.classList.toggle('over', y < limit && !d.body.classList.contains('menu-open'));
      }
    }
    var bar = d.querySelector('.progress');
    var art = d.querySelector('.prose');
    if (bar && art) {
      var r = art.getBoundingClientRect();
      var total = art.offsetHeight - window.innerHeight * 0.6;
      var p = Math.min(1, Math.max(0, -r.top / Math.max(total, 1)));
      bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---- hero entrance */
  if (hero) requestAnimationFrame(function () { requestAnimationFrame(function () { hero.classList.add('ready'); }); });

  /* ---- reveal on scroll, both directions
     Elements fade and rise in as they enter the view, and fade back out as they
     leave it. The direction follows the scroll: content leaving at the top drifts
     up, content leaving at the bottom drifts down, so scrolling back up replays
     the motion naturally. */
  var items = d.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window && items.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var el = e.target;
        if (e.isIntersecting) {
          el.classList.add('in');
        } else if (el.classList.contains('in') || !el.dataset.seen) {
          var above = e.boundingClientRect.top < (e.rootBounds ? e.rootBounds.top : 0);
          el.setAttribute('data-side', above ? 'top' : 'bottom');
          el.classList.remove('in');
        }
        el.dataset.seen = '1';
      });
    }, { rootMargin: '-5% 0px -3% 0px', threshold: 0 });
    items.forEach(function (el) { io.observe(el); });
  } else { items.forEach(function (el) { el.classList.add('in'); }); }

  /* ---- smooth scrolling
     Trackpads, touch screens and high-refresh displays already scroll smoothly,
     so they keep the native scroll untouched (no added lag). Only a notched mouse
     wheel, which jumps in steps, is eased: a short, frame-rate independent glide
     (about 250 ms) that keeps up with the hand at 60, 120 or 144 Hz. */
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (fine && !reduce && 'requestAnimationFrame' in window) {
    var target = window.scrollY, current = window.scrollY, running = false, last = 0, rate = 16, padUntil = 0;
    var maxY = function () { return Math.max(0, root.scrollHeight - window.innerHeight); };
    var scrollable = function (el, dy) {
      while (el && el !== d.body && el !== root) {
        var cs = getComputedStyle(el), oy = cs.overflowY;
        if ((oy === 'auto' || oy === 'scroll') && el.scrollHeight > el.clientHeight + 1) {
          if ((dy > 0 && el.scrollTop + el.clientHeight < el.scrollHeight - 1) || (dy < 0 && el.scrollTop > 0)) return true;
        }
        el = el.parentElement;
      }
      return false;
    };
    var step = function (t) {
      var dt = Math.min(0.05, (t - last) / 1000 || 0.016); last = t;
      current += (target - current) * (1 - Math.exp(-rate * dt));
      if (Math.abs(target - current) < 0.5) { current = target; running = false; }
      window.scrollTo({ top: current, left: 0, behavior: 'instant' });
      if (running) requestAnimationFrame(step);
    };
    var go = function (y, r) {
      target = Math.max(0, Math.min(maxY(), y)); rate = r || 16;
      if (!running) { current = window.scrollY; running = true; last = performance.now(); requestAnimationFrame(step); }
    };
    var isWheelNotch = function (e) {
      if (e.deltaMode === 1 || e.deltaMode === 2) return true;
      if (e.deltaX !== 0 || e.timeStamp < padUntil) return false;
      var w = e.wheelDeltaY;
      if (typeof w === 'number' && w !== 0) {
        if (Math.abs(w) === Math.abs(e.deltaY) * 3) { padUntil = e.timeStamp + 1200; return false; } /* macOS trackpad */
        return Math.abs(w) % 120 === 0 && Math.abs(e.deltaY) >= 40;
      }
      return Math.abs(e.deltaY) >= 50 && Number.isInteger(e.deltaY);
    };
    window.addEventListener('wheel', function (e) {
      if (e.defaultPrevented || e.ctrlKey || e.metaKey || d.body.classList.contains('menu-open')) return;
      if (!isWheelNotch(e)) { if (running) { running = false; target = current = window.scrollY; } return; }
      var dy = e.deltaY * (e.deltaMode === 1 ? 40 : e.deltaMode === 2 ? window.innerHeight : 1);
      if (scrollable(e.target, dy)) return;
      e.preventDefault();
      if (!running) target = window.scrollY;
      go(target + dy, 16);
    }, { passive: false });
    /* keep in step with keyboard, scrollbar drags and find-in-page */
    window.addEventListener('scroll', function () { if (!running) { target = current = window.scrollY; } }, { passive: true });
    ['keydown', 'mousedown', 'touchstart'].forEach(function (t) { window.addEventListener(t, function () { if (running) { running = false; target = current = window.scrollY; } }, { passive: true }); });
    /* same-page links glide to their section, below the sticky header */
    d.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href*="#"]');
      if (!a || e.metaKey || e.ctrlKey || e.shiftKey) return;
      var url = new URL(a.href, location.href);
      if (url.pathname !== location.pathname || !url.hash || url.hash.length < 2) return;
      var el = d.getElementById(decodeURIComponent(url.hash.slice(1)));
      if (!el) return;
      e.preventDefault();
      var off = (hdr ? hdr.offsetHeight : 0) + 16;
      go(el.getBoundingClientRect().top + window.scrollY - off, 7);
      if (history.pushState) history.pushState(null, '', url.hash);
    });
  }

  /* ---- mobile menu */
  var btn = d.querySelector('.menu-btn'), mnav = d.getElementById('mnav');
  function setMenu(open) {
    d.body.classList.toggle('menu-open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    mnav.setAttribute('aria-hidden', open ? 'false' : 'true');
    if ('inert' in mnav) mnav.inert = !open;
    onScroll();
    if (open) { var f = mnav.querySelector('a'); f && f.focus({ preventScroll: true }); }
    else btn.focus({ preventScroll: true });
  }
  if (btn && mnav) {
    if ('inert' in mnav) mnav.inert = true;
    btn.addEventListener('click', function () { setMenu(!d.body.classList.contains('menu-open')); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && d.body.classList.contains('menu-open')) setMenu(false); });
    window.addEventListener('resize', function () { if (window.innerWidth > 1060 && d.body.classList.contains('menu-open')) setMenu(false); });
  }

  /* ---- accordions */
  d.querySelectorAll('.acc-q').forEach(function (q) {
    q.addEventListener('click', function () {
      var item = q.closest('.acc-item'), open = !item.classList.contains('open');
      item.classList.toggle('open', open);
      q.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  /* ---- tabs */
  d.querySelectorAll('[role="tablist"]').forEach(function (list) {
    var tabs = list.querySelectorAll('[role="tab"]');
    function select(t) {
      tabs.forEach(function (x) {
        var on = x === t; x.setAttribute('aria-selected', on ? 'true' : 'false'); x.tabIndex = on ? 0 : -1;
        var p = d.getElementById(x.getAttribute('aria-controls')); if (p) p.hidden = !on;
      });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); history.replaceState(null, '', '#' + t.dataset.hash); });
      t.addEventListener('keydown', function (e) {
        var n = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (n) { var nx = tabs[(i + n + tabs.length) % tabs.length]; nx.focus(); select(nx); }
      });
    });
    var h = location.hash.slice(1);
    tabs.forEach(function (t) { if (t.dataset.hash === h) select(t); });
  });

  /* ---- filterable lists (insights + opportunities) */
  d.querySelectorAll('[data-filter-root]').forEach(function (rootEl) {
    var input = rootEl.querySelector('[data-filter-input]');
    var chips = rootEl.querySelectorAll('[data-chip]');
    var list = rootEl.querySelectorAll('[data-item]');
    var count = rootEl.querySelector('[data-count]');
    var empty = rootEl.querySelector('[data-empty]');
    var noun = rootEl.dataset.noun || 'items';
    var active = { };
    var qs = new URLSearchParams(location.search);
    chips.forEach(function (c) {
      var g = c.dataset.group, v = c.dataset.chip;
      if (qs.get(g) === v) { active[g] = v; }
    });
    if (input && qs.get('q')) input.value = qs.get('q');
    function apply(animate) {
      var term = input ? input.value.trim().toLowerCase() : '';
      var shown = 0;
      chips.forEach(function (c) {
        var g = c.dataset.group, v = c.dataset.chip;
        c.setAttribute('aria-pressed', (active[g] || 'all') === v ? 'true' : 'false');
      });
      list.forEach(function (el) {
        var ok = (!term || el.dataset.search.indexOf(term) > -1);
        Object.keys(active).forEach(function (g) { if (active[g] && active[g] !== 'all' && (el.dataset[g] || '').split('|').indexOf(active[g]) < 0) ok = false; });
        el.classList.toggle('is-hidden', !ok);
        if (ok) {
          shown++;
          if (animate && !reduce) { el.classList.remove('fade-in'); void el.offsetWidth; el.classList.add('fade-in'); }
        }
      });
      if (count) count.textContent = shown + ' ' + (shown === 1 ? noun.replace(/s$/, '') : noun);
      if (empty) empty.classList.toggle('is-hidden', shown > 0);
      var p = new URLSearchParams();
      if (term) p.set('q', term);
      Object.keys(active).forEach(function (g) { if (active[g] && active[g] !== 'all') p.set(g, active[g]); });
      var s = p.toString(); history.replaceState(null, '', location.pathname + (s ? '?' + s : '') + location.hash);
    }
    chips.forEach(function (c) { c.addEventListener('click', function () { active[c.dataset.group] = c.dataset.chip; apply(true); }); });
    if (input) { var t; input.addEventListener('input', function () { clearTimeout(t); t = setTimeout(function () { apply(false); }, 90); }); }
    apply(false);
  });

  /* ---- site search */
  var sroot = d.querySelector('[data-site-search]');
  if (sroot) {
    var sin = sroot.querySelector('input'), out = sroot.querySelector('[data-results]'), cnt = sroot.querySelector('[data-count]');
    var data = [];
    fetch('/search-index.json').then(function (r) { return r.json(); }).then(function (j) {
      data = j; var q0 = new URLSearchParams(location.search).get('q'); if (q0) sin.value = q0; run();
    });
    function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    function run() {
      var q = sin.value.trim().toLowerCase(), words = q.split(/\s+/).filter(Boolean);
      var res = !words.length ? [] : data.map(function (it) {
        var hay = (it.t + ' ' + it.d + ' ' + it.b).toLowerCase(), score = 0;
        for (var i = 0; i < words.length; i++) { var w = words[i]; if (hay.indexOf(w) < 0) return null; if (it.t.toLowerCase().indexOf(w) > -1) score += 5; score += 1; }
        return { it: it, s: score };
      }).filter(Boolean).sort(function (a, b) { return b.s - a.s; });
      cnt.textContent = words.length ? res.length + (res.length === 1 ? ' result' : ' results') : 'Type to search pages, articles and roles';
      out.innerHTML = res.slice(0, 60).map(function (r) {
        return '<a class="job fade-in" href="' + r.it.u + '"><div><span class="tag">' + esc(r.it.k) + '</span><h3 style="margin-top:6px">' + esc(r.it.t) + '</h3></div><p class="small" style="grid-column:span 2">' + esc(r.it.d) + '</p><span class="go" aria-hidden="true">' + ARROW + '</span></a>';
      }).join('');
      history.replaceState(null, '', location.pathname + (q ? '?q=' + encodeURIComponent(q) : ''));
    }
    var ARROW = '<svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 11 11 3M4.5 3H11v6.5"/></svg>';
    var tt; sin.addEventListener('input', function () { clearTimeout(tt); tt = setTimeout(run, 80); });
  }

  /* ---- copy link */
  d.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var u = location.href.split('#')[0];
      (navigator.clipboard ? navigator.clipboard.writeText(u) : Promise.reject()).then(function () {
        b.setAttribute('aria-label', 'Link copied'); b.classList.add('done');
        var tip = b.querySelector('.tip'); if (tip) { tip.textContent = 'Copied'; setTimeout(function () { tip.textContent = ''; }, 1600); }
      }).catch(function () { window.prompt('Copy this link', u); });
    });
  });

  /* ---- file inputs: show chosen file name */
  d.querySelectorAll('.file input[type=file]').forEach(function (inp) {
    inp.addEventListener('change', function () {
      var lbl = inp.closest('.file').querySelector('[data-file-label]');
      var f = inp.files && inp.files[0];
      if (f && f.size > 50 * 1024 * 1024) { alertField(inp, 'This file is larger than 50 MB.'); inp.value = ''; return; }
      if (lbl) lbl.textContent = f ? f.name + ' · ' + Math.max(1, Math.round(f.size / 1024)) + ' KB' : lbl.dataset.default;
    });
  });
  function alertField(el, msg) {
    var f = el.closest('.fld'); if (!f) return;
    f.classList.add('invalid'); var e = f.querySelector('.err'); if (e) e.textContent = msg;
  }

  /* ---- forms */
  d.querySelectorAll('form[data-form]').forEach(function (form) {
    form.setAttribute('novalidate', '');
    form.addEventListener('input', function (e) { var f = e.target.closest('.fld'); if (f && e.target.checkValidity()) f.classList.remove('invalid'); });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var firstBad = null;
      form.querySelectorAll('input,select,textarea').forEach(function (el) {
        var f = el.closest('.fld'); if (!f) return;
        var ok = el.checkValidity();
        if (el.type === 'radio') { ok = !!form.querySelector('input[name="' + el.name + '"]:checked') || !el.required; }
        f.classList.toggle('invalid', !ok);
        if (!ok) { var er = f.querySelector('.err'); if (er && !er.textContent) er.textContent = el.type === 'email' ? 'Please enter a valid email address.' : 'Please complete this field.'; if (!firstBad) firstBad = el; }
      });
      if (firstBad) { firstBad.focus(); return; }
      var wrap = form.closest('.form-wrap');
      var btnS = form.querySelector('[type=submit]'); btnS.disabled = true; var old = btnS.innerHTML; btnS.textContent = 'Sending…';
      var fd = new FormData(form);
      var onNetlify = /netlify\.app$/.test(location.hostname) || form.hasAttribute('data-netlify-live');
      var target = FORM_ENDPOINT || (onNetlify ? '/' : '');
      function done() { wrap.classList.add('sent'); wrap.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' }); }
      if (target) {
        fetch(target, { method: 'POST', body: fd, headers: { 'Accept': 'application/json' } })
          .then(function (r) { if (!r.ok) throw 0; done(); })
          .catch(function () { mailFallback(form, fd); wrap.classList.add('via-mail'); done(); })
          .finally(function () { btnS.disabled = false; btnS.innerHTML = old; });
      } else { mailFallback(form, fd); wrap.classList.add('via-mail'); btnS.disabled = false; btnS.innerHTML = old; done(); }
    });
  });
  function mailFallback(form, fd) {
    var lines = [], hasFile = false;
    fd.forEach(function (v, k) {
      if (k === 'form-name' || k === 'bot-field') return;
      if (v instanceof File) { if (v.name) { hasFile = true; lines.push(k + ': ' + v.name + ' (please attach)'); } return; }
      lines.push(k + ': ' + v);
    });
    if (hasFile) lines.push('', 'Please attach your file to this email before sending.');
    var subj = form.dataset.subject || 'Website enquiry';
    location.href = 'mailto:' + FORM_EMAIL + '?subject=' + encodeURIComponent(subj) + '&body=' + encodeURIComponent(lines.join('\n'));
  }

  /* ---- prefill from ?role= */
  (function () {
    var role = new URLSearchParams(location.search).get('role'); if (!role) return;
    var nice = /[\s,]/.test(role) ? role : role.replace(/-/g, ' ').replace(/\b\w/g, function (c) { return c.toUpperCase(); });
    d.querySelectorAll('input[name="role_sought"]').forEach(function (i) { if (!i.value) i.value = nice; });
    d.querySelectorAll('select[name="position_type"]').forEach(function (sel) {
      for (var k = 0; k < sel.options.length; k++) { if (sel.options[k].text.toLowerCase().replace(/[^a-z0-9]+/g, '-') === role) sel.selectedIndex = k; }
    });
  })();

  /* ---- inline booking calendar (falls back to the link if it cannot load) */
  d.querySelectorAll('[data-cal]').forEach(function (el) {
    if (window.WW_PREVIEW) return;
    var f = d.createElement('iframe');
    f.title = 'Book a 30-minute call with Windward Recruiting';
    f.loading = 'lazy';
    f.hidden = true;
    f.src = el.getAttribute('data-cal') + '?embed_domain=' + encodeURIComponent(location.hostname) + '&embed_type=Inline&hide_gdpr_banner=1';
    f.addEventListener('load', function () {
      f.hidden = false; el.classList.add('live');
      var fb = el.querySelector('.cal-fallback'); if (fb) fb.hidden = true;
    });
    el.appendChild(f);
  });

  /* ---- year */
  d.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
