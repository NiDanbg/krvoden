// Karel Voden — minimal client-side behavior for the static site.
// No router: every page is pre-rendered HTML with real URLs.
document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        navMenu.addEventListener('click', (e) => {
            if (e.target.classList.contains('nav-link')) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    }

    // Book search — the index holds every edition in every language, so a German
    // title leads to the German page. Loaded once, on first use.
    const searchBox = document.querySelector('.nav-search');
    if (searchBox) {
        const toggle = searchBox.querySelector('.search-toggle');
        const input = searchBox.querySelector('.search-input');
        const results = searchBox.querySelector('.search-results');
        const noneText = results.dataset.none;
        // The site's own code for this page's language ("se"), not the one the
        // crawler reads off <html lang> ("sv") — the index is keyed the site's way.
        const pageLang = document.documentElement.dataset.siteLang
            || document.documentElement.lang || 'en';
        let index = null, loading = null;

        const CYR = { 'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ж':'zh','з':'z','и':'i','й':'y',
            'к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f',
            'х':'h','ц':'ts','ч':'ch','ш':'sh','щ':'sht','ъ':'a','ь':'','ю':'yu','я':'ya' };

        // Fold everything to bare latin letters: Hüterin -> huterin, ß -> ss,
        // Наследницата -> naslednicata. Lets a reader type without diacritics.
        const fold = (s) => (s || '').toLowerCase()
            .replace(/ß/g, 'ss')
            .normalize('NFD').replace(/\p{M}/gu, '')
            .split('').map((c) => (c in CYR ? CYR[c] : c)).join('')
            .replace(/[^a-z0-9]+/g, ' ')
            // ts and c are the same sound in transliteration: naslednitsa = naslednica
            .replace(/ts/g, 'c')
            .trim();

        const loadIndex = () => {
            if (index) return Promise.resolve(index);
            if (!loading) {
                loading = fetch('/search-index.json')
                    .then((r) => r.json())
                    .then((data) => {
                        index = data.map((e) => Object.assign({}, e, {
                            _t: fold(e.t), _s: fold(e.s), _g: fold(e.g),
                        }));
                        return index;
                    })
                    .catch(() => { index = []; return index; });
            }
            return loading;
        };

        const rank = (entry, q) => {
            let score;
            if (entry._t.startsWith(q)) score = 0;
            else if (entry._t.includes(' ' + q)) score = 1;
            else if (entry._t.includes(q)) score = 2;
            else if (entry._s && entry._s.includes(q)) score = 3;
            else if (entry._g && entry._g.includes(q)) score = 4;
            else return null;
            return score * 2 + (entry.l === pageLang ? 0 : 1);
        };

        const render = (q) => {
            const folded = fold(q);
            if (folded.length < 2) { results.hidden = true; results.innerHTML = ''; return; }
            const hits = [];
            (index || []).forEach((e) => {
                const s = rank(e, folded);
                if (s !== null) hits.push([s, e]);
            });
            hits.sort((a, b) => a[0] - b[0] || a[1].t.localeCompare(b[1].t));
            results.hidden = false;
            if (!hits.length) {
                results.innerHTML = '<p class="search-empty">' + noneText + '</p>';
                return;
            }
            results.innerHTML = hits.slice(0, 8).map(([, e]) => {
                const cover = e.c ? '<img src="' + e.c + '" alt="">' : '';
                const series = e.s ? '<span class="search-series">' + e.s + '</span>' : '';
                return '<a class="search-hit" href="' + e.u + '">' + cover +
                    '<span class="search-hit-text"><span class="search-title">' + e.t + '</span>' +
                    series + '</span><span class="search-lang">' + e.l.toUpperCase() + '</span></a>';
            }).join('');
        };

        const open = () => {
            searchBox.classList.add('open');
            toggle.setAttribute('aria-expanded', 'true');
            input.focus();
            loadIndex().then(() => { if (input.value) render(input.value); });
        };
        const close = () => {
            searchBox.classList.remove('open');
            toggle.setAttribute('aria-expanded', 'false');
            results.hidden = true;
        };

        toggle.addEventListener('click', () => {
            searchBox.classList.contains('open') ? close() : open();
        });
        input.addEventListener('input', () => loadIndex().then(() => render(input.value)));
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') { close(); toggle.focus(); }
            if (e.key === 'Enter') {
                const first = results.querySelector('.search-hit');
                if (first) window.location.href = first.getAttribute('href');
            }
        });
        document.addEventListener('click', (e) => {
            if (!searchBox.contains(e.target)) close();
        });
    }

    // Cookie banner
    const banner = document.getElementById('cookie-banner');
    const acceptBtn = document.getElementById('cookie-accept-btn');
    if (banner && acceptBtn) {
        if (!localStorage.getItem('cookiesAccepted')) {
            setTimeout(() => banner.classList.add('show'), 1000);
        }
        acceptBtn.onclick = () => {
            localStorage.setItem('cookiesAccepted', 'true');
            banner.classList.remove('show');
        };
    }

    // Lead-magnet banners — our own modal opens instantly (no provider
    // trigger delay); Sender.net is loaded on demand, only on click, and
    // renders its embedded form into the modal once ready.
    document.querySelectorAll('.lead-magnet-cta').forEach((btn) => {
        btn.addEventListener('click', () => {
            const accountId = btn.dataset.accountId;
            const modal = btn.closest('.lead-magnet-banner')?.nextElementSibling;
            if (!accountId || !modal || !modal.classList.contains('lead-magnet-modal')) return;
            modal.classList.add('open');
            const formId = modal.querySelector('[data-sender-form-id]')?.dataset.senderFormId;
            if (window.senderForms) {
                if (formId) window.senderForms.render(formId);
                return;
            }
            (function (s, e, n, d, er) {
                s['Sender'] = er;
                s[er] = s[er] || function () { (s[er].q = s[er].q || []).push(arguments); };
                s[er].l = 1 * new Date();
                s[er].on = function (event, callback) {
                    s[er].listeners = s[er].listeners || {};
                    (s[er].listeners[event] = s[er].listeners[event] || []).push(callback);
                };
                const a = e.createElement(n);
                const m = e.getElementsByTagName(n)[0];
                a.async = 1;
                a.src = d;
                a.onload = () => { if (formId) window.senderForms.render(formId); };
                m.parentNode.insertBefore(a, m);
            })(window, document, 'script', 'https://cdn.sender.net/accounts_resources/universal.js', 'sender');
            window.sender(accountId);
        });
    });

    document.querySelectorAll('.lead-magnet-modal').forEach((modal) => {
        modal.querySelector('.lead-magnet-modal-close')?.addEventListener('click', () => {
            modal.classList.remove('open');
        });
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.classList.remove('open');
        });
    });

    // Contact form
    // Shares the same Google Form/inbox as the Crispin Thorn site — the
    // message body is tagged with the site of origin so replies can tell
    // the two apart in one shared response sheet.
    const form = document.getElementById('contact-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const statusDiv = document.getElementById('form-status');
            const lang = document.documentElement.lang === 'bg' ? 'bg' : 'en';
            const sendingText = lang === 'bg' ? 'Изпращане...' : 'Sending...';
            const okText = lang === 'bg' ? 'Благодаря! Вашето съобщение беше изпратено.' : 'Thank you! Your message has been sent.';
            const errText = lang === 'bg' ? 'Възникна грешка. Моля, опитайте отново.' : 'An error occurred. Please try again.';
            statusDiv.textContent = sendingText;
            const formData = new FormData(form);
            const name = formData.get('name');
            const email = formData.get('email');
            const message = `[Karel Voden website] ${formData.get('message')}`;
            const formUrl = `https://docs.google.com/forms/d/e/1FAIpQLSd6oAve7uoiaXMJWWukyYHWEZQgGTJxPgCpV40E-f3mCNkQtw/formResponse?entry.1843393081=${encodeURIComponent(name)}&entry.1799285576=${encodeURIComponent(email)}&entry.530113389=${encodeURIComponent(message)}`;
            try {
                await fetch(formUrl, { method: 'POST', mode: 'no-cors' });
                statusDiv.textContent = okText;
                statusDiv.style.color = 'green';
                form.reset();
            } catch (error) {
                statusDiv.textContent = errText;
                statusDiv.style.color = 'red';
            }
        });
    }
});
