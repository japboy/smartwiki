#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""Transformer module

This module include some tools for wiki entry conversion.
"""

import logging
import re
import urllib

import markdown

import page
from dbmodels import WikiEntries

__author__     = u'Yu I.'
__copyright__  = u'Copyright 2011, Yu Inao'
__credits__    = [u'None']
__license__    = u'MIT License'
__version__    = u'0.1.1'

def quote(path):
    encoded = path.encode('utf-8')
    quoted = urllib.quote_plus(encoded)

    return unicode(quoted, 'utf-8')

def unquote(path):
    encoded = path.encode('utf-8')
    unquoted = urllib.unquote(encoded)
    unquoted_unquoted = urllib.unquote_plus(unquoted)

    return unicode(unquoted_unquoted, 'utf-8')

def normalize(path):
    unquoted = unquote(path)

    return unquoted.replace(u' ', u'+').lower()

def isvalid(path):
    pattern = re.compile(r'[^!#&+,./:=?_\s][^!#&,./:=?]+', re.UNICODE)
    matched = pattern.match(unquote(path))

    if matched:
        flag = True
    else:
        flag = False

    return flag

def linkfy_keyword(text):
    query = WikiEntries().all()
    entities = query.fetch(query.count())
    keywords = list(set([entity.name for entity in entities]))

    for keyword in keywords:
        text = text.replace(keyword,
                            u'<a href="/%s">%s</a>' % (quote(keyword), keyword))

    return text

def markdownize(text):
    md = markdown.Markdown(extensions=['extra'],
                           output_format='html4')

    return md.convert(text)

class Transform(object):
    def run(self, content):
        parts = []
        offset = 0

        for match in self.regexp.finditer(content):
            parts.append(content[offset:match.start(0)])
            parts.append(self.replace(match))

            offset = match.end(0)

        parts.append(content[offset:])
        return ''.join(parts)

class AutoLink(Transform):
    def __init__(self):
        self.regexp = re.compile(r'(.*)([^(]https?:\/\/[A-Za-z0-9\/\.[^\s)]]+)',
                                 re.UNICODE)

    def replace(self, match):
        url = match.group(2)

        return match.group(1) + u'<a href="%s">%s</a>' % (url, url)

if __name__ == '__main__':
    pass
