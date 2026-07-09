"""
Pure, dependency-free HTML template functions for the Karel Voden SSG build.
No DOM, no fetch — every function takes plain data and returns an HTML string.
"""
import html as _html

BASE_URL = "https://krvoden.com"
ALL_LANGS = ['bg', 'en', 'de', 'fr', 'it', 'nl', 'es', 'pt', 'se']
UI_LANGS = ['en', 'bg']

NAV_LABELS = {
    'en': [('/', 'Home'), ('library/', 'The Library'), ('news/', 'News'),
           ('about/', 'About'), ('contact/', 'Contact')],
    'bg': [('/', 'Начало'), ('library/', 'Библиотека'), ('news/', 'Новини'),
           ('about/', 'За автора'), ('contact/', 'Контакти')],
}

UI_STRINGS = {
    'en': {
        'synopsis_not_available': 'Synopsis not available.',
        'available_on': 'Available on',
        'no_links_lang': 'Links for this language are not available yet.',
        'synopsis': 'Synopsis',
        'read_excerpt': 'Read Excerpt',
        'latest_works': 'Latest Works',
        'welcome': 'Welcome to My Worlds',
        'explore_library': 'Explore the Full Library',
        'latest_news': 'Latest News',
        'read_all_news': 'Read all news',
        'the_library': 'The Library',
        'explore_series': 'Explore the Series',
        'other_works': 'Other Works',
        'standalone_novels': 'Standalone Novels',
        'short_stories': 'Short Stories',
        'books_in_series': 'Books in this series',
        'in_progress': 'In Progress',
        'news_and_updates': 'News and Updates',
        'no_news': 'No news yet. Stay tuned!',
        'about_the_author': 'About the Author',
        'get_in_touch': 'Get in Touch',
        'contact_intro': 'For business inquiries, media requests, or just to say hello, please use the form below.',
        'name': 'Name', 'email': 'Email', 'message': 'Message', 'send_message': 'Send Message',
        'back': 'Back', 'excerpt_from': 'Excerpt from',
        'not_found': '404 - Page Not Found',
        'privacy_policy': 'Privacy Policy',
        'by': 'by',
        'cookie_text': 'We use cookies to enhance your experience and for analytics. By continuing to browse, you agree to our <a href="/privacy-policy/">Privacy Policy</a>.',
        'cookie_accept': 'Accept',
    },
    'bg': {
        'synopsis_not_available': 'Няма налична анотация.',
        'available_on': 'Налично в',
        'no_links_lang': 'Все още няма линкове за този език.',
        'synopsis': 'Анотация',
        'read_excerpt': 'Прочети откъс',
        'latest_works': 'Най-нови творби',
        'welcome': 'Добре дошли в Моите светове',
        'explore_library': 'Разгледай цялата библиотека',
        'latest_news': 'Последни новини',
        'read_all_news': 'Прочети всички новини',
        'the_library': 'Библиотека',
        'explore_series': 'Разгледай поредиците',
        'other_works': 'Други творби',
        'standalone_novels': 'Самостоятелни романи',
        'short_stories': 'Разкази',
        'books_in_series': 'Книги в поредицата',
        'in_progress': 'В процес',
        'news_and_updates': 'Новини и събития',
        'no_news': 'Все още няма новини. Очаквайте скоро!',
        'about_the_author': 'За автора',
        'get_in_touch': 'Свържете се с мен',
        'contact_intro': 'За бизнес запитвания, медийни покани или просто да кажете "здравей", моля, използвайте формата по-долу.',
        'name': 'Име', 'email': 'Имейл', 'message': 'Съобщение', 'send_message': 'Изпрати съобщение',
        'back': 'Назад', 'excerpt_from': 'Откъс от',
        'not_found': '404 - Страницата не е намерена',
        'privacy_policy': 'Политика за поверителност',
        'by': 'от',
        'cookie_text': 'Използваме "бисквитки", за да подобрим вашето преживяване и за анализи. Продължавайки, вие се съгласявате с нашата <a href="/bg/privacy-policy/">Политика за поверителност</a>.',
        'cookie_accept': 'Приемам',
    },
}


def esc(s):
    return _html.escape(str(s or ''), quote=True)


def ui_lang_of(lang):
    """Chrome language for a given content language: en/bg map to themselves, everything else -> en."""
    return lang if lang in UI_LANGS else 'en'


def prefix(lang):
    return '' if lang == 'en' else f'/{lang}'


def home_path(lang):
    return prefix(lang) + '/'


def library_path(lang, sub=''):
    return prefix(lang) + '/library/' + (sub + '/' if sub else '')


def series_path(sid, lang):
    return prefix(lang) + f'/series/{sid}/'


def book_path(bid, lang):
    return prefix(lang) + f'/book/{bid}/'


def excerpt_path(bid, lang):
    return prefix(lang) + f'/excerpt/{bid}/'


def about_path(lang):
    return prefix(lang) + '/about/'


def contact_path(lang):
    return prefix(lang) + '/contact/'


def news_path(lang):
    return prefix(lang) + '/news/'


def news_article_path(slug, lang):
    return prefix(lang) + f'/news/{slug}/'


def privacy_path(lang):
    return prefix(lang) + '/privacy-policy/'


def site_title(data, lang):
    ui = ui_lang_of(lang)
    return data['meta'][ui]['siteTitle']


def author_name(data, lang):
    ui = ui_lang_of(lang)
    return data['meta'][ui]['name']


def find_book_by_id(data, bid):
    """Return (book, kind, series_id) or (None, None, None)."""
    for s in data.get('series', []):
        for b in s.get('books', []):
            if b['id'] == bid:
                return b, 'series', s['id']
    for b in data.get('novels', []):
        if b['id'] == bid:
            return b, 'novel', None
    for b in data.get('short_stories', []):
        if b['id'] == bid:
            return b, 'story', None
    return None, None, None


# ─────────────────────────────────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────────────────────────────────

def layout(data, *, lang, path, title, description, body_html,
           og_image='images/common/social-share.jpg', hreflangs=None,
           active_nav_base=None, nav_lang_switch=None):
    """
    lang: content/page language (drives <html lang>)
    path: this page's site-root-relative path, e.g. '/book/foo/'
    hreflangs: list of (hreflang_code, absolute_url) for <link rel=alternate>
    active_nav_base: which nav item should be marked active ('/', 'library/', ...)
    nav_lang_switch: {'en': url_or_None, 'bg': url_or_None} for the EN|BG switcher
    """
    ui = ui_lang_of(lang)
    depth = path.strip('/').count('/') + 1 if path != '/' else 0
    root = '../' * depth if depth else './'
    canonical = BASE_URL + path

    hreflang_tags = ''
    if hreflangs:
        hreflang_tags = '\n    '.join(
            f'<link rel="alternate" hreflang="{code}" href="{url}">' for code, url in hreflangs
        )

    nav_items = ''
    for href, label in NAV_LABELS[ui]:
        is_active = (href == '/' and active_nav_base == '/') or \
                    (href != '/' and active_nav_base and active_nav_base.startswith(href))
        nav_items += f'<li class="nav-item"><a href="{root}{href.lstrip("/")}" class="nav-link{" active" if is_active else ""}">{esc(label)}</a></li>'

    lang_switch_html = ''
    if nav_lang_switch:
        parts = []
        for code in ('en', 'bg'):
            url = nav_lang_switch.get(code)
            label = code.upper()
            if ui == code:
                parts.append(f'<span>{label}</span>')
            elif url:
                parts.append(f'<a href="{url}">{label}</a>')
        lang_switch_html = ' | '.join(parts)

    strings = UI_STRINGS[ui]

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(title)}</title>

    <meta name="description" content="{esc(description)}">
    <meta name="author" content="Karel Voden">

    <meta property="og:title" content="{esc(title)}">
    <meta property="og:description" content="{esc(description)}">
    <meta property="og:image" content="{BASE_URL}/{og_image.lstrip('/')}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="website">

    <link rel="canonical" href="{canonical}">
    {hreflang_tags}

    <link rel="apple-touch-icon" sizes="180x180" href="{root}images/common/favicons/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="{root}images/common/favicons/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="{root}images/common/favicons/favicon-16x16.png">
    <link rel="manifest" href="{root}images/common/favicons/site.webmanifest">

    <link rel="stylesheet" href="{root}style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
</head>
<body>
    <header>
        <nav class="navbar">
            <a href="{root}" class="nav-logo">Karel VODEN</a>
            <ul class="nav-menu">{nav_items}</ul>
            <button class="hamburger" aria-label="Open menu">
                <span class="bar"></span><span class="bar"></span><span class="bar"></span>
            </button>
            <div class="lang-switcher">{lang_switch_html}</div>
        </nav>
    </header>

    <main id="main-content">
{body_html}
    </main>

    <footer>
        <div class="container">
            <p>© 2024 Karel Voden. All rights reserved. | <a href="{root}privacy-policy/">{esc(strings['privacy_policy'])}</a></p>
        </div>
    </footer>

    <script src="{root}assets/site.js"></script>

    <div id="cookie-banner" class="cookie-banner">
        <div class="cookie-content">
            <p id="cookie-text">{strings['cookie_text']}</p>
            <button id="cookie-accept-btn" class="btn">{esc(strings['cookie_accept'])}</button>
        </div>
    </div>
</body>
</html>
"""


# ─────────────────────────────────────────────────────────────────────────
# SHARED PIECES
# ─────────────────────────────────────────────────────────────────────────

def book_card(book, ui_lang):
    i18n = book.get('i18n', {})
    display_lang = ui_lang if ui_lang in i18n else 'en'
    bdata = i18n.get(display_lang)
    if not bdata:
        return ''
    title = bdata.get('title', '')
    cover = bdata.get('cover') or 'images/common/cover-placeholder.jpg'
    pills = ''.join(
        f'<a href="{book_path(book["id"], l)}" class="lang-pill">{l.upper()}</a>'
        for l in i18n
    )
    status = f'<span class="status-tag">{esc(UI_STRINGS[ui_lang]["in_progress"])}</span>' \
        if book.get('status') == 'in-progress' else ''
    href = book_path(book['id'], display_lang)
    link_style = 'text-decoration:none;color:inherit'
    return f"""<div class="book-card">
        <a href="{href}" style="{link_style}"><img src="/{esc(cover)}" alt="Cover of {esc(title)}" loading="lazy"></a>
        <div class="book-card-content"><h3><a href="{href}" style="{link_style}">{esc(title)}</a></h3><div class="lang-pills">{pills}</div>{status}</div>
    </div>"""


# ─────────────────────────────────────────────────────────────────────────
# PAGE BODIES
# ─────────────────────────────────────────────────────────────────────────

def render_homepage(data, lang, latest_news_html=''):
    ui = ui_lang_of(lang)
    s = UI_STRINGS[ui]
    meta = data['meta'][ui]
    featured_ids = data.get('featured', [])
    cards = []
    for bid in featured_ids:
        book, _, _ = find_book_by_id(data, bid)
        if book:
            cards.append(book_card(book, ui))
    body = f"""
        <div class="hero-section"><div class="container"><h1>{esc(s['welcome'])}</h1><p class="author-intro">{meta['intro']}</p></div></div>
        <div class="container homepage-content">
            <h2>{esc(s['latest_works'])}</h2>
            <div class="books-grid-featured">{''.join(cards)}</div>
            <div class="all-books-link"><a href="{library_path(lang)}" class="btn">{esc(s['explore_library'])}</a></div>
            {latest_news_html}
        </div>"""
    return body


def render_news_excerpt_block(lang, article_title, excerpt_text, slug):
    ui = ui_lang_of(lang)
    s = UI_STRINGS[ui]
    return f"""<div class="latest-news-section">
        <h2>{esc(s['latest_news'])}</h2>
        <div class="news-excerpt">
            <h3>{esc(article_title)}</h3>
            <p>{esc(excerpt_text)}</p>
            <a href="{news_path(lang)}" class="read-more">{esc(s['read_all_news'])} →</a>
        </div>
    </div>"""


def render_library_hub(data, lang):
    ui = ui_lang_of(lang)
    s = UI_STRINGS[ui]
    cards = []
    for series in data.get('series', []):
        sd = series['i18n'].get(ui) or series['i18n'].get('en') or {}
        bg_style = ''
        if series.get('seriesImage'):
            bg_style = f"background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('/{esc(series['seriesImage'])}')"
        cards.append(f'<a href="{series_path(series["id"], lang)}" class="hub-card" style="{bg_style}"><h2>{esc(sd.get("title", series["id"]))}</h2></a>')
    body = f"""
        <div class="container library-hub">
            <h1>{esc(s['the_library'])}</h1>
            <h2>{esc(s['explore_series'])}</h2>
            <div class="hub-grid">{''.join(cards)}</div>
            <h2>{esc(s['other_works'])}</h2>
            <div class="hub-grid small">
                <a href="{library_path(lang, 'novels')}" class="hub-card"><h2>{esc(s['standalone_novels'])}</h2></a>
                <a href="{library_path(lang, 'stories')}" class="hub-card"><h2>{esc(s['short_stories'])}</h2></a>
            </div>
        </div>"""
    return body


def render_series_page(data, series, lang):
    ui = ui_lang_of(lang)
    s = UI_STRINGS[ui]
    sd = series['i18n'].get(ui) or series['i18n'].get('en') or {}
    header_img = series.get('seriesImage') or 'images/common/series-bg-placeholder.jpg'
    cards = ''.join(book_card(b, ui) for b in series.get('books', []))
    body = f"""
        <div class="series-page-header" style="background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('/{esc(header_img)}');">
            <div class="container"><h1>{esc(sd.get('title', series['id']))}</h1><p class="series-synopsis">{sd.get('series_synopsis', '')}</p></div>
        </div>
        <div class="container"><h2>{esc(s['books_in_series'])}</h2><div class="books-grid">{cards}</div></div>"""
    return body


def render_book_list_page(data, lang, kind):
    ui = ui_lang_of(lang)
    titles = {'novels': {'en': 'Standalone Novels', 'bg': 'Самостоятелни романи'},
              'short_stories': {'en': 'Short Stories', 'bg': 'Разкази'}}
    title = titles[kind][ui]
    cards = ''.join(book_card(b, ui) for b in data.get(kind, []))
    return f"""<div class="container book-list-page"><h1>{esc(title)}</h1><div class="books-grid">{cards}</div></div>"""


def render_book_detail(data, book, lang, synopsis_html):
    ui = ui_lang_of(lang)
    s = UI_STRINGS[ui]
    bdata = book['i18n'].get(lang) or book['i18n'].get('en')
    cover = bdata.get('cover') or 'images/common/cover-placeholder.jpg'
    excerpt_link = ''
    if bdata.get('excerpt'):
        excerpt_link = f'<div class="excerpt-link-cover"><a href="{excerpt_path(book["id"], lang)}" class="btn-secondary">{esc(s["read_excerpt"])}</a></div>'
    links = [l for l in book.get('links', []) if l.get('lang', '').lower() == lang.lower()]
    if links:
        buy_html = ''.join(
            f'<a href="{esc(l["url"])}" target="_blank" rel="noopener" class="buy-logo-link" title="Buy on {esc(l["platform"])}"><img src="/images/common/{l["platform"].lower()}.png" alt="{esc(l["platform"])}"></a>'
            for l in links
        )
    else:
        buy_html = f'<p>{esc(s["no_links_lang"])}</p>'
    synopsis_html = synopsis_html or f'<p>{esc(s["synopsis_not_available"])}</p>'
    body = f"""
        <div class="container book-detail-view">
            <div class="book-detail-cover">
                <img src="/{esc(cover)}" alt="{esc(bdata['title'])}">
                {excerpt_link}
            </div>
            <div class="book-detail-info">
                <h1>{esc(bdata['title'])}</h1>
                {f'<p class="book-genre">{esc(bdata["genre"])}</p>' if bdata.get('genre') else ''}
                <h3>{esc(s['synopsis'])}</h3><div class="synopsis">{synopsis_html}</div>
                <h3>{esc(s['available_on'])}</h3>
                <div class="buy-links">{buy_html}</div>
            </div>
        </div>"""
    return body


def render_excerpt_page(book, lang, excerpt_html):
    ui = ui_lang_of(lang)
    s = UI_STRINGS[ui]
    bdata = book['i18n'].get(lang) or book['i18n'].get('en')
    body = f"""
        <div class="reading-container">
            <h1 class="preview-title">{esc(s['excerpt_from'])} {esc(bdata['title'])}</h1>
            <a href="{book_path(book['id'], lang)}" class="back-link">← {esc(s['back'])}</a>
            <article class="prose">{excerpt_html}</article>
        </div>"""
    return body


def render_news_list_page(lang, articles):
    """articles: list of dicts {slug, title, date, author, excerpt}, newest first."""
    ui = ui_lang_of(lang)
    s = UI_STRINGS[ui]
    if not articles:
        items = f'<p>{esc(s["no_news"])}</p>'
    else:
        items = ''
        for a in articles:
            items += f"""<article class="news-item">
                <h2><a href="{news_article_path(a['slug'], lang)}" style="color:inherit;text-decoration:none">{esc(a['title'])}</a></h2>
                <p class="news-meta"><span>{esc(a['date_fmt'])}</span> | <span>{esc(s['by'])} {esc(a['author'])}</span></p>
                <div class="news-content"><p>{esc(a['excerpt'])}</p></div>
            </article>"""
    return f"""<div class="container news-page"><h1>{esc(s['news_and_updates'])}</h1><div class="news-list">{items}</div></div>"""


def render_news_article_page(lang, article, content_html):
    ui = ui_lang_of(lang)
    s = UI_STRINGS[ui]
    body = f"""<div class="container news-page">
        <a href="{news_path(lang)}" class="back-link">← {esc(s['back'])}</a>
        <article class="news-item">
            <h1>{esc(article['title'])}</h1>
            <p class="news-meta"><span>{esc(article['date_fmt'])}</span> | <span>{esc(s['by'])} {esc(article['author'])}</span></p>
            <div class="news-content">{content_html}</div>
        </article>
    </div>"""
    return body


def render_about_page(data, lang, bio_html, author_photo):
    ui = ui_lang_of(lang)
    s = UI_STRINGS[ui]
    name = author_name(data, lang)
    return f"""<div class="container about-page">
        <div class="author-photo-large"><img src="/{esc(author_photo)}" alt="Photo of {esc(name)}"></div>
        <div class="author-bio-content"><h1>{esc(s['about_the_author'])}</h1><p class="bio-text">{bio_html}</p></div>
    </div>"""


def render_contact_page(lang):
    ui = ui_lang_of(lang)
    s = UI_STRINGS[ui]
    return f"""<div class="container contact-page">
        <h1>{esc(s['get_in_touch'])}</h1>
        <p>{esc(s['contact_intro'])}</p>
        <form id="contact-form" class="contact-form">
            <div class="form-group"><label for="name">{esc(s['name'])}</label><input type="text" id="name" name="name" required></div>
            <div class="form-group"><label for="email">{esc(s['email'])}</label><input type="email" id="email" name="email" required></div>
            <div class="form-group"><label for="message">{esc(s['message'])}</label><textarea id="message" name="message" rows="6" required></textarea></div>
            <button type="submit" class="btn">{esc(s['send_message'])}</button>
        </form>
        <div id="form-status"></div>
    </div>"""


def render_privacy_page(lang, title, body_html):
    return f'<div class="container text-page"><h1>{esc(title)}</h1>{body_html}</div>'


def render_404_page(lang='en'):
    ui = ui_lang_of(lang)
    s = UI_STRINGS[ui]
    return f'<div class="container"><h1>{esc(s["not_found"])}</h1><p><a href="/">← {esc(s["back"])}</a></p></div>'
