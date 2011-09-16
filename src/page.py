#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Page handling module

This is my basic template to start writing Python codes. This is now almost
based on Rob Knight's Python Coding Guidelines. In addition respective PEP 8.
"""

import datetime

from google.appengine.ext import db

import transformer
from dbmodels import WikiEntries

__author__ = 'Yu I.'
__copyright__ = 'Copyright 2011, Yu Inao'
__license__ = 'MIT License'
__version__ = '0.1'
__maintainer__ = 'Yu I.'
__status__ = 'Experiment'

class Page(object):
    """Abstraction for a wiki page

    This class handles all the wiki pages. First, you can call the page
    instance from `load` method with page name, or you can also check first if
    the page is existed or not from `hasentry` method with page name.
    """

    def __init__(self, name, entity=None):
        self.name = transformer.unquote(name)
        self.post_content = u''
        self.post_format = u''
        self.wikified_content = u''

        if entity:
            self.entity = entity
            self.name = self.entity.name
            self.wikified_content = \
                transformer.markdownize(self.wikify_content())
        else:
            self.entity = \
                WikiEntries(content=u'Write down new wiki entry here.')

    def view_url(self):
        return '/' + transformer.quote(self.name)

    def edit_url(self):
        return '/' + transformer.quote(self.name) + '?mode=edit'

    def remove_url(self):
        return '/' + transformer.quote(self.name) + '?mode=edit&action=remove'

    def get_entries(self):
        query = WikiEntries.all()

        query.order('-modified')

        return query.fetch(query.count())

    def wikify_content(self):
        transforms = [transformer.WikiWords(), transformer.AutoLink()]
        content = self.entity.content

        for transform in transforms:
            content = transform.run(content)

        return content

    def save(self):
        now = datetime.datetime.now()

        if not self.entity.created:
            self.entity.created = now

        self.entity.content = self.post_content
        self.entity.format = self.post_format
        self.entity.modified = now
        self.entity.name = self.name
        self.entity.name_normalized = self.name.replace(' ', '+').lower()

        self.entity.put()

    def remove(self):
        self.entity.delete()

    @staticmethod
    def load(name):
        normalized_name = transformer.normalize(name)
        query = WikiEntries.all()

        query.filter('name_normalized =', normalized_name).order('-modified')

        entity = query.get()
        page = Page(name, entity)

        if not entity:
            page = Page(name)

        return page

    @staticmethod
    def hasentry(name):
        flag = False
        normalized_name = transformer.normalize(name)
        query = WikiEntries.all()

        query.filter('name_normalized =', normalized_name)

        if query.count() >= 1:
            flag = True

        return flag

if __name__ == '__main__':
    pass
