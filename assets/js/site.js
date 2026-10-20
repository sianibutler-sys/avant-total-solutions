(function () {
  'use strict';
  document.documentElement.classList.add('js');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* Header: tighten on scroll */
  var header = $('#header');
  var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 12); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* Services dropdown */
  var svcWrap = $('#nav-services'), svcBtn = $('#services-toggle');
  function setSvc(open) { svcWrap.dataset.open = String(open); svcBtn.setAttribute('aria-expanded', String(open)); }
  svcBtn.addEventListener('click', function (e) { e.stopPropagation(); setSvc(svcWrap.dataset.open !== 'true'); });
  document.addEventListener('click', function (e) { if (!svcWrap.contains(e.target)) setSvc(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { setSvc(false); setMenu(false); } });

  /* Mobile menu */
  var menuBtn = $('#menu-btn'), menu = $('#mobile-menu');
  function setMenu(open) {
    menu.classList.toggle('open', open); menu.setAttribute('aria-hidden', String(!open));
    menuBtn.setAttribute('aria-expanded', String(open)); menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.style.overflow = open ? 'hidden' : '';
  }
  menuBtn.addEventListener('click', function () { setMenu(menu.getAttribute('aria-hidden') === 'true'); });
  $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });

  /* Hero mark: follows the pointer a little, each capsule at its own depth */
  var mark = $('#mark');
  if (mark && !reduce && window.matchMedia('(pointer: fine)').matches) {
    var parts = [[$('.p-amber', mark), 10], [$('.p-flame', mark), 18], [$('.p-navy', mark), 6]];
    var raf = 0;
    window.addEventListener('pointermove', function (e) {
      if (raf) return;
      raf = requestAnimationFrame(function () {
        raf = 0;
        var r = mark.getBoundingClientRect();
        var dx = (e.clientX - (r.left + r.width / 2)) / window.innerWidth;
        var dy = (e.clientY - (r.top + r.height / 2)) / window.innerHeight;
        parts.forEach(function (p) { if (p[0]) p[0].style.translate = (dx * p[1]) + 'px ' + (dy * p[1]) + 'px'; });
      });
    }, { passive: true });
  }

  /* Tabs helper with arrow-key support */
  function tabs(list, onSelect) {
    var btns = $$('[role="tab"]', list);
    function select(i, focus) {
      btns.forEach(function (b, j) {
        var on = i === j;
        b.setAttribute('aria-selected', String(on));
        b.tabIndex = on ? 0 : -1;
      });
      if (focus) btns[i].focus();
      onSelect(i, btns[i]);
    }
    btns.forEach(function (b, i) {
      b.addEventListener('click', function () { select(i, false); });
      b.addEventListener('keydown', function (e) {
        var n = btns.length, k = e.key, t = null;
        if (k === 'ArrowRight' || k === 'ArrowDown') t = (i + 1) % n;
        if (k === 'ArrowLeft' || k === 'ArrowUp') t = (i - 1 + n) % n;
        if (k === 'Home') t = 0;
        if (k === 'End') t = n - 1;
        if (t !== null) { e.preventDefault(); select(t, true); }
      });
    });
    return select;
  }

  /* Service track */
  var track = $('#track'), ind = $('#track-ind');
  var panels = $$('.panel');
  function moveInd(btn) {
    if (!btn) return;
    ind.style.width = btn.offsetWidth + 'px';
    ind.style.transform = 'translateX(' + btn.offsetLeft + 'px)';
  }
  var selectStage = tabs(track, function (i, btn) {
    panels.forEach(function (p, j) {
      var on = i === j;
      p.hidden = !on;
      if (on && !reduce) { p.classList.remove('entering'); void p.offsetWidth; p.classList.add('entering'); }
    });
    moveInd(btn);
    if (track.scrollWidth > track.clientWidth) {
      track.scrollTo({ left: btn.offsetLeft - 16, behavior: reduce ? 'auto' : 'smooth' });
    }
  });
  moveInd($('[aria-selected="true"]', track));
  window.addEventListener('resize', function () { moveInd($('[aria-selected="true"]', track)); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { moveInd($('[aria-selected="true"]', track)); });
  track.addEventListener('scroll', function () { moveInd($('[aria-selected="true"]', track)); }, { passive: true });

  $$('[data-stage]').forEach(function (a) {
    a.addEventListener('click', function () { selectStage(Number(a.dataset.stage), false); setSvc(false); });
  });

  /* Before / after */
  var cmp = $('#compare'), range = $('#compare-range');
  if (cmp && range) {
    var setPos = function () { cmp.style.setProperty('--pos', range.value + '%'); };
    range.addEventListener('input', setPos); setPos();
  }

  /* Client voices */
  var stage = $('#voice-stage');
  tabs($('#voice-pick'), function (i, btn) {
    var bq = document.createElement('blockquote');
    var p = document.createElement('p'); p.textContent = btn.dataset.q;
    var c = document.createElement('cite');
    var b = document.createElement('b'); b.textContent = btn.dataset.who;
    c.appendChild(b); c.appendChild(document.createTextNode(', ' + btn.dataset.where));
    bq.appendChild(p); bq.appendChild(c);
    if (!reduce) bq.className = 'entering';
    stage.replaceChildren(bq);
  });

  /* Service area */
  var detail = $('#state-detail');
  tabs($('#states'), function (i, btn) {
    $('h3', detail).textContent = btn.dataset.state;
    $('p', detail).textContent = btn.dataset.text;
  });

  /* Quote request: three steps */
  var form = $('#qform');
  var steps = $$('.fs', form);
  var heads = ['What do you need?', 'About the job', 'How do we reach you?'];
  var bars = $$('.progress span', form);
  var back = $('#back'), next = $('#next'), send = $('#send');
  var cur = 0;
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

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!valid(2)) return;
    var data = {
      services: $$('input[name="service"]:checked', form).map(function (c) { return c.value; }),
      zip: $('#q-zip').value.trim(), timeline: $('#q-when').value, message: $('#q-msg').value.trim(),
      name: $('#q-name').value.trim(), phone: $('#q-phone').value.trim(), email: $('#q-email').value.trim()
    };
    var endpoint = form.dataset.endpoint;
    var finish = function (text) {
      steps.forEach(function (s) { s.hidden = true; });
      $('#form-nav').hidden = true;
      $('.step-title', form).hidden = true;
      bars.forEach(function (b) { b.className = 'done'; });
      if (text) $('#done-text').textContent = text;
      $('#done').hidden = false;
    };
    if (!endpoint) { finish('Preview only: this form is not connected to email yet. On the live site it will send straight to hello@avanttotalsolutions.com.'); return; }
    send.disabled = true; send.textContent = 'Sending';
    fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { if (!r.ok) throw new Error(); finish(); })
      .catch(function () {
        send.disabled = false; send.textContent = 'Send request';
        var err = $('#err-2'); err.hidden = false;
        err.textContent = 'Your request did not send. Try again, or call or text 410-357-1406.';
      });
  });
})();
