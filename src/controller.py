#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""Request handler module

This is request handler. All of the application request will be handled here.
"""

import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import template
import transformer
from page import Page
from page import get_entries

__author__     = u'Yu I.'
__copyright__  = u'Copyright 2011, Yu Inao'
__credits__    = [u'None']
__license__    = u'MIT License'
__version__    = u'0.1.1'

class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        logging.warn(repr(self.value))
        return

class BaseRequestHandler(webapp.RequestHandler):
    """Abstraction for request handler

    This implementation is based on cccwiki
        Copyright 2008 Google Inc.
        Author: Bret Taylor
        License: Apache License
    """

    def generate(self, template_name, **template_values):
        """Page generator method

        This method write out a page using Django template. Template HTMLs are
        read from `templates` sub directory.
        """

        common_values = {'application_name': u'スマートウィキ',
                         'user': None}

        if not template_values.has_key('message'):
            template_values.update({'message': None})

        template_values.update(common_values)
        self.response.out.write(template.render(template_name,
                                                **template_values))

class WikiPage(BaseRequestHandler):
    """The request handler for all the requests

    This class handles all the requests to wiki pages. First of all, checking
    if page entity exists or not, then loading it if exsiting, or loading
    editor page if not existing. GET method loads editor page if URL query has
    `mode=edit` as well. POST method handles edit operations.
    """

    def get(self, page_name):
        """Request GET handling method

        This method handles all the GET requests to wiki pages. The argument
        should be the URL path & query string. Remember the argument is unicode
        object and is quoted and encoded as UTF-8.
        """

        query_string = self.request.query_string

        try:
            queries = \
                dict(item.split(u'=') for item in query_string.split(u'&'))
        except ValueError, e:
            logging.warn(e)

        if not page_name:
            page_name = u'メインページ'
            self.redirect(u'/' + transformer.quote(page_name))
            return

        page = Page.load(page_name)
        mode = self.request.get('mode')
        action = self.request.get('action')
        responses = {}

        if not transformer.isvalid(page_name):
            mode = u'error'
            responses.update({'message': {'type': u'warn',
                                          'text': u'ページ名が不正です。' + \
                                                 u'メインページに戻ります。'}})

            self.error(400)
        elif not page.exists() and not mode:
            self.redirect(u'/' + page_name + u'?mode=edit')
            return
        elif not page.exists() and mode:
            responses.update({'message': {'type': u'warn',
                                          'text': u'“' + \
                                            transformer.unquote(page_name) + \
                              u'”はありません。あなたが最初の投稿者です。'}})
        elif page.exists() and not mode:
            mode = u'view'
        elif page.exists() and mode == 'edit' and action == 'remove':
            self.delete(page_name)
            responses.update({'message': {'type': u'warn',
                                          'text': u'“' + \
                                            transformer.unquote(page_name) + \
                              u'”を削除しました。作り直すこともできます。'}})

        responses.update({'page': page, 'entries': get_entries()})

        self.generate(mode + u'.html', **responses)

    def post(self, page_name):
        """Request POST handling method

        This method handles all the POST requests to wiki pages. It's almost
        same as GET method.
        """

        page = Page.load(page_name)

        page.name = self.request.get('name')
        page.post_requests[u'content'] = self.request.get('content')
        page.post_requests[u'format'] = self.request.get('format')

        page.save()
        self.redirect(page.path[u'view'])

    def delete(self, page_name):
        """Request DELETE handling method"""

        page = Page.load(page_name)

        page.remove()

def main():
    application = webapp.WSGIApplication([(r'/(.*)[/#]?', WikiPage)],
                                         debug=True)

    run_wsgi_app(application)

if __name__ == '__main__':
    main()
