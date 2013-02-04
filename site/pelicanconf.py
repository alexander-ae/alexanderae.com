#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u"__alexander__"
SITENAME = u"Alexander A. E. - log"
SITEURL = 'http://127.0.0.1:8000'

# Feed
FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_ATOM = None
CATEGORY_FEED_RSS = None
TAG_FEED_ATOM = 'feeds/%s.atom.xml'
TAG_FEED_RSS = 'feeds/%s.rss.xml'

# Local
TIMEZONE = 'America/Lima'
DEFAULT_LANG = 'es'
DEFAULT_DATE_FORMAT = '%d %b %Y'
LOCALE = ('es_ES',)

DEFAULT_PAGINATION = 3
DEFAULT_CATEGORY = "Sin categoría"
MARKUP = ('md',)
RELATIVE_URLS = False
SUMMARY_MAX_LENGTH = 56

# Links
MENUITEMS = (('Blog', '/'),
             ('Archivos', '/archives.html'),
             ('Etiquetas', '/tags.html'),
             (u'Buscar aquí', '/pages/buscar.html'),
             )

FOOTER_LINKS = (('Blog', '/'),
               ('Sobre mi', '/pages/about-me.html'),
                )


PLUGINS = ['pelican.plugins.assets', 'pelican.plugins.sitemap',
           'pelican.plugins.gzip_cache']
JINJA_EXTENSIONS = ['jinja2.ext.do', 'jinja2htmlcompress.HTMLCompress']

SHOW_AUTHOR = True
AUTHOR_FULL_NAME = 'Alexander Geronimo Ayasca Esquives'
META_DESCRIPTION = '''Sitio personal de __alexander__: Encontraras
    publicaciones sobre algunas de mis afficciones como linux, la programacion
    en python, desarrollo web en general entre otros'''

THEME = 'themes/alexander-theme'
STATIC_PATHS = ['pictures']

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.7,
        'indexes': 0.7,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'daily',
        'indexes': 'daily',
        'pages': 'weekly'
    }
}

# Externos
DISQUS_SITENAME = ''
TWITTER_USERNAME = ''
EMAIL = ''
GOOGLE_ANALYTICS_ID = ''
GOOGLE_SITE_VERIFICATION = ''

# Extra
FILES_TO_COPY = (('extra/humans.txt', 'humans.txt'),
                 ('extra/favicon.png', 'favicon.png'),
                 )
