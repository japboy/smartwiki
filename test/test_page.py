#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""Test case module for Page module"""

import datetime
import logging
import unittest

from google.appengine.ext import testbed

import transformer
from dbmodels import WikiEntries

# Testee
import page

__author__     = u'Yu I.'
__credits__    = [u'None']
__license__    = u'Public domain'
__version__    = u'0.1.1'

QUOTED_NAME_UNICODE = u'%E3%83%86%E3%82%B9%E3%83%88%E3%83%9A%E3%83%BC%E3%82%B8'

class ToolTestCase(unittest.TestCase):
    def setUp(self, name=QUOTED_NAME_UNICODE, entity=None):
        self.testbed = testbed.Testbed()

        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_get_entries(self):
        query = WikiEntries.all()

        query.order('-modified')
        query.fetch(query.count())
        # FIXME: Do test!

class PageTestCase(unittest.TestCase):
    def setUp(self, name=QUOTED_NAME_UNICODE, entity=None):
        self.testbed = testbed.Testbed()

        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

        # __init__ processes

        self.name = transformer.unquote(name)
        self.post_requests = {u'content': u'',
                              u'format': u'markdown-extra'}
        self.path = {u'view': '/' + transformer.quote(self.name),
                     u'edit': '/' + transformer.quote(self.name) + '?mode=edit',
                     u'remove':
                '/' + transformer.quote(self.name) + '?mode=edit&action=remove',
                     u'newpage':
                  '/' + transformer.quote(u'新しいページ') + '?mode=edit'}

        if entity:
            self.existence = True
            self.entity = entity
            self.name = self.entity.name
            self.content = self.wikify_content()
        else:
            self.existence = False
            self.entity = \
                WikiEntries(content=u'新しい wiki エントリーを書いて下さい。')

    def tearDown(self):
        self.testbed.deactivate()

    def test_load(self, name=QUOTED_NAME_UNICODE):
        normalized_name = transformer.normalize(name)
        query = WikiEntries.all()

        query.filter(u'name_normalized =', normalized_name).order(u'-modified')

        entity = query.get()

        if entity:
            page_ = page.Page(name, entity)
        else:
            page_ = page.Page(name)

        self.assertIsInstance(page_, page.Page)

    def test_exists(self):
        self.assertIsInstance(self.existence, bool)

    def test_remove(self):
        try:
            self.entity.delete()
        except NotSavedError:
            logging.warn(u'Non existed entry is requested to remove.')
        # Not tested yet

    def test_save(self):
        now = datetime.datetime.now()

        if not self.entity.created:
            self.entity.created = now

        self.entity.content = self.post_requests[u'content']
        self.entity.format = self.post_requests[u'format']
        self.entity.modified = now
        self.entity.name = self.name
        self.entity.name_normalized = transformer.normalize(self.name)

        self.entity.put()
        self.assertEqual(1, len(self.entity.all().fetch(10)))

    def test_wikify_content(self):
        transforms = [transformer.AutoLink()]
        content = self.entity.content

        for transform in transforms:
            content = transform.run(content)

        return transformer.markdownize(transformer.linkfy_keyword(content))
        # Not tested yet

if __name__ == '__main__':
    pass
