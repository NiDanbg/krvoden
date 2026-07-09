#!/usr/bin/env python3
"""
Static site generator for the Karel Voden author site.
Reads data.js / synopsis / books / news from this directory and writes a
fully pre-rendered, hash-free static site into dist/.

Usage:  python scripts/build.py
"""
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import render as R
import markdown_lite as MD

BASE = Path(__file__).resolve().parent.parent  # karelvoden/
DIST = BASE / 'dist'
UI_LANGS = ['en', 'bg']


# ─────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────

def load_author_data():
    text = (BASE / 'data.js').read_text(encoding='utf-8')
    m = re.search(r'const\s+authorData\s*=\s*(\{.*\})\s*;?\s*$', text, re.DOTALL)
    if not m:
        raise ValueError('Cannot locate authorData object in data.js')
    obj = m.group(1)
    try:
        return json.loads(obj)
    except json.JSONDecodeError:
        pass

    # Tolerant fallback for hand-edited JS (unquoted keys, comments, trailing commas).
    strings = []

    def save_template(match):
        content = match.group(1)
        content = content.replace('\\', '\\\\').replace('"', '\\"')
        content = content.replace('\r\n', '\\n').replace('\n', '\\n').replace('\r', '').replace('\t', '\\t')
        strings.append(f'"{content}"')
        return f'\x02{len(strings) - 1}\x02'

    obj = re.sub(r'`([^`]*)`', save_template, obj, flags=re.DOTALL)

    def save_str(match):
        strings.append(match.group(0))
        return f'\x02{len(strings) - 1}\x02'

    obj = re.sub(r'"(?:[^"\\]|\\.)*"', save_str, obj)
    obj = re.sub(r'//[^\n]*', '', obj)
    obj = re.sub(r'(?<!["\w\x02])([a-zA-Z_$][a-zA-Z0-9_$]*)(\s*):', r'"\1"\2:', obj)
    obj = re.sub(r',(\s*[}\]])', r'\1', obj)
    for i, s_val in enumerate(strings):
        obj = obj.replace(f'\x02{i}\x02', s_val)
    return json.loads(obj)


def read_text(relpath):
    p = BASE / relpath
    return p.read_text(encoding='utf-8') if p.exists() else ''


EN_MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
             'August', 'September', 'October', 'November', 'December']
BG_MONTHS = ['януари', 'февруари', 'март', 'април', 'май', 'юни', 'юли',
             'август', 'септември', 'октомври', 'ноември', 'декември']


def format_date(date_str, ui_lang):
    try:
        y, mo, d = date_str[:10].split('-')
        months = BG_MONTHS if ui_lang == 'bg' else EN_MONTHS
        month = months[int(mo) - 1]
        return f'{int(d)} {month} {y}' if ui_lang == 'bg' else f'{month} {int(d)}, {y}'
    except Exception:
        return date_str


def slugify(stem):
    slug = re.sub(r'[^a-z0-9]+', '-', stem.lower()).strip('-')
    return slug or 'article'


def load_news():
    """Returns {ui_lang: [ {slug, title, author, date_raw, date_fmt, content_html, excerpt}, ... newest first ]}"""
    index_path = BASE / 'news' / 'index.json'
    filenames = json.loads(index_path.read_text(encoding='utf-8')) if index_path.exists() else []
    result = {lang: [] for lang in UI_LANGS}
    for fname in filenames:
        stem = fname[:-3] if fname.endswith('.md') else fname
        slug = slugify(stem)
        date_raw = fname[:10]
        for lang in UI_LANGS:
            p = BASE / 'news' / lang / fname
            if not p.exists():
                continue
            metadata, content = MD.parse_frontmatter(p.read_text(encoding='utf-8'))
            words = content.split()
            excerpt = ' '.join(words[:30]) + ('...' if len(words) > 30 else '')
            result[lang].append({
                'slug': slug,
                'title': metadata.get('title') or stem,
                'author': metadata.get('author') or 'Karel Voden',
                'date_raw': date_raw,
                'date_fmt': format_date(date_raw, lang),
                'content_html': MD.to_html(content),
                'excerpt': excerpt,
            })
    for lang in UI_LANGS:
        result[lang].reverse()  # newest first, matching original site behaviour
    return result


# ─────────────────────────────────────────────────────────────────────────
# OUTPUT HELPERS
# ─────────────────────────────────────────────────────────────────────────

SITEMAP = []


def write_page(path, html_str, priority=0.5):
    rel = path.strip('/')
    target_dir = (DIST / rel) if rel else DIST
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / 'index.html').write_text(html_str, encoding='utf-8')
    SITEMAP.append((R.BASE_URL + path, priority))


def iter_all_books(data):
    for s in data.get('series', []):
        for b in s.get('books', []):
            yield b
    for b in data.get('novels', []):
        yield b
    for b in data.get('short_stories', []):
        yield b


def same_route_switch(path_fn, *args):
    return {'en': path_fn('en', *args), 'bg': path_fn('bg', *args)}


def book_lang_switch(book, id_):
    i18n = book['i18n']
    return {
        'en': R.book_path(id_, 'en') if 'en' in i18n else R.home_path('en'),
        'bg': R.book_path(id_, 'bg') if 'bg' in i18n else R.home_path('bg'),
    }


# ─────────────────────────────────────────────────────────────────────────
# BUILD
# ─────────────────────────────────────────────────────────────────────────

def _clean_dist():
    import time
    if not DIST.exists():
        return
    for attempt in range(5):
        try:
            shutil.rmtree(DIST)
            return
        except PermissionError:
            time.sleep(0.3 * (attempt + 1))
    # Last resort: remove what we can, ignore stubborn locked files (e.g. AV scanner).
    shutil.rmtree(DIST, ignore_errors=True)


def build():
    _clean_dist()
    DIST.mkdir(parents=True, exist_ok=True)

    data = load_author_data()
    news = load_news()

    # ---- site-language pages (en / bg) ----
    for ui in UI_LANGS:
        latest_news_html = ''
        if news[ui]:
            latest = news[ui][0]
            latest_news_html = R.render_news_excerpt_block(ui, latest['title'], latest['excerpt'], latest['slug'])
        body = R.render_homepage(data, ui, latest_news_html)
        write_page(R.home_path(ui), R.layout(
            data, lang=ui, path=R.home_path(ui),
            title=R.site_title(data, ui),
            description=data['meta'][ui]['intro'][:160],
            body_html=body, active_nav_base='/',
            nav_lang_switch=same_route_switch(lambda l: R.home_path(l)),
        ), 1.0)

        body = R.render_library_hub(data, ui)
        write_page(R.library_path(ui), R.layout(
            data, lang=ui, path=R.library_path(ui),
            title=f"{R.UI_STRINGS[ui]['the_library']} | {R.author_name(data, ui)}",
            description=R.UI_STRINGS[ui]['explore_series'],
            body_html=body, active_nav_base='library/',
            nav_lang_switch=same_route_switch(lambda l: R.library_path(l)),
        ), 0.9)

        for kind, sub in (('novels', 'novels'), ('short_stories', 'stories')):
            body = R.render_book_list_page(data, ui, kind)
            write_page(R.library_path(ui, sub), R.layout(
                data, lang=ui, path=R.library_path(ui, sub),
                title=f"{R.author_name(data, ui)}",
                description=R.UI_STRINGS[ui]['the_library'],
                body_html=body, active_nav_base='library/',
                nav_lang_switch=same_route_switch(lambda l, s=sub: R.library_path(l, s)),
            ), 0.6)

        for series in data.get('series', []):
            sd = series['i18n'].get(ui) or series['i18n'].get('en') or {}
            body = R.render_series_page(data, series, ui)
            write_page(R.series_path(series['id'], ui), R.layout(
                data, lang=ui, path=R.series_path(series['id'], ui),
                title=f"{sd.get('title', series['id'])} | {R.author_name(data, ui)}",
                description=(sd.get('series_synopsis') or '')[:160],
                body_html=body,
                nav_lang_switch=same_route_switch(lambda l, sid=series['id']: R.series_path(sid, l)),
            ), 0.7)

        about_photo = data['meta'].get('photo') or 'images/common/author-placeholder.jpg'
        bio_html = MD.bio_html(read_text(f'synopsis/{ui}/about.txt'))
        body = R.render_about_page(data, ui, bio_html, about_photo)
        write_page(R.about_path(ui), R.layout(
            data, lang=ui, path=R.about_path(ui),
            title=f"{R.UI_STRINGS[ui]['about_the_author']} | {R.author_name(data, ui)}",
            description=R.UI_STRINGS[ui]['about_the_author'],
            body_html=body, active_nav_base='about/',
            nav_lang_switch=same_route_switch(lambda l: R.about_path(l)),
        ), 0.8)

        body = R.render_contact_page(ui)
        write_page(R.contact_path(ui), R.layout(
            data, lang=ui, path=R.contact_path(ui),
            title=f"{R.UI_STRINGS[ui]['get_in_touch']} | {R.author_name(data, ui)}",
            description=R.UI_STRINGS[ui]['contact_intro'],
            body_html=body, active_nav_base='contact/',
            nav_lang_switch=same_route_switch(lambda l: R.contact_path(l)),
        ), 0.7)

        body = R.render_news_list_page(ui, news[ui])
        write_page(R.news_path(ui), R.layout(
            data, lang=ui, path=R.news_path(ui),
            title=f"{R.UI_STRINGS[ui]['news_and_updates']} | {R.author_name(data, ui)}",
            description=R.UI_STRINGS[ui]['news_and_updates'],
            body_html=body, active_nav_base='news/',
            nav_lang_switch=same_route_switch(lambda l: R.news_path(l)),
        ), 0.8)

        for article in news[ui]:
            other_lang_has_it = any(a['slug'] == article['slug'] for a in news['bg' if ui == 'en' else 'en'])
            switch = {
                'en': R.news_article_path(article['slug'], 'en') if (ui == 'en' or other_lang_has_it) else R.news_path('en'),
                'bg': R.news_article_path(article['slug'], 'bg') if (ui == 'bg' or other_lang_has_it) else R.news_path('bg'),
            }
            body = R.render_news_article_page(ui, article, article['content_html'])
            write_page(R.news_article_path(article['slug'], ui), R.layout(
                data, lang=ui, path=R.news_article_path(article['slug'], ui),
                title=f"{article['title']} | {R.author_name(data, ui)}",
                description=article['excerpt'][:160],
                body_html=body, active_nav_base='news/',
                nav_lang_switch=switch,
            ), 0.5)

        title, priv_body = MD.privacy_html(read_text(f'synopsis/{ui}/privacy-policy.txt'))
        body = R.render_privacy_page(ui, title or R.UI_STRINGS[ui]['privacy_policy'], priv_body)
        write_page(R.privacy_path(ui), R.layout(
            data, lang=ui, path=R.privacy_path(ui),
            title=f"{R.UI_STRINGS[ui]['privacy_policy']} | {R.author_name(data, ui)}",
            description=R.UI_STRINGS[ui]['privacy_policy'],
            body_html=body,
            nav_lang_switch=same_route_switch(lambda l: R.privacy_path(l)),
        ), 0.3)

    # ---- content-language pages (book / excerpt) ----
    for book in iter_all_books(data):
        bid = book['id']
        i18n = book['i18n']
        langs_here = sorted(i18n.keys())
        hreflangs = [(l, R.BASE_URL + R.book_path(bid, l)) for l in langs_here]
        switch = book_lang_switch(book, bid)

        for lang in langs_here:
            bdata = i18n[lang]
            synopsis_txt = read_text(bdata['synopsis']) if bdata.get('synopsis') else ''
            synopsis_html = MD.synopsis_html(synopsis_txt)
            body = R.render_book_detail(data, book, lang, synopsis_html)
            write_page(R.book_path(bid, lang), R.layout(
                data, lang=lang, path=R.book_path(bid, lang),
                title=f"{bdata['title']} | {R.author_name(data, lang)}",
                description=(' '.join(synopsis_txt.split()) or bdata['title'])[:160],
                og_image=bdata.get('cover') or 'images/common/cover-placeholder.jpg',
                body_html=body, hreflangs=hreflangs, nav_lang_switch=switch,
            ), 0.6)

            if bdata.get('excerpt'):
                excerpt_txt = read_text(bdata['excerpt'])
                excerpt_html = MD.to_html(excerpt_txt)
                body = R.render_excerpt_page(book, lang, excerpt_html)
                write_page(R.excerpt_path(bid, lang), R.layout(
                    data, lang=lang, path=R.excerpt_path(bid, lang),
                    title=f"{R.UI_STRINGS[R.ui_lang_of(lang)]['excerpt_from']} {bdata['title']} | {R.author_name(data, lang)}",
                    description=bdata['title'],
                    og_image=bdata.get('cover') or 'images/common/cover-placeholder.jpg',
                    body_html=body, hreflangs=hreflangs, nav_lang_switch=switch,
                ), 0.5)

    # ---- static assets ----
    for name in ('images', 'style.css'):
        src = BASE / name
        if src.is_dir():
            shutil.copytree(src, DIST / name, dirs_exist_ok=True)
        elif src.exists():
            shutil.copy2(src, DIST / name)

    (DIST / 'assets').mkdir(exist_ok=True)
    shutil.copy2(BASE / 'assets' / 'site.js', DIST / 'assets' / 'site.js')

    (DIST / 'CNAME').write_text('krvoden.com\n', encoding='utf-8')
    (DIST / '404.html').write_text(R.layout(
        data, lang='en', path='/',
        title=f"404 | {R.author_name(data, 'en')}",
        description='Page not found',
        body_html=R.render_404_page('en'),
        nav_lang_switch=same_route_switch(lambda l: R.home_path(l)),
    ), encoding='utf-8')

    (DIST / 'robots.txt').write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {R.BASE_URL}/sitemap.xml\n", encoding='utf-8'
    )

    sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>',
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, priority in SITEMAP:
        sitemap_xml.append(f'    <url><loc>{url}</loc><priority>{priority}</priority></url>')
    sitemap_xml.append('</urlset>')
    (DIST / 'sitemap.xml').write_text('\n'.join(sitemap_xml), encoding='utf-8')

    print(f'Built {len(SITEMAP)} pages into {DIST}')


if __name__ == '__main__':
    build()
