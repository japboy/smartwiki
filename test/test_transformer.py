#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""Test case module for Transformer module"""

import re
import unittest
import urllib

import markdown

from google.appengine.ext import testbed

import page
from dbmodels import WikiEntries

# Testee
import transformer

__author__     = u'Yu I.'
__credits__    = [u'None']
__license__    = u'Public domain'
__version__    = u'0.1.1'

UNQUOTED_UNICODE = u'テスト ページ'
QUOTED_UNICODE = u'%E3%83%86%E3%82%B9%E3%83%88+%E3%83%9A%E3%83%BC%E3%82%B8'
QUOTED_STRING = '%E3%83%86%E3%82%B9%E3%83%88+%E3%83%9A%E3%83%BC%E3%82%B8'
MARKDOWN_UNICODE = u'# Header 1 {#head1}'
HTML_UNICODE = u'<h1 id="head1">Header 1</h1>'
TEXT_UNICODE = u"""これは、テストページです。"""
LINKFIED_TEXT_UNICODE = u"""これは、<a href="/%E3%83%86%E3%82%B9%E3%83%88%E3%83%9A%E3%83%BC%E3%82%B8">テストページ</a>です。"""

class URLToolsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_quote(self, path=UNQUOTED_UNICODE):
        self.assertIsInstance(path, unicode)

        encoded_path = path.encode('utf-8')

        self.assertIsInstance(encoded_path, str)

        quoted_path = urllib.quote_plus(encoded_path)

        self.assertEqual(quoted_path, QUOTED_STRING)

        final_quoted_path = unicode(quoted_path, 'utf-8')

        self.assertEqual(final_quoted_path, QUOTED_UNICODE)

    def test_unquote(self, path=QUOTED_UNICODE):
        self.assertIsInstance(path, unicode)

        encoded_path = path.encode('utf-8')

        self.assertIsInstance(encoded_path, str)

        unquoted_path = urllib.unquote(encoded_path)

        self.assertEqual(unquoted_path, 'テスト+ページ')

        unquted_unquoted_path = urllib.unquote_plus(unquoted_path)

        self.assertEqual(unquted_unquoted_path, 'テスト ページ')

        final_unquoted_path = unicode(unquted_unquoted_path, 'utf-8')

        self.assertEqual(final_unquoted_path, UNQUOTED_UNICODE)

    def test_normalize(self, path=QUOTED_UNICODE):
        self.assertIsInstance(path, unicode)

        unquoted = transformer.unquote(path)

        self.assertEqual(unquoted, UNQUOTED_UNICODE)

        normalized_unquoted = unquoted.replace(u' ', u'+').lower()

        self.assertEqual(normalized_unquoted, u'テスト+ページ')

    def test_isvalid(self, path=QUOTED_UNICODE):
        pattern = re.compile(r'[^!#&+,./:=?_\s][^!#&,./:=?]+', re.UNICODE)
        matched = pattern.match(transformer.unquote(path))

        if matched:
            self.assertNotEqual(matched, None)

            flag = True
        else:
            self.assertEqual(matched, None)

            flag = False

        self.assertIsInstance(flag, bool)

class KeywordLinkTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()

        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

        entity = WikiEntries(name=u'テストページ')

        entity.put()

    def tearDown(self):
        self.testbed.deactivate()

    def test_linkfy_keyword(self, text=TEXT_UNICODE):
        query = WikiEntries().all()
        entities = query.fetch(query.count())
        keywords = list(set([entity.name for entity in entities]))

        for keyword in keywords:
            text = text.replace(keyword, u'<a href="/%s">%s</a>' % (transformer.quote(keyword), keyword))

        self.assertEqual(text, LINKFIED_TEXT_UNICODE)

class MarkdownTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_markdownize(self, text=MARKDOWN_UNICODE):
        md = markdown.Markdown(extensions=['extra'],
                               output_format='html4')

        self.assertIsInstance(md, markdown.Markdown)
        self.assertEqual(md.convert(text), HTML_UNICODE)

if __name__ == '__main__':
    pass
