"""
Pure, dependency-free HTML template functions for the Karel Voden SSG build.
No DOM, no fetch — every function takes plain data and returns an HTML string.
"""
import html as _html
import json as _json

BASE_URL = "https://krvoden.com"
GA_ID = "G-GF28ENCM9M"
SENDER_ACCOUNT_ID = "ed72b4b7a59839"
SUPPORT_EMAIL = "contact@krvoden.com"

# Short content hashes for style.css / assets/site.js, filled in by build.py.
# They ride along as ?v=... so a returning reader never runs a stale script.
ASSET_V = {'css': '', 'js': ''}


def asset_v(kind):
    return ('?v=' + ASSET_V[kind]) if ASSET_V.get(kind) else ''


ALL_LANGS = ['bg', 'en', 'de', 'fr', 'it', 'nl', 'es', 'pt', 'se']

# The site calls Swedish "se" in its folders, but "se" is Northern Sami to a
# search engine. Everything a crawler reads - <html lang>, hreflang, og:locale -
# goes out as the real code; the folder names stay as they are.
BCP47 = {'se': 'sv'}

OG_LOCALES = {'bg': 'bg_BG', 'en': 'en_US', 'de': 'de_DE', 'fr': 'fr_FR', 'it': 'it_IT',
              'nl': 'nl_NL', 'es': 'es_ES', 'pt': 'pt_PT', 'se': 'sv_SE'}


def bcp47(lang):
    return BCP47.get(lang, lang)


UI_LANGS = ['en', 'bg']

NAV_LABELS = {
    'en': [('/', 'Home'), ('library/', 'The Library'), ('store/', 'Bookshop'), ('news/', 'News'),
           ('about/', 'About'), ('contact/', 'Contact')],
    'bg': [('/', 'Начало'), ('library/', 'Библиотека'), ('store/', 'Книжарница'), ('news/', 'Новини'),
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
        'terms_of_service': 'Terms of Service',
        'customer_support': 'Customer support',
        'search': 'Search',
        'store': 'Bookshop',
        'store_intro': 'These editions come straight from the author, without a middleman. The download link arrives the moment the payment goes through.',
        'store_note': 'Payment and invoicing are handled by Creem, the Merchant of Record for these orders. Books are delivered as EPUB files. The details are in the {terms}.',
        'store_heading': 'Buy direct from the author',
        'store_cta': 'Visit the bookshop',
        'editions_in': 'Editions in',
        'read_excerpt_short': 'Read excerpt',
        'search_placeholder': 'Search for a book…',
        'search_none': 'Nothing found',
        'get_gift': 'Get it free',
        'desc_library': 'Every novel and short story by Karel Voden, with the series they belong to and the languages each one is published in.',
        'desc_novels': 'The standalone novels of Karel Voden - thrillers that braid ancient mysteries into modern conspiracies.',
        'desc_stories': 'Short stories by Karel Voden, set in the worlds his novels open up.',
        'desc_news': 'Releases, translations and what Karel Voden is working on next.',
        'desc_about': 'Karel Voden writes international thrillers and conspiracy fiction. Who he is and how the books came about.',
        'desc_privacy': 'What this site collects, why, and how to have it removed.',
        'desc_terms': 'Digital delivery, refunds and copyright for the ebooks sold directly on this site.',
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
        'terms_of_service': 'Общи условия',
        'customer_support': 'Обслужване на клиенти',
        'search': 'Търсене',
        'store': 'Книжарница',
        'store_intro': 'Книги, които се продават направо от автора, без посредник. Линкът за изтегляне идва в мига, в който плащането мине.',
        'store_note': 'Плащането и фактурите минават през Creem, продавач по договор за тези поръчки. Книгите се доставят във формат EPUB. Подробностите са в {terms}.',
        'store_heading': 'Купи директно от автора',
        'store_cta': 'Към книжарницата',
        'editions_in': 'Издания на',
        'read_excerpt_short': 'Прочети откъс',
        'search_placeholder': 'Търсене на книга…',
        'search_none': 'Няма намерено',
        'get_gift': 'Вземи безплатно',
        'desc_library': 'Всички романи и разкази на Karel Voden, поредиците, към които принадлежат, и езиците, на които излизат.',
        'desc_novels': 'Самостоятелните романи на Karel Voden - трилъри, в които древни загадки се преплитат със съвременни конспирации.',
        'desc_stories': 'Разкази на Karel Voden, разположени в световете на романите му.',
        'desc_news': 'Нови заглавия, преводи и над какво работи Karel Voden в момента.',
        'desc_about': 'Karel Voden пише международни трилъри и конспиративна фантастика. Кой е той и как се раждат книгите му.',
        'desc_privacy': 'Какво събира този сайт, защо и как да поискате данните си да бъдат изтрити.',
        'desc_terms': 'Доставка, връщане на суми и авторски права за електронните книги, продавани директно тук.',
    },
}


# Direct-sale button, one label per book language (the chrome stays en/bg, the book does not).
BUY_DIRECT_LABELS = {
    'bg': 'Купи директно от автора за {price}',
    'en': 'Buy direct from the author for {price}',
    'de': 'Direkt vom Autor kaufen für {price}',
    'fr': "Acheter directement à l'auteur pour {price}",
    'it': "Acquista direttamente dall'autore per {price}",
    'nl': 'Koop rechtstreeks bij de auteur voor {price}',
    'es': 'Compra directamente al autor por {price}',
    'pt': 'Compre diretamente ao autor por {price}',
    'se': 'Köp direkt av författaren för {price}',
}

# (decimal separator, layout) per language. Prices are in euro; the non-breaking
# space keeps the amount and the symbol on the same line.
PRICE_FORMATS = {
    'bg': (',', '{amount} €'),
    'en': ('.', '€{amount}'),
    'de': (',', '{amount} €'),
    'fr': (',', '{amount} €'),
    'it': (',', '{amount} €'),
    'nl': (',', '€ {amount}'),
    'es': (',', '{amount} €'),
    'pt': (',', '{amount} €'),
    'se': (',', '{amount} €'),
}

# Short form of the same button, for the bookshop rows where the price stands on its own.
BUY_DIRECT_SHORT = {
    'bg': 'Купи директно',
    'en': 'Buy direct',
    'de': 'Direkt kaufen',
    'fr': 'Acheter directement',
    'it': 'Acquista direttamente',
    'nl': 'Direct kopen',
    'es': 'Compra directa',
    'pt': 'Compra direta',
    'se': 'Köp direkt',
}

# Names of the book languages, in each of the two chrome languages.
LANG_NAMES = {
    'en': {'bg': 'Bulgarian', 'en': 'English', 'de': 'German', 'fr': 'French', 'it': 'Italian',
           'nl': 'Dutch', 'es': 'Spanish', 'pt': 'Portuguese', 'se': 'Swedish'},
    'bg': {'bg': 'български', 'en': 'английски', 'de': 'немски', 'fr': 'френски', 'it': 'италиански',
           'nl': 'нидерландски', 'es': 'испански', 'pt': 'португалски', 'se': 'шведски'},
}

# Set by build.py: False hides the bookshop from the menu, the footer and the
# homepage, so nothing ever points at an empty shelf.
STORE_ACTIVE = False


# Each language's own name for itself. One list serves all nine editions, which
# beats keeping nine names in nine languages.
LANG_AUTONYMS = {
    'bg': 'български', 'en': 'English', 'de': 'Deutsch', 'fr': 'Français',
    'it': 'Italiano', 'nl': 'Nederlands', 'es': 'Español', 'pt': 'Português',
    'se': 'Svenska',
}

# The plain statement of what a book is, in the language of the book. A reader
# infers it from the cover; a language model has to read it written down.
# Every part is optional - the sentence is assembled from whatever data exists.
BOOK_FACTS = {
    'bg': {'base': '„{title}“ е {genre} от {author}.',
           'series_n': ' Книга {n} от поредицата „{series}“.',
           'series': ' Част от поредицата „{series}“.',
           'published': ' Издадена през {year} г.',
           'publisher': ' Издател: {publisher}.',
           'isbn': ' ISBN {isbn}.',
           'langs': ' Издания на: {langs}.'},
    'en': {'base': '“{title}” is {article}{genre} by {author}.',
           'article': 'a ',
           'series_n': ' Book {n} of the {series} series.',
           'series': ' Part of the {series} series.',
           'published': ' Published in {year}.',
           'publisher': ' Publisher: {publisher}.',
           'isbn': ' ISBN {isbn}.',
           'langs': ' Editions in: {langs}.'},
    'de': {'base': '„{title}“ ist {article}{genre} von {author}.',
           'article': 'ein ',
           'series_n': ' Band {n} der Reihe „{series}“.',
           'series': ' Teil der Reihe „{series}“.',
           'published': ' Erschienen {year}.',
           'publisher': ' Verlag: {publisher}.',
           'isbn': ' ISBN {isbn}.',
           'langs': ' Ausgaben auf: {langs}.'},
    'fr': {'base': '« {title} » est {article}{genre} de {author}.',
           'article': 'un ',
           'series_n': ' Tome {n} de la série « {series} ».',
           'series': ' Fait partie de la série « {series} ».',
           'published': ' Publié en {year}.',
           'publisher': ' Éditeur : {publisher}.',
           'isbn': ' ISBN {isbn}.',
           'langs': ' Éditions en : {langs}.'},
    'it': {'base': '«{title}» è {article}{genre} di {author}.',
           'article': 'un ',
           'series_n': ' Libro {n} della serie «{series}».',
           'series': ' Fa parte della serie «{series}».',
           'published': ' Pubblicato nel {year}.',
           'publisher': ' Editore: {publisher}.',
           'isbn': ' ISBN {isbn}.',
           'langs': ' Edizioni in: {langs}.'},
    'nl': {'base': '“{title}” is {article}{genre} van {author}.',
           'article': 'een ',
           'series_n': ' Deel {n} van de reeks “{series}”.',
           'series': ' Onderdeel van de reeks “{series}”.',
           'published': ' Verschenen in {year}.',
           'publisher': ' Uitgever: {publisher}.',
           'isbn': ' ISBN {isbn}.',
           'langs': ' Edities in: {langs}.'},
    'es': {'base': '«{title}» es {article}{genre} de {author}.',
           'article': 'un ',
           'series_n': ' Libro {n} de la serie «{series}».',
           'series': ' Forma parte de la serie «{series}».',
           'published': ' Publicado en {year}.',
           'publisher': ' Editorial: {publisher}.',
           'isbn': ' ISBN {isbn}.',
           'langs': ' Ediciones en: {langs}.'},
    'pt': {'base': '«{title}» é {article}{genre} de {author}.',
           'article': 'um ',
           'series_n': ' Livro {n} da série «{series}».',
           'series': ' Faz parte da série «{series}».',
           'published': ' Publicado em {year}.',
           'publisher': ' Editora: {publisher}.',
           'isbn': ' ISBN {isbn}.',
           'langs': ' Edições em: {langs}.'},
    'se': {'base': '”{title}” är {article}{genre} av {author}.',
           'article': 'en ',
           'series_n': ' Bok {n} i serien ”{series}”.',
           'series': ' Del av serien ”{series}”.',
           'published': ' Utgiven {year}.',
           'publisher': ' Förlag: {publisher}.',
           'isbn': ' ISBN {isbn}.',
           'langs': ' Utgåvor på: {langs}.'},
}


# Articles a genre may already carry. "Una historia satírica de burocracia
# mágica" is a whole phrase, not a bare genre noun, so the template must not
# put a second article in front of it.
GENRE_ARTICLES = {
    'en': r"(a|an|the)\b", 'de': r"(ein|eine|einer)\b", 'fr': r"(un|une)\b",
    'it': r"(un|uno|una|un')", 'nl': r"(een)\b", 'es': r"(un|una|unos|unas)\b",
    'pt': r"(um|uma)\b", 'se': r"(en|ett)\b",
}


def genre_has_article(lang, genre):
    import re as _re
    pattern = GENRE_ARTICLES.get(lang)
    return bool(pattern and _re.match(pattern, genre, _re.IGNORECASE))


def genre_article(lang, genre, default):
    """The article to put before the genre, or nothing when it brings its own."""
    if genre_has_article(lang, genre):
        return ''
    if lang == 'en' and genre[:1].lower() in 'aeiou':
        return 'an '
    return default


def short_genre(genre):
    """Genre fields are catalogue strings - "Balkan noir / FICTION / Thrillers"
    or "Исторически техно-трилър, Конспиративен трилър". A sentence needs the
    first part, spelled the way the author typed it: lowercasing turns a name
    like Balkan noir into something that reads as a mistake."""
    import re as _re
    return _re.split(r'[/,;]', str(genre or ''))[0].strip()


def year_of(date_str):
    """First four digits of whatever the admin panel holds: 2026-03-14, 03/2026, 2026."""
    import re as _re
    m = _re.search(r'\d{4}', str(date_str or ''))
    return m.group(0) if m else ''


def series_title_for(series, lang):
    if not series:
        return ''
    ui = ui_lang_of(lang)
    sd = series['i18n'].get(lang) or series['i18n'].get(ui) or series['i18n'].get('en') or {}
    return sd.get('title', '')


def book_facts_sentence(data, book, lang, series=None):
    """One sentence stating what this book is, built from whatever data exists.
    Empty when there is not even a genre to state."""
    bdata = book['i18n'].get(lang) or {}
    tpl = BOOK_FACTS.get(lang, BOOK_FACTS['en'])
    genre = short_genre(bdata.get('genre'))
    if not genre or not bdata.get('title'):
        return ''
    article = genre_article(lang, genre, tpl.get('article', ''))
    if genre_has_article(lang, genre):
        # The genre carries its own article. It was typed as a standalone label,
        # so it starts with a capital; mid-sentence that reads like a title.
        genre = genre[0].lower() + genre[1:]
    out = tpl['base'].format(title=bdata['title'], genre=genre,
                             author=author_name(data, lang), article=article)
    stitle = series_title_for(series, lang)
    if stitle:
        if lang == 'en':
            # The English template supplies the article, so a series called
            # "The Beyond the Petrohan Files" must not bring its own.
            import re as _re
            stitle = _re.sub(r'^the\s+', '', stitle, flags=_re.IGNORECASE)
        pos = book.get('position')
        out += (tpl['series_n'].format(n=pos, series=stitle) if pos
                else tpl['series'].format(series=stitle))
    year = year_of(bdata.get('published'))
    if year:
        out += tpl['published'].format(year=year)
    if bdata.get('publisher'):
        out += tpl['publisher'].format(publisher=bdata['publisher'])
    if bdata.get('isbn'):
        out += tpl['isbn'].format(isbn=bdata['isbn'])
    others = [LANG_AUTONYMS[l] for l in ALL_LANGS
              if l in book.get('i18n', {}) and book['i18n'][l].get('title')]
    if len(others) > 1:
        out += tpl['langs'].format(langs=', '.join(others))
    return out


def render_book_facts(data, book, lang, series=None):
    text = book_facts_sentence(data, book, lang, series)
    return f'<p class="book-facts">{esc(text)}</p>' if text else ''


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


def terms_path(lang):
    return prefix(lang) + '/terms-of-service/'


def store_path(lang):
    return prefix(lang) + '/store/'


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
# STRUCTURED DATA (JSON-LD)
# ─────────────────────────────────────────────────────────────────────────

def abs_url(path):
    """Site-root-relative path or asset path -> absolute URL."""
    return BASE_URL + '/' + str(path or '').lstrip('/')


def person_ref(data, lang):
    """The author, as one node every other node can point at."""
    ui = ui_lang_of(lang)
    node = {
        '@type': 'Person',
        '@id': BASE_URL + '/#author',
        'name': author_name(data, lang),
        'url': abs_url(about_path(ui)),
    }
    photo = (data.get('meta') or {}).get('photo')
    if photo:
        node['image'] = abs_url(photo)
    return node


def jsonld_website(data, lang):
    ui = ui_lang_of(lang)
    return {
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        '@id': BASE_URL + '/#website',
        'name': site_title(data, ui),
        'url': abs_url(home_path(ui)),
        'inLanguage': bcp47(ui),
        'publisher': person_ref(data, ui),
    }


def jsonld_person(data, lang, bio_text=''):
    ui = ui_lang_of(lang)
    node = dict(person_ref(data, ui), **{'@context': 'https://schema.org'})
    bio = ' '.join((bio_text or '').split())
    if bio:
        node['description'] = bio[:300]
    node['jobTitle'] = 'Author' if ui == 'en' else 'Писател'
    return node


def jsonld_book(data, book, lang, synopsis_text='', series=None):
    """One node per language edition, because each edition has its own title,
    cover and - where the author sells it himself - its own price."""
    bdata = book['i18n'].get(lang) or {}
    node = {
        '@context': 'https://schema.org',
        '@type': 'Book',
        'name': bdata.get('title', ''),
        'url': abs_url(book_path(book['id'], lang)),
        'author': person_ref(data, lang),
        'inLanguage': bcp47(lang),
        'bookFormat': 'https://schema.org/EBook',
    }
    if bdata.get('genre'):
        node['genre'] = bdata['genre']
    if bdata.get('published'):
        node['datePublished'] = str(bdata['published'])
    if bdata.get('isbn'):
        node['isbn'] = str(bdata['isbn'])
    if bdata.get('publisher'):
        node['publisher'] = {'@type': 'Organization', 'name': bdata['publisher']}
    if book.get('position'):
        node['position'] = book['position']
    node['abstract'] = book_facts_sentence(data, book, lang, series)
    if bdata.get('cover'):
        node['image'] = abs_url(bdata['cover'])
    syn = ' '.join((synopsis_text or '').split())
    if syn:
        node['description'] = syn[:300]
    if series:
        ui = ui_lang_of(lang)
        sd = series['i18n'].get(lang) or series['i18n'].get(ui) or series['i18n'].get('en') or {}
        if sd.get('title'):
            node['isPartOf'] = {
                '@type': 'BookSeries',
                'name': sd['title'],
                'url': abs_url(series_path(series['id'], ui)),
            }
    url = (bdata.get('creem_checkout_url') or '').strip()
    price = str(bdata.get('price') or '').strip()
    if bdata.get('direct_sale_active') and url and price:
        node['offers'] = {
            '@type': 'Offer',
            'price': price,
            'priceCurrency': 'EUR',
            'availability': 'https://schema.org/InStock',
            'url': url,
        }
    if not node.get('abstract'):
        node.pop('abstract', None)
    links = [l for l in book.get('links', []) if l.get('lang', '').lower() == lang.lower() and l.get('url')]
    if links:
        node['sameAs'] = [l['url'] for l in links]
    return node


def jsonld_article(data, lang, article):
    ui = ui_lang_of(lang)
    node = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': article.get('title', ''),
        'url': abs_url(news_article_path(article['slug'], ui)),
        'author': person_ref(data, ui),
        'publisher': person_ref(data, ui),
        'inLanguage': bcp47(ui),
    }
    if article.get('date_raw'):
        node['datePublished'] = article['date_raw']
    if article.get('excerpt'):
        node['description'] = article['excerpt'][:300]
    return node


def jsonld_breadcrumbs(items):
    """items: list of (name, site-root-relative path)."""
    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i, 'name': name, 'item': abs_url(path)}
            for i, (name, path) in enumerate(items, start=1)
        ],
    }


def book_breadcrumbs(data, book, lang, series=None, leaf=None):
    ui = ui_lang_of(lang)
    s = UI_STRINGS[ui]
    bdata = book['i18n'].get(lang) or {}
    items = [(author_name(data, ui), home_path(ui)), (s['the_library'], library_path(ui))]
    if series:
        sd = series['i18n'].get(lang) or series['i18n'].get(ui) or series['i18n'].get('en') or {}
        if sd.get('title'):
            items.append((sd['title'], series_path(series['id'], ui)))
    items.append((bdata.get('title', book['id']), book_path(book['id'], lang)))
    if leaf:
        items.append((leaf, excerpt_path(book['id'], lang)))
    return jsonld_breadcrumbs(items)


# ─────────────────────────────────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────────────────────────────────

def layout(data, *, lang, path, title, description, body_html,
           og_image='images/common/social-share.jpg', hreflangs=None,
           active_nav_base=None, nav_lang_switch=None,
           og_type='website', jsonld=None):
    """
    lang: content/page language (drives <html lang>)
    path: this page's site-root-relative path, e.g. '/book/foo/'
    hreflangs: list of (hreflang_code, absolute_url) for <link rel=alternate>
    active_nav_base: which nav item should be marked active ('/', 'library/', ...)
    nav_lang_switch: {'en': url_or_None, 'bg': url_or_None} for the EN|BG switcher
    og_type: 'website', 'book', 'article', 'profile'
    jsonld: one schema.org dict, or a list of them
    """
    ui = ui_lang_of(lang)
    depth = path.strip('/').count('/') + 1 if path != '/' else 0
    root = '../' * depth if depth else './'
    canonical = BASE_URL + path

    hreflang_tags = ''
    locale_alt_tags = ''
    if hreflangs:
        tags = [f'<link rel="alternate" hreflang="{bcp47(code)}" href="{url}">'
                for code, url in hreflangs]
        # Whoever does not match any of the listed languages lands on the English
        # edition; without x-default Google picks one for them.
        default = dict(hreflangs).get('en') or hreflangs[0][1]
        tags.append(f'<link rel="alternate" hreflang="x-default" href="{default}">')
        hreflang_tags = '\n    '.join(tags)
        locale_alt_tags = '\n    '.join(
            f'<meta property="og:locale:alternate" content="{OG_LOCALES[code]}">'
            for code, _ in hreflangs if code != lang and code in OG_LOCALES
        )

    jsonld_tags = ''
    if jsonld:
        blocks = jsonld if isinstance(jsonld, list) else [jsonld]
        jsonld_tags = '\n    '.join(
            '<script type="application/ld+json">'
            + _json.dumps(b, ensure_ascii=False, separators=(',', ':'))
            + '</script>'
            for b in blocks
        )

    nav_items = ''
    for href, label in NAV_LABELS[ui]:
        if href == 'store/' and not STORE_ACTIVE:
            continue
        is_active = (href == '/' and active_nav_base == '/') or \
                    (href != '/' and active_nav_base and active_nav_base.startswith(href))
        # Language-aware: the BG chrome must stay inside /bg/, not fall back to the EN pages.
        nav_href = prefix(ui) + '/' + href.lstrip('/')
        nav_items += f'<li class="nav-item"><a href="{nav_href}" class="nav-link{" active" if is_active else ""}">{esc(label)}</a></li>'

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
<html lang="{bcp47(lang)}" data-site-lang="{lang}">
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
    <meta property="og:type" content="{og_type}">
    <meta property="og:site_name" content="{esc(site_title(data, ui))}">
    <meta property="og:locale" content="{OG_LOCALES.get(lang, 'en_US')}">
    {locale_alt_tags}

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{esc(title)}">
    <meta name="twitter:description" content="{esc(description)}">
    <meta name="twitter:image" content="{BASE_URL}/{og_image.lstrip('/')}">

    <link rel="canonical" href="{canonical}">
    {hreflang_tags}

    {jsonld_tags}

    <link rel="apple-touch-icon" sizes="180x180" href="{root}images/common/favicons/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="{root}images/common/favicons/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="{root}images/common/favicons/favicon-16x16.png">
    <link rel="manifest" href="{root}images/common/favicons/site.webmanifest">

    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
    <script>
       window.dataLayer = window.dataLayer || [];
       function gtag(){{dataLayer.push(arguments);}}
       gtag('js', new Date());
       gtag('config', '{GA_ID}');
    </script>

    <link rel="stylesheet" href="{root}style.css{asset_v('css')}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
</head>
<body>
    <header>
        <nav class="navbar">
            <a href="{home_path(ui)}" class="nav-logo">Karel VODEN</a>
            <ul class="nav-menu">{nav_items}</ul>
            <div class="nav-search">
                <button type="button" class="search-toggle" aria-label="{esc(strings['search'])}" aria-expanded="false">
                    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"
                         stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><line x1="16.5" y1="16.5" x2="21" y2="21"></line></svg>
                </button>
                <div class="search-panel">
                    <input type="search" class="search-input" autocomplete="off" spellcheck="false"
                           placeholder="{esc(strings['search_placeholder'])}" aria-label="{esc(strings['search'])}">
                    <div class="search-results" data-none="{esc(strings['search_none'])}" hidden></div>
                </div>
            </div>
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
            <p>© 2024 Karel Voden. All rights reserved. | <a href="{privacy_path(ui)}">{esc(strings['privacy_policy'])}</a> | <a href="{terms_path(ui)}">{esc(strings['terms_of_service'])}</a>{f' | <a href="{store_path(ui)}">{esc(strings["store"])}</a>' if STORE_ACTIVE else ''}</p>
            <p class="footer-support">{esc(strings['customer_support'])}: <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></p>
        </div>
    </footer>

    <script src="{root}assets/site.js{asset_v('js')}"></script>

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

def render_homepage(data, lang, latest_news_html='', store_band=''):
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
            {store_band}
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


def render_book_detail(data, book, lang, synopsis_html, series=None):
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
                {render_book_facts(data, book, lang, series)}
                <h3>{esc(s['synopsis'])}</h3><div class="synopsis">{synopsis_html}</div>
                {render_lead_magnet(bdata, lang)}
                {render_direct_sale(bdata, lang)}
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
            {render_lead_magnet(bdata, lang)}
        </div>"""
    return body


def render_news_list_page(lang, articles):
    """articles: list of dicts {slug, title, date, author, content_html}, newest first.
    The whole article stands on the list page - a reader should not have to click
    through to find out whether a piece of news concerns them."""
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
                <div class="news-content">{a['content_html']}</div>
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


def render_lead_magnet(bdata, lang):
    """Banner + instant custom modal for a free-gift Sender.net embedded form,
    shown only if configured for this book+language. Sender.net's script is only
    loaded on click, and its embedded-form widget renders inside our own modal
    so opening is instant (no provider trigger delay)."""
    lm = bdata.get('leadMagnet') or {}
    if not lm.get('enabled') or not lm.get('senderFormId'):
        return ''
    ui = ui_lang_of(lang)
    cta = UI_STRINGS[ui]['get_gift']
    img_html = f'<img src="/{esc(lm["image"])}" alt="" class="lead-magnet-img">' if lm.get('image') else ''
    return f"""
        <div class="lead-magnet-banner">
            {img_html}
            <div class="lead-magnet-body">
                <p>{esc(lm.get('bannerText', ''))}</p>
                <button type="button" class="btn lead-magnet-cta" data-account-id="{esc(SENDER_ACCOUNT_ID)}">{esc(cta)}</button>
            </div>
        </div>
        <div class="lead-magnet-modal">
            <div class="lead-magnet-modal-inner">
                <button type="button" class="lead-magnet-modal-close" aria-label="Close">&times;</button>
                <div class="sender-form-field" data-sender-form-id="{esc(lm['senderFormId'])}"></div>
            </div>
        </div>"""


def format_price(price, lang):
    """Price as the reader of that language writes it. Anything that is not a
    number is printed exactly as typed in the admin panel."""
    sep, template = PRICE_FORMATS.get(lang, PRICE_FORMATS['en'])
    raw = str(price or '').strip()
    try:
        amount = f'{float(raw.replace(",", ".")):.2f}'
    except ValueError:
        return raw
    return template.format(amount=amount.replace('.', sep))


def render_direct_sale(bdata, lang):
    """Checkout button for this language edition, sold by the author through Creem.
    Every translation is its own product, so price and link come from i18n[lang].
    The label speaks the language of the book, not of the surrounding chrome."""
    if not bdata.get('direct_sale_active'):
        return ''
    url = (bdata.get('creem_checkout_url') or '').strip()
    price = str(bdata.get('price') or '').strip()
    if not url or not price:
        return ''
    label = BUY_DIRECT_LABELS.get(lang, BUY_DIRECT_LABELS['en']).format(
        price=format_price(price, lang))
    return f"""
        <div class="direct-sale">
            <a href="{esc(url)}" class="direct-sale-btn" target="_blank" rel="noopener">{esc(label)}</a>
        </div>"""


def store_row(entry, ui):
    """One purchasable edition: cover, what it is, and the way to buy it."""
    lang = entry['lang']
    book_url = book_path(entry['id'], lang)
    cover = entry.get('cover') or 'images/common/cover-placeholder.jpg'
    overline = ' · '.join(filter(None, [entry.get('series'), LANG_NAMES[ui].get(lang, lang.upper())]))
    genre = f'<p class="store-genre">{esc(entry["genre"])}</p>' if entry.get('genre') else ''
    teaser = f'<p class="store-teaser">{esc(entry["teaser"])}</p>' if entry.get('teaser') else ''
    excerpt = (f'<a class="store-excerpt" href="{excerpt_path(entry["id"], lang)}">'
               f'{esc(UI_STRINGS[ui]["read_excerpt_short"])}</a>') if entry.get('has_excerpt') else ''
    return f"""
            <article class="store-item">
                <a class="store-cover" href="{book_url}"><img src="/{esc(cover)}" alt="{esc(entry['title'])}" loading="lazy"></a>
                <div class="store-body">
                    <p class="store-overline">{esc(overline)}</p>
                    <h3 class="store-title"><a href="{book_url}">{esc(entry['title'])}</a></h3>
                    {genre}
                    {teaser}
                </div>
                <div class="store-buy">
                    <span class="store-price">{esc(format_price(entry['price'], lang))}</span>
                    <a class="direct-sale-btn" href="{esc(entry['url'])}" target="_blank" rel="noopener">{esc(BUY_DIRECT_SHORT[ui])}</a>
                    {excerpt}
                </div>
            </article>"""


def render_store_page(entries, lang):
    """The bookshop: every edition the author sells directly, grouped by language
    only once there is more than one - a lone section heading looks like a mistake."""
    ui = ui_lang_of(lang)
    s = UI_STRINGS[ui]
    langs = [l for l in ALL_LANGS if any(e['lang'] == l for e in entries)]
    sections = []
    for l in langs:
        rows = ''.join(store_row(e, ui) for e in entries if e['lang'] == l)
        head = (f'<h2 class="store-lang-head">{esc(s["editions_in"])} {esc(LANG_NAMES[ui][l])}</h2>'
                if len(langs) > 1 else '')
        sections.append(head + f'<div class="store-list">{rows}</div>')
    terms_link = f'<a href="{terms_path(ui)}">{esc(s["terms_of_service"])}</a>'
    note = esc(s['store_note']).replace('{terms}', terms_link)
    return f"""
        <div class="container store-page">
            <h1>{esc(s['store'])}</h1>
            <p class="store-intro">{esc(s['store_intro'])}</p>
            {''.join(sections)}
            <p class="store-note">{note}</p>
        </div>"""


def render_store_band(entries, lang):
    """Homepage strip pointing at the bookshop. Silent when nothing is on sale."""
    if not entries:
        return ''
    ui = ui_lang_of(lang)
    s = UI_STRINGS[ui]
    covers = ''.join(
        f'<img src="/{esc(e.get("cover") or "images/common/cover-placeholder.jpg")}" alt="{esc(e["title"])}" loading="lazy">'
        for e in entries[:3]
    )
    return f"""
        <section class="store-band">
            <div class="store-band-covers">{covers}</div>
            <div class="store-band-text">
                <h2>{esc(s['store_heading'])}</h2>
                <p>{esc(s['store_intro'])}</p>
                <a class="direct-sale-btn" href="{store_path(ui)}">{esc(s['store_cta'])}</a>
            </div>
        </section>"""


def render_terms_page(lang, title, body_html):
    return f'<div class="container text-page"><h1>{esc(title)}</h1>{body_html}</div>'


def render_privacy_page(lang, title, body_html):
    return f'<div class="container text-page"><h1>{esc(title)}</h1>{body_html}</div>'


def render_404_page(lang='en'):
    ui = ui_lang_of(lang)
    s = UI_STRINGS[ui]
    return f'<div class="container"><h1>{esc(s["not_found"])}</h1><p><a href="/">← {esc(s["back"])}</a></p></div>'
