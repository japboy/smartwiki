#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""Datastore model module

This contains Datastore models for wiki entries.
"""

from google.appengine.ext import db

__author__     = u'Yu I.'
__copyright__  = u'Copyright 2011, Yu Inao'
__credits__    = [u'None']
__license__    = u'MIT License'
__version__    = u'0.1.1'

class WikiEntries(db.Model):
    """Basic wiki entry model

    This is basic model for wiki entries. History recording is not yet
    supported.
    """

    content = db.TextProperty()
    format = db.StringProperty()
    created = db.DateTimeProperty()
    modified = db.DateTimeProperty()
    name = db.StringProperty()
    name_normalized = db.StringProperty()
    user = db.StringProperty()

if __name__ == '__main__':
    pass
