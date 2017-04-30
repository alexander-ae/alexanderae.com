#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import sys
sys.path.append('.')
from pelicanconf import *

SITEURL = 'https://alexanderae.com'

OUTPUT_PATH = '/home/alcaudon/webapps/alexander_ae_site'
DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

# Uncomment following line for absolute URLs in production:
RELATIVE_URLS = False

DISQUS_SITENAME = 'alexanderaeblog'
TWITTER_USERNAME = '__alexander_'
EMAIL = 'alexander.ayasca.esquives@gmail.com'
GOOGLE_TAG_MANAGER_ID = 'GTM-K4R3KJ'
GOOGLE_SITE_VERIFICATION = 'dTKg4FbepddqdYP9iaPVB2ltcImvpKoCB_0l-Notfbg'

PLUGINS = ['assets', 'sitemap', 'gzip_cache', 'optimize_images']
JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.do', 'jinja2htmlcompress.HTMLCompress']
}
