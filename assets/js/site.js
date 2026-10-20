(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var play = function (v) { if (!v) return; var p = v.play(); if (p && p.catch) p.catch(function () {}); };

  /* Header */
  var header = $('#header');
  var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 12); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* Mobile menu */
  var menuBtn = $('#menu-btn'), menu = $('#mobile-menu');
  function setMenu(open) {
    menu.classList.toggle('open', open); menu.setAttribute('aria-hidden', String(!open));
    menuBtn.setAttribute('aria-expanded', String(open)); menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.style.overflow = open ? 'hidden' : '';
  }
  menuBtn.addEventListener('click', function () { setMenu(menu.getAttribute('aria-hidden') === 'true'); });
  $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });

  /* Services dropdown */
  var dd = $('#nav-dd'), ddBtn = $('#nav-dd-btn');
  if (dd) {
    var setDD = function (o) { dd.dataset.open = String(o); ddBtn.setAttribute('aria-expanded', String(o)); };
    ddBtn.addEventListener('click', function (e) { e.stopPropagation(); setDD(dd.dataset.open !== 'true'); });
    document.addEventListener('click', function (e) { if (!dd.contains(e.target)) setDD(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setDD(false); });
  }

  /* Page hero video on service pages */
  var phv = $('.page-hero video');
  if (phv) { if (reduce) phv.removeAttribute('autoplay'); else play(phv); }

  if ($('#hero-video')) {
  /* Hero video: respect reduced motion, offer pause */
  var hv = $('#hero-video'), tog = $('#video-toggle');
  function setHero(on) {
    if (on) play(hv); else hv.pause();
    tog.setAttribute('aria-label', on ? 'Pause background video' : 'Play background video');
    tog.innerHTML = '<svg><use href="#' + (on ? 'pause' : 'play') + '"/></svg>';
  }
  if (reduce) { hv.removeAttribute('autoplay'); setHero(false); } else { play(hv); }
  tog.addEventListener('click', function () { setHero(hv.paused); });

  }

  if ($('#svc')) {
  /* Services: one panel open, in job order */
  var items = $$('.svc-item'), caps = $$('#capsules span');
  var wide = window.matchMedia('(min-width: 981px)');
  function openSvc(i) {
    items.forEach(function (it, j) {
      var on = i === j;
      it.dataset.open = String(on);
      $('.svc-trigger', it).setAttribute('aria-expanded', String(on));
      var v = $('video', it);
      if (v) { if (on && !reduce && svcVisible && wide.matches) play(v); else v.pause(); }
    });
    caps.forEach(function (c, j) { c.classList.toggle('on', j === i); });
  }
  var svcVisible = false;
  items.forEach(function (it, i) {
    $('.svc-trigger', it).addEventListener('click', function () { openSvc(i); });
    it.addEventListener('mouseenter', function () { if (wide.matches) openSvc(i); });
  });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        svcVisible = e.isIntersecting;
        items.forEach(function (it) {
          var v = $('video', it); if (!v) return;
          var show = svcVisible && !reduce && wide.matches && it.dataset.open === 'true';
          if (show) play(v); else v.pause();
        });
      });
    }, { threshold: 0.2 }).observe($('#svc'));
  }
  $$('[data-open]').forEach(function (a) {
    if (a.classList.contains('svc-item')) return;
    a.addEventListener('click', function () { openSvc(Number(a.dataset.open)); });
  });

  }

  if ($('#proof-nav')) {
  /* Proof band video + reviews */
  var pv = $('#proof-video');
  if (pv && !reduce && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) play(pv); else pv.pause(); }); }, { threshold: 0.2 }).observe(pv.parentElement);
  }
  var stage = $('#proof-stage'), pnav = $('#proof-nav');
  var pbtns = $$('[role="tab"]', pnav);
  function pick(i, focus) {
    pbtns.forEach(function (b, j) { b.setAttribute('aria-selected', String(i === j)); b.tabIndex = i === j ? 0 : -1; });
    if (focus) pbtns[i].focus();
    var b = pbtns[i], bq = document.createElement('blockquote');
    var p = document.createElement('p'); p.textContent = b.dataset.q;
    var c = document.createElement('cite'), w = document.createElement('b');
    w.textContent = b.dataset.who; c.appendChild(w); c.appendChild(document.createTextNode(', ' + b.dataset.where));
    bq.appendChild(p); bq.appendChild(c); if (!reduce) bq.className = 'entering';
    stage.replaceChildren(bq);
  }
  pbtns.forEach(function (b, i) {
    b.addEventListener('click', function () { pick(i, false); });
    b.addEventListener('keydown', function (e) {
      var n = pbtns.length, t = null;
      if (e.key === 'ArrowRight') t = (i + 1) % n;
      if (e.key === 'ArrowLeft') t = (i - 1 + n) % n;
      if (t !== null) { e.preventDefault(); pick(t, true); }
    });
  });

  }

  if ($('#compare')) {
  /* Before and after */
  var cmp = $('#compare'), range = $('#compare-range');
  range.addEventListener('input', function () { cmp.style.setProperty('--pos', range.value + '%'); });
  var babtns = $$('#ba-tabs [role="tab"]');
  function pickBA(i, focus) {
    babtns.forEach(function (b, j) { b.setAttribute('aria-selected', String(i === j)); b.tabIndex = i === j ? 0 : -1; });
    if (focus) babtns[i].focus();
    var b = babtns[i];
    $('#ba-before').src = b.dataset.b; $('#ba-after').src = b.dataset.a;
    $('#ba-before').alt = 'Before: ' + b.dataset.cap; $('#ba-after').alt = 'After: ' + b.dataset.cap;
    $('#ba-cap').textContent = b.dataset.cap;
    var tags = $('#ba-tags'); tags.replaceChildren();
    b.dataset.tags.split('|').forEach(function (t) { var s = document.createElement('span'); s.textContent = t; tags.appendChild(s); });
    range.value = 50; cmp.style.setProperty('--pos', '50%');
  }
  babtns.forEach(function (b, i) {
    b.addEventListener('click', function () { pickBA(i, false); });
    b.addEventListener('keydown', function (e) {
      var n = babtns.length, t = null;
      if (e.key === 'ArrowRight') t = (i + 1) % n;
      if (e.key === 'ArrowLeft') t = (i - 1 + n) % n;
      if (t !== null) { e.preventDefault(); pickBA(t, true); }
    });
  });
  babtns.forEach(function (b) { [b.dataset.b, b.dataset.a].forEach(function (src) { var im = new Image(); im.src = src; }); });

  }

  if ($('#strip')) {
  /* Project filters and small before/after cards */
  var chips = $$('#proj-filters button');
  if (chips.length) {
    var cards = $$('.pcard'), count = $('#proj-count');
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        chips.forEach(function (o) { o.setAttribute('aria-pressed', String(o === c)); });
        var f = c.dataset.f, n = 0;
        cards.forEach(function (card) { var on = f === 'all' || card.dataset.cat === f; card.hidden = !on; if (on) n++; });
        count.textContent = n + (n === 1 ? ' project' : ' projects');
      });
    });
  }
  $$('.mini-compare').forEach(function (mc) {
    var r = $('input', mc);
    r.addEventListener('input', function () { mc.style.setProperty('--pos', r.value + '%'); });
  });

  /* Photo strip */
  var strip = $('#strip');
  var step = function (dir) { var f = $('figure', strip); strip.scrollBy({ left: dir * (f.offsetWidth + 14), behavior: reduce ? 'auto' : 'smooth' }); };
  $('#strip-prev').addEventListener('click', function () { step(-1); });
  $('#strip-next').addEventListener('click', function () { step(1); });

  }

  /* Service area */
  var sbtns = $$('#states button');
  sbtns.forEach(function (b) {
    b.addEventListener('click', function () {
      var open = b.getAttribute('aria-expanded') === 'true';
      sbtns.forEach(function (o) { o.setAttribute('aria-expanded', 'false'); });
      b.setAttribute('aria-expanded', String(!open));
    });
  });

  if ($('#qform')) {
  /* Quote request: three steps */
  var form = $('#qform'), steps = $$('.fs', form), bars = $$('.progress span', form);
  var heads = ['What do you need?', 'About the job', 'How do we reach you?'];
  var back = $('#back'), next = $('#next'), send = $('#send'), cur = 0;
  function show(n) {
    cur = n;
    steps.forEach(function (s, j) { s.hidden = j !== n; });
    bars.forEach(function (b, j) { b.className = j < n ? 'done' : (j === n ? 'now' : ''); });
    $('#step-heading').textContent = heads[n];
    $('#step-count').textContent = 'Step ' + (n + 1) + ' of 3';
    back.hidden = n === 0; next.hidden = n === 2; send.hidden = n !== 2;
  }
  function valid(n) {
    var ok = true;
    if (n === 0) ok = $$('input[name="service"]:checked', form).length > 0;
    if (n === 1) ok = !!($('#q-zip').value.trim() || $('#q-msg').value.trim());
    if (n === 2) ok = !!($('#q-name').value.trim() && ($('#q-phone').value.trim() || $('#q-email').value.trim()));
    $('#err-' + n).hidden = ok;
    return ok;
  }
  next.addEventListener('click', function () {
    if (!valid(cur)) return;
    show(cur + 1);
    var first = $('input, select, textarea', steps[cur]); if (first) first.focus();
  });
  back.addEventListener('click', function () { show(cur - 1); });
  $$('[data-pick]').forEach(function (a) {
    a.addEventListener('click', function () {
      $$('input[name="service"]', form).forEach(function (c) { if (c.value === a.dataset.pick) c.checked = true; });
    });
  });
  try {
    var want = new URLSearchParams(window.location.search).get('service');
    if (want) $$('input[name="service"]', form).forEach(function (c) { if (c.value === want) c.checked = true; });
  } catch (err) {}
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!valid(2)) return;
    var data = {
      services: $$('input[name="service"]:checked', form).map(function (c) { return c.value; }),
      zip: $('#q-zip').value.trim(), timeline: $('#q-when').value, message: $('#q-msg').value.trim(),
      name: $('#q-name').value.trim(), phone: $('#q-phone').value.trim(), email: $('#q-email').value.trim()
    };
    var finish = function (text) {
      steps.forEach(function (s) { s.hidden = true; });
      $('#form-nav').hidden = true; $('.step-title', form).hidden = true;
      bars.forEach(function (b) { b.className = 'done'; });
      if (text) $('#done-text').textContent = text;
      $('#done').hidden = false;
    };
    var endpoint = form.dataset.endpoint;
    if (!endpoint) { finish('Preview only: this form is not connected yet. On the live site it will deliver straight to Avant Total Solutions.'); return; }
    send.disabled = true; send.textContent = 'Sending';
    fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { if (!r.ok) throw new Error(); finish(); })
      .catch(function () {
        send.disabled = false; send.textContent = 'Send request';
        var err = $('#err-2'); err.hidden = false;
        err.textContent = 'Your request did not send. Try again, or call or text 410-357-1406.';
      });
  });
  }

})();
