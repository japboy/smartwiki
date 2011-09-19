#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""Wrapper module for Genshi template engine

This provides functions to render page by Genshi template engine.
"""

import os

from genshi.core import Markup
from genshi.template import TemplateLoader
from genshi.template.base import Context

__author__     = u'Yu I.'
__copyright__  = u'Copyright 2011, Yu Inao'
__credits__    = [u'None']
__license__    = u'MIT License'
__version__    = u'0.1.1'

TEMPLATE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             u'static',
                                             u'templates'))
loader = TemplateLoader([TEMPLATE_PATH],
                        auto_reload=True, # for development
                        max_cache_size=100)

def unescape(text):
    return Markup(text)

def render(name, **kwargs):
    template = loader.load(name)
    ctxt = Context(**kwargs)
    stream = template.generate(ctxt)

    return stream.render('html', doctype='html5')

if __name__ == '__main__':
    pass
