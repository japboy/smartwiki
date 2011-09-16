#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Transformer module

This module include some tools for wiki entry conversion.
"""

import re
import urllib

import markdown
import page

__author__ = 'Yu I.'
__copyright__ = 'Copyright 2011, Yu Inao'
__license__ = 'MIT License'
__version__ = '0.1'
__maintainer__ = 'Yu I.'
__status__ = 'Experiment'

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

    return unquoted.replace(' ', '+').lower()

def isvalid(path):
    flag = False
    pattern = re.compile(r'[\s!#&,./:=?_]+')
    matched = pattern.match(unquote(path))

    if not matched:
        flag = True

    return flag

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

class WikiWords(Transform):
    def __init__(self):
        self.regexp = re.compile(u'([^\s][A-Za-z0-9ぁ-ヶ亜-黑]+[^\s])', re.UNICODE)

    def replace(self, match):
        wikiword = match.group(1)

        if page.Page.hasentry(quote(wikiword)):
            return u'<a href="/%s">%s</a>' % (wikiword, wikiword)
        else:
            return wikiword

class AutoLink(Transform):
    def __init__(self):
        self.regexp = re.compile(u'(.*)(https?:\/\/[A-Za-z0-9\/\.][^\s]+)',
                                 re.UNICODE)

    def replace(self, match):
        url = match.group(2)

        return match.group(1) + u'<a href="%s">%s</a>' % (url, url)

if __name__ == '__main__':
    pass
