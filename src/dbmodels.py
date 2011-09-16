#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Datastore model module

This contains Datastore models for wiki entries.
"""

from google.appengine.ext import db

__author__ = 'Yu I.'
__copyright__ = 'Copyright 2011, Yu Inao'
__license__ = 'MIT License'
__version__ = '0.1'
__maintainer__ = 'Yu I.'
__status__ = 'Experiment'

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
