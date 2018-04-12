#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals

AUTHOR = u"__alexander__"
SITENAME = u"Alexander A. E."
SITEURL = 'http://127.0.0.1:8000'

PATH = 'source'

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
# LOCALE = ('es_ES',)

DEFAULT_PAGINATION = 6
DEFAULT_CATEGORY = "Sin categoría"
MARKUP = ('md',)
RELATIVE_URLS = False
SUMMARY_MAX_LENGTH = 80

# Links
MENUITEMS = (('Blog', '/'),
             ('Sobre mi', '/pages/about-me.html'),
             ('Archivos', '/archives.html'),
             ('Etiquetas', '/tags.html'),
             (u'Buscar aquí', '/pages/buscar.html'),
             )

FOOTER_LINKS = (('Blog', '/'),
                ('Sobre mi', '/pages/about-me.html'),
                )

PLUGIN_PATHS = ['/home/alexander/Proyectos/pelican-plugins']
PLUGINS = ['assets', 'sitemap', 'tag_cloud']
JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.do']
}

SHOW_AUTHOR = True
AUTHOR_FULL_NAME = 'Alexander Geronimo Ayasca Esquives'
META_DESCRIPTION = '''Mi blog personal, encontrarás publicaciones sobre algunas de mis aficciones como linux,
    programación en python, desarrollo web en general entre otros'''

THEME = 'themes/skeleton-theme'

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.8,
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
STATIC_PATHS = [
    'pictures',
    'extra/humans.txt',
    'extra/favicon.png'
]

EXTRA_PATH_METADATA = {
    'extra/humans.txt': {'path': 'humans.txt'},
    'extra/favicon.png': {'path': 'favicon.png'}
}

DEBUG = True
