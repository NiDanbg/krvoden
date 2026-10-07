/* ПРОЖЕКТОР: движение и поведение.
   Плавен скрол: Lenis. Скрол сцени: GSAP + ScrollTrigger. Без тях страницата
   остава четима и работеща; при prefers-reduced-motion движението се изключва.
   Поведението на сайта (меню, търсене, бисквитки, език) е запазено. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const lang = window.SITE_LANG || 'en';
  const T = (k, en) => (lang === 'bg' && window.SITE_BG && window.SITE_BG[k]) || en;
  const G = window.gsap, ST = window.ScrollTrigger;
  if (G && ST) G.registerPlugin(ST);
  const anim = !!(G && ST) && !reduce;
  const root = document.documentElement;
  const seen = root.classList.contains('seen');
  const introDelay = (seen || reduce) ? 0.05 : 2.05;
  const page = document.body.dataset.page || 'home';

  /* ---------- Плавен скрол ---------- */
  let lenis = null;
  if (window.Lenis && !reduce) {
    lenis = new window.Lenis({ lerp: 0.085, smoothWheel: true });
    if (anim) {
      lenis.on('scroll', ST.update);
      G.ticker.add(t => lenis.raf(t * 1000));
      G.ticker.lagSmoothing(0);
    } else {
      const raf = t => { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }
  }
  $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    const id = a.getAttribute('href');
    const t = id.length > 1 ? $(id) : null;
    if (!t) return;
    e.preventDefault();
    closeMenu();
    lenis ? lenis.scrollTo(t, { offset: -60 }) : t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
  }));

  /* ---------- Навигация ---------- */
  const nav = $('.nav'), sentinel = $('[data-nav-sentinel]');
  if (sentinel && 'IntersectionObserver' in window) {
    new IntersectionObserver(([e]) => nav.classList.toggle('solid', !e.isIntersecting)).observe(sentinel);
  } else nav.classList.add('solid');
  if (lenis) lenis.on('scroll', e => nav.classList.toggle('hide', e.direction === 1 && e.scroll > 700 && !$('.menu-overlay.active')));

  const menu = $('.menu-overlay'), hb = $('.hamburger');
  function closeMenu() {
    if (!menu || !menu.classList.contains('active')) return;
    menu.classList.remove('active'); hb.classList.remove('active'); hb.setAttribute('aria-expanded', 'false');
    lenis && lenis.start();
  }
  if (hb && menu) hb.addEventListener('click', () => {
    const o = menu.classList.toggle('active'); hb.classList.toggle('active', o); hb.setAttribute('aria-expanded', o);
    lenis && (o ? lenis.stop() : lenis.start());
  });

  /* ---------- Търсене (в макета: по заглавия; истинското остава в assets/site.js) ---------- */
  const BOOKS = [
    { en: 'The Gnostic Cipher', bg: 'Гностичният Шифър', g: ['Techno-Thriller, Global Conspiracy', T('g.cipher')], c: ['en/the-gnostic-cipher.webp', 'bg/Cover-gnostichnia-shifar-_bg.webp'] },
    { en: 'The Tree of Consciousness', bg: 'Дървото на съзнанието', g: ['Techno-Thriller, Global Conspiracy', T('g.tree')], c: ['en/the-tree-of-consciousness.webp', 'bg/Cover-dyrvoto-na-syznanieto-BG.webp'] },
    { en: 'The Seed of Eden', bg: 'Семето на Едем', g: ['Sci-fi conspiracy thriller', T('g.seed')], c: ['en/The_Seed_of_Eden.webp', 'bg/SEmeto-na-edem-bg.webp'] },
    { en: 'The Tuzo Anomaly', bg: 'Аномалията Тузо', g: ['A Techno-Apocalyptic Thriller', T('g.tuzo')], c: ['en/the-tuzo-anomaly.webp', 'bg/Anomaliata-Tuzo-BG.webp'] },
    { en: 'Square Knot', bg: 'Квадратен възел', g: ['Balkan noir', T('g.knot')], c: ['en/Square-Knot-EN_.webp', 'bg/---5.58.5.webp'] }
  ];
  const so = $('.search-overlay'), sin = so && $('.search-input', so), sres = so && $('.search-results', so);
  const li = lang === 'bg' ? 1 : 0;
  function openSearch(o) {
    so.classList.toggle('open', o);
    if (o) { lenis && lenis.stop(); setTimeout(() => sin.focus(), 120); } else { lenis && lenis.start(); }
  }
  if (so) {
    $$('.search-toggle').forEach(b => b.addEventListener('click', () => openSearch(true)));
    $('.close', so).addEventListener('click', () => openSearch(false));
    addEventListener('keydown', e => { if (e.key === 'Escape') { openSearch(false); closeMenu(); } });
    sin.addEventListener('input', () => {
      const q = sin.value.trim().toLowerCase();
      if (!q) { sres.hidden = true; return; }
      const hits = BOOKS.filter(b => (b.en + ' ' + b.bg).toLowerCase().includes(q));
      sres.hidden = false;
      sres.innerHTML = hits.length
        ? hits.map(b => `<a class="search-hit" href="#"><img src="../../images/${b.c[li]}" alt=""><span><span class="search-title">${[b.en, b.bg][li]}</span><span class="search-series">${b.g[li]}</span></span></a>`).join('')
        : `<div class="search-empty">${T('search.none', 'Nothing found')}</div>`;
    });
  }

  /* ---------- Бисквитки ---------- */
  const cb = $('#cookie-banner');
  if (cb) {
    let ok = false; try { ok = localStorage.getItem('pz-cookie') === '1'; } catch (e) {}
    if (!ok) setTimeout(() => cb.classList.add('show'), seen ? 900 : 3600);
    $('#cookie-accept-btn').addEventListener('click', () => { cb.classList.remove('show'); try { localStorage.setItem('pz-cookie', '1'); } catch (e) {} });
  }

  /* ---------- Проявяване, наклон ---------- */
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' });
    $$('[data-reveal]').forEach(el => io.observe(el));
  } else $$('[data-reveal]').forEach(el => el.classList.add('is-in'));

  if (fine) $$('[data-tilt]').forEach(el => {
    const max = +el.dataset.tilt || 9;
    el.addEventListener('pointermove', e => {
      const r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      el.classList.add('live');
      el.style.setProperty('--ry', ((x - .5) * 2 * max).toFixed(2) + 'deg');
      el.style.setProperty('--rx', (-(y - .5) * 2 * max).toFixed(2) + 'deg');
      el.style.setProperty('--mx', (x * 100).toFixed(1) + '%');
      el.style.setProperty('--my', (y * 100).toFixed(1) + '%');
    });
    el.addEventListener('pointerleave', () => {
      el.classList.remove('live');
      el.style.setProperty('--ry', '0deg'); el.style.setProperty('--rx', '0deg');
    });
  });

  /* ---------- Помощни ---------- */
  function splitChars(el) {
    const text = el.textContent.trim();
    el.setAttribute('aria-label', text);
    el.textContent = '';
    const chars = [];
    text.split(/\s+/).forEach(w => {
      const ws = document.createElement('span'); ws.className = 'word'; ws.setAttribute('aria-hidden', 'true');
      [...w].forEach(c => { const cs = document.createElement('span'); cs.className = 'char'; cs.textContent = c; ws.appendChild(cs); chars.push(cs); });
      el.appendChild(ws);
    });
    return chars;
  }
  function splitWords(el) {
    const text = el.textContent.trim();
    el.setAttribute('aria-label', text);
    el.textContent = '';
    return text.split(/\s+/).map(w => { const s = document.createElement('span'); s.className = 'w'; s.setAttribute('aria-hidden', 'true'); s.textContent = w; el.appendChild(s); return s; });
  }
  function initDust(box, tintOf) {
    const cv = $('.dust', box); if (!cv || reduce) return;
    const ctx = cv.getContext('2d'); const DPR = Math.min(devicePixelRatio || 1, 2);
    let W = 0, H = 0;
    const size = () => { W = cv.clientWidth; H = cv.clientHeight; cv.width = W * DPR; cv.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0); };
    size(); addEventListener('resize', size);
    const N = innerWidth < 700 ? 46 : 110;
    const ps = Array.from({ length: N }, () => ({ x: Math.random(), y: Math.random(), r: Math.random() * 1.5 + .4, vx: (Math.random() - .3) * .00007, vy: -Math.random() * .00006 - .00002, a: Math.random() * .55 + .15, p: Math.random() * 6.28, d: Math.random() * .7 + .4 }));
    let run = false, last = 0;
    const frame = t => {
      if (!run) return;
      const dt = Math.min(50, t - last); last = t;
      const rgb = tintOf();
      ctx.clearRect(0, 0, W, H);
      for (const p of ps) {
        p.x += p.vx * dt * (.5 + p.d); p.y += p.vy * dt * (.5 + p.d); p.p += dt * .0016;
        if (p.y < -.03) { p.y = 1.03; p.x = Math.random(); }
        if (p.x > 1.03) p.x = -.03; if (p.x < -.03) p.x = 1.03;
        const al = p.a * (.3 + .7 * (Math.sin(p.p) + 1) / 2), px = p.x * W, py = p.y * H, r = p.r * 4;
        const g = ctx.createRadialGradient(px, py, 0, px, py, r);
        g.addColorStop(0, `rgba(${rgb},${al})`); g.addColorStop(1, `rgba(${rgb},0)`);
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(px, py, r, 0, 6.283); ctx.fill();
      }
      requestAnimationFrame(frame);
    };
    new IntersectionObserver(([e]) => { run = e.isIntersecting; if (run) { last = performance.now(); requestAnimationFrame(frame); } }).observe(box);
  }
  function pointerParallax(box, layers) {
    if (!anim || !fine) return;
    const qs = layers.map(l => ({ els: $$(l.sel, box), amt: l.amt })).map(l => ({ amt: l.amt, x: l.els.map(el => G.quickTo(el, 'x', { duration: 1.3, ease: 'power3.out' })), y: l.els.map(el => G.quickTo(el, 'y', { duration: 1.3, ease: 'power3.out' })) }));
    box.addEventListener('pointermove', e => {
      const r = box.getBoundingClientRect(), nx = (e.clientX - r.left) / r.width - .5, ny = (e.clientY - r.top) / r.height - .5;
      qs.forEach(l => { l.x.forEach(f => f(nx * l.amt)); l.y.forEach(f => f(ny * l.amt * .7)); });
    });
  }

  /* ---------- ГЛАВНА: сцена ---------- */
  const hero = $('.hero');
  if (hero) {
    const scenes = $$('.scene', hero), chaps = $$('.chap', hero);
    let cur = 0, prog = null;
    const tintOf = () => scenes[cur].dataset.tint;
    initDust(hero, tintOf);

    if (!anim) {
      hero.classList.add('ready');
      chaps.forEach((c, i) => c.addEventListener('click', () => { cur = i; scenes.forEach((s, k) => s.classList.toggle('is-active', k === i)); chaps.forEach((x, k) => x.classList.toggle('is-active', k === i)); }));
    } else {
      const sets = scenes.map(s => splitChars($('.h-title', s)));
      sets.forEach(cs => G.set(cs, { yPercent: 115 }));
      const show = (i, first) => {
        const prev = first ? null : scenes[cur], next = scenes[i];
        if (prev) {
          G.to(prev, { opacity: 0, duration: 1.5, ease: 'power2.inOut', onComplete: () => { prev.classList.remove('is-active'); prev.style.visibility = 'hidden'; } });
          G.to(sets[cur], { yPercent: -115, duration: .8, stagger: .012, ease: 'power3.in' });
        }
        cur = i;
        next.classList.add('is-active'); next.style.visibility = 'visible';
        G.fromTo(next, { opacity: first ? 1 : 0 }, { opacity: 1, duration: 1.5, ease: 'power2.inOut' });
        G.fromTo($('.plate', next), { scale: 1.18 }, { scale: 1.02, duration: 18, ease: 'none' });
        G.fromTo(sets[i], { yPercent: 115 }, { yPercent: 0, duration: 1.4, stagger: .04, ease: 'expo.out', delay: first ? 0.1 : .5 });
        G.fromTo($$('.billing,.tagline,.cta', next), { y: 26, opacity: 0 }, { y: 0, opacity: 1, duration: 1.2, stagger: .12, ease: 'expo.out', delay: first ? .5 : .9 });
        chaps.forEach((c, k) => c.classList.toggle('is-active', k === i));
        if (prog) prog.kill();
        const bar = $('.bar i', chaps[i]);
        G.set($$('.chap .bar i', hero), { scaleX: 0 });
        prog = G.to(bar, { scaleX: 1, duration: 9, ease: 'none', onComplete: () => show((i + 1) % scenes.length) });
      };
      chaps.forEach((c, i) => c.addEventListener('click', () => { if (i !== cur) show(i); }));
      G.delayedCall(introDelay, () => { hero.classList.add('ready'); G.set($('.chapters', hero), { opacity: 1 }); show(0, true); });
      const cps = $('.chapters', hero);
      cps.addEventListener('pointerenter', () => prog && prog.pause());
      cps.addEventListener('pointerleave', () => prog && prog.play());

      pointerParallax(hero, [{ sel: '.plate-wrap', amt: -26 }, { sel: '.fogs', amt: 46 }, { sel: '.copy', amt: -10 }]);

      G.timeline({ scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } })
        .to($$('.plate-wrap', hero), { yPercent: 12, scale: 1.1, ease: 'none' }, 0)
        .to($('.copy', hero), { yPercent: -16, opacity: 0, ease: 'none' }, 0)
        .to($('.chapters', hero), { opacity: 0, ease: 'none' }, 0);
    }
  }

  /* ---------- ГЛАВНА: жанрова лента ---------- */
  const mq = $('.marquee');
  if (mq && !reduce) {
    const track = $('.track', mq), grp = $('.grp', track);
    for (let i = 0; i < 2; i++) track.appendChild(grp.cloneNode(true));
    let x = 0, w = grp.offsetWidth, last = performance.now(), run = true;
    addEventListener('resize', () => { w = grp.offsetWidth; });
    new IntersectionObserver(([e]) => { run = e.isIntersecting; if (run) { last = performance.now(); requestAnimationFrame(tick); } }).observe(mq);
    function tick(t) {
      if (!run) return;
      const dt = Math.min(40, t - last) / 16.67; last = t;
      const boost = lenis ? lenis.velocity * .4 : 0;
      x -= (.8 + boost) * dt;
      if (x <= -w) x += w; if (x > 0) x -= w;
      track.style.transform = `translate3d(${x}px,0,0)`;
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  /* ---------- Думи, които се проявяват със скрола ---------- */
  $$('[data-words]').forEach(el => {
    const ws = splitWords(el);
    if (anim) G.fromTo(ws, { opacity: .14 }, { opacity: 1, stagger: .12, ease: 'none', scrollTrigger: { trigger: el, start: 'top 82%', end: 'bottom 50%', scrub: true } });
  });

  /* ---------- Заглавия: лепкаво подреждане ---------- */
  const stories = $$('.story');
  if (stories.length && anim) {
    G.matchMedia().add('(min-width: 981px)', () => {
      stories.forEach((s, i) => {
        if (stories[i + 1]) G.to($('.inner', s), { scale: .9, opacity: .22, ease: 'none', scrollTrigger: { trigger: stories[i + 1], start: 'top bottom', end: 'top top', scrub: true } });
        G.from($$('.txt > *', s), { y: 50, opacity: 0, duration: 1.2, stagger: .09, ease: 'expo.out', scrollTrigger: { trigger: s, start: 'top 55%', once: true } });
        G.from($('.obj', s), { y: 90, opacity: 0, scale: .94, duration: 1.5, ease: 'expo.out', scrollTrigger: { trigger: s, start: 'top 55%', once: true } });
      });
    });
  }

  /* ---------- Поредица: хоризонтален ход ---------- */
  const series = $('.series');
  if (series && anim) {
    G.matchMedia().add('(min-width: 981px)', () => {
      const track = $('.h-track', series), bar = $('.prog i', series);
      const dist = () => Math.max(0, track.scrollWidth - innerWidth);
      G.to(track, { x: () => -dist(), ease: 'none', scrollTrigger: { trigger: series, start: 'top top', end: () => '+=' + dist(), pin: true, scrub: .7, invalidateOnRefresh: true, onUpdate: s => { bar.style.transform = `scaleX(${s.progress})`; } } });
    });
  }

  /* ---------- Библиотека: филтър ---------- */
  const chips = $$('[data-f]'), cards = $$('.card[data-g]');
  chips.forEach(c => c.addEventListener('click', () => {
    chips.forEach(x => x.classList.toggle('on', x === c));
    const f = c.dataset.f;
    cards.forEach(k => k.classList.toggle('is-off', f !== 'all' && !k.dataset.g.split(' ').includes(f)));
  }));

  /* ---------- СТРАНИЦА НА КНИГА ---------- */
  const bhero = $('.bhero');
  if (bhero) {
    initDust(bhero, () => bhero.dataset.tint);
    if (anim) {
      const chars = splitChars($('h1', bhero));
      G.set(chars, { yPercent: 115 });
      G.fromTo(chars, { yPercent: 115 }, { yPercent: 0, duration: 1.4, stagger: .04, ease: 'expo.out', delay: introDelay });
      G.from($$('.txt > :not(h1)', bhero), { y: 26, opacity: 0, duration: 1.2, stagger: .1, ease: 'expo.out', delay: introDelay + .5 });
      G.from($('.obj', bhero), { y: 70, opacity: 0, duration: 1.6, ease: 'expo.out', delay: introDelay + .2 });
      pointerParallax(bhero, [{ sel: '.plate-wrap', amt: -22 }]);
      G.timeline({ scrollTrigger: { trigger: bhero, start: 'top top', end: 'bottom top', scrub: true } })
        .to($('.plate-wrap', bhero), { yPercent: 14, scale: 1.1, ease: 'none' }, 0)
        .to($('.inner', bhero), { yPercent: -8, opacity: .0, ease: 'none' }, 0);
    }
  }

  const st = $('.statement');
  if (st && anim) {
    st.classList.add('pinned');
    const l1 = $('.ln.one', st), l2 = $('.ln.two', st);
    G.set([l1, l2], { opacity: 0, y: 40 });
    G.timeline({ scrollTrigger: { trigger: st, start: 'top top', end: '+=180%', pin: true, scrub: .6 } })
      .to(l1, { opacity: 1, y: 0, duration: 1 })
      .to(l1, { opacity: .1, y: () => -innerHeight * .3, duration: .9 }, '+=.5')
      .to(l2, { opacity: 1, y: 0, duration: 1 }, '<+.15')
      .to({}, { duration: .7 });
  }

  const LINKS = {
    EN: [['Amazon', 'https://www.amazon.com/dp/B0GR9RZYDB']],
    BG: [['Draft2Digital', 'https://books2read.com/u/3kErGO']],
    DE: [['Amazon', 'https://www.amazon.de/dp/B0GRN64P2G'], ['Draft2Digital', 'https://books2read.com/u/3Jdv2g']],
    ES: [['Amazon', 'https://www.amazon.es/dp/B0GRVKVWNQ'], ['Draft2Digital', 'https://books2read.com/u/bxLdwJ']],
    FR: [['Amazon', 'https://www.amazon.fr/dp/B0GRR9R386'], ['Draft2Digital', 'https://books2read.com/u/mYwJ7Y']],
    IT: [['Amazon', 'https://www.amazon.it/dp/B0GGZM4HGM'], ['Draft2Digital', 'https://books2read.com/u/mgQJoR']],
    NL: [['Amazon', 'https://www.amazon.nl/dp/B0GS2C225K'], ['Draft2Digital', 'https://books2read.com/u/bWDMk1']],
    PT: [['Amazon', 'https://www.amazon.es/dp/B0GSC3H9DC'], ['Draft2Digital', 'https://books2read.com/u/bWDNX1']],
    SE: [['Amazon', 'https://www.amazon.com/dp/B0GRSQ373C'], ['Draft2Digital', 'https://books2read.com/u/mqdJoZ']]
  };
  const langBox = $('[data-buy-langs]'), shop = $('[data-buy-shop]');
  if (langBox && shop) {
    const order = ['EN', 'BG', 'DE', 'FR', 'IT', 'NL', 'ES', 'PT', 'SE'];
    const draw = L => {
      $$('.chip', langBox).forEach(c => c.classList.toggle('on', c.dataset.l === L));
      const ls = LINKS[L] || [];
      shop.innerHTML = ls.length ? ls.map(l => `<a href="${l[1]}" target="_blank" rel="noopener">${l[0]} <i>→</i></a>`).join('') : `<p>${T('b.nolinks', 'Links for this language are not available yet.')}</p>`;
    };
    order.forEach(L => { const b = document.createElement('button'); b.type = 'button'; b.className = 'chip'; b.dataset.l = L; b.textContent = L; b.addEventListener('click', () => draw(L)); langBox.appendChild(b); });
    draw(lang.toUpperCase());
  }

  /* ---------- Обновяване след зареждане ---------- */
  addEventListener('load', () => { if (anim) ST.refresh(); });
})();
