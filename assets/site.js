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
