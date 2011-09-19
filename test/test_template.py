#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""Test case module for Template module"""

import os
import unittest

import genshi
from genshi.core import Markup
from genshi.template import TemplateLoader
from genshi.template.base import Context

__author__     = u'Yu I.'
__credits__    = [u'None']
__license__    = u'Public domain'
__version__    = u'0.1.1'

ESCAPED_UNICODE = u'&lt;a href="http://example.com"&gt;こちら!&lt;/a&gt;'
UNESCAPED_UNICODE = u'<a href="http://example.com">こちら!</a>'

class TemplateTestCase(unittest.TestCase):
    def setUp(self):
        template_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                     u'..',
                                                     u'src',
                                                     u'static',
                                                     u'templates'))
        self.loader = TemplateLoader([template_path],
                                     auto_reload=True, # for development
                                     max_cache_size=100)

    def tearDown(self):
        pass

    def test_unescape(self, text=ESCAPED_UNICODE):
        self.assertIsInstance(text, unicode)

        unescaped_text = Markup(text)

        self.assertIsInstance(unescaped_text, Markup)
        self.assertEqual(unescaped_text, UNESCAPED_UNICODE)

    def test_render(self, name=u'foundation.html', **kwargs):
        template = self.loader.load(name)

        self.assertIsInstance(template, genshi.template.MarkupTemplate)

        ctxt = Context(**kwargs)

        self.assertIsInstance(ctxt, Context)

        stream = template.generate(ctxt)

        self.assertIsInstance(stream, genshi.core.Stream)
        self.assertIsInstance(stream.render('html', doctype='html5'), str)

if __name__ == '__main__':
    pass
