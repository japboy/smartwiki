#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""Page handling module

This is my basic template to start writing Python codes. This is now almost
based on Rob Knight's Python Coding Guidelines. In addition respective PEP 8.
"""

import datetime
import logging

import template
import transformer
from dbmodels import WikiEntries

__author__     = u'Yu I.'
__copyright__  = u'Copyright 2011, Yu Inao'
__credits__    = [u'None']
__license__    = u'MIT License'
__version__    = u'0.1.1'

def get_entries():
    query = WikiEntries.all()

    query.order('-modified')

    return query.fetch(query.count())

class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Page(object):
    """Abstraction for a wiki page

    This class handles all the wiki pages. First, you can call the page
    instance from `load` method with page name, or you can also check first if
    the page is existed or not from `hasentry` method with page name.
    """

    def __init__(self, name, entity=None):
        self.name = transformer.unquote(name)
        self.post_requests = {u'content': u'', u'format': u''}
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
            self.content = template.unescape(self.wikify_content())
        else:
            self.existence = False
            self.entity = \
                WikiEntries(content=u'新しい wiki エントリーを書いて下さい。')

    @staticmethod
    def load(name):
        normalized_name = transformer.normalize(name)
        query = WikiEntries.all()

        query.filter(u'name_normalized =', normalized_name).order(u'-modified')

        entity = query.get()

        if entity:
            page = Page(name, entity)
        else:
            page = Page(name)

        return page

    def exists(self):
        return self.existence

    def remove(self):
        try:
            self.entity.delete()
        except NotSavedError:
            logging.warn(u'Non existed entry is requested to remove.')

    def save(self):
        now = datetime.datetime.now()

        if not self.entity.created:
            self.entity.created = now

        self.entity.content = self.post_requests[u'content']
        self.entity.format = self.post_requests[u'format']
        self.entity.modified = now
        self.entity.name = self.name
        self.entity.name_normalized = transformer.normalize(self.name)

        self.entity.put()

    def wikify_content(self):
        transforms = [transformer.AutoLink()]
        content = self.entity.content

        for transform in transforms:
            content = transform.run(content)

        return transformer.markdownize(transformer.linkfy_keyword(content))

if __name__ == '__main__':
    pass
