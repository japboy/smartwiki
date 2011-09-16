#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Request handler module

This is request handler. All of the application request will be handled here.
"""

import os
import urllib
import urlparse

from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import transformer
from page import Page

__author__ = 'Yu I.'
__copyright__ = 'Copyright 2011, Yu Inao'
__license__ = 'MIT License'
__version__ = '0.1'
__maintainer__ = 'Yu I.'
__status__ = 'Experiment'

class BaseRequestHandler(webapp.RequestHandler):
    """Abstraction for request handler

    This implementation is based on cccwiki
        Copyright 2008 Google Inc.
        Author: Bret Taylor
        License: Apache License
    """

    def generate(self, template_name, template_value={}):
        """Page generator method

        This method write out a page using Django template. Template HTMLs are
        read from `templates` sub directory.
        """

        values = {'application_name': u'スマートウィキ',
                  'user': None}

        values.update(template_value)

        directory = os.path.dirname(__file__)
        path = os.path.join(directory, os.path.join('templates', template_name))

        self.response.out.write(template.render(path, values))

class WikiPage(BaseRequestHandler):
    """The request handler for all the requests

    This class handles all the requests to wiki pages. First of all, checking
    if page entity exists or not, then loading it if exsiting, or loading
    editor page if not existing. GET method loads editor page if URL query has
    `mode=edit` as well. POST method handles edit operations.
    """

    def get(self, path_and_query):
        """Request GET handling method

        This method handles all the GET requests to wiki pages. The argument
        should be the URL path & query string. Remember the argument is unicode
        object and is quoted and encoded as UTF-8.
        """

        if not path_and_query:
            page_name = u'メインページ'
            self.redirect(u'/' + transformer.quote(page_name))
            return

        url = urlparse.urlparse(path_and_query)
        page_name = url.path
        page_exists = Page.hasentry(page_name)
        mode = self.request.get('mode')
        action = self.request.get('action')
        responses = {}

        if not transformer.isvalid(page_name):
            mode = u'error'
            responses.update({'message': {'type': u'warn',
                                          'text': u'ページ名が不正です。' + \
                                                 u'メインページに戻ります。'}})

            self.error(400)
        elif not page_exists and not mode:
            self.redirect(u'/' + page_name + u'?mode=edit')
            return
        elif not page_exists and mode:
            responses.update({'message': {'type': u'warn',
                                          'text': u'“' + \
                                            transformer.unquote(page_name) + \
                              u'”はありません。あなたが最初の投稿者です。'}})
        elif page_exists and not mode:
            mode = u'view'
        elif page_exists and mode == 'edit' and action == 'remove':
            self.delete(page_name)
            responses.update({'message': {'type': u'warn',
                                          'text': u'“' + \
                                            transformer.unquote(page_name) + \
                              u'”を削除しました。作り直すこともできます。'}})

        page = Page.load(page_name)

        responses.update({'page': page})

        self.generate(mode + u'.html', responses)

    def post(self, page_name):
        """Request POST handling method

        This method handles all the POST requests to wiki pages. It's almost
        same as GET method.
        """

        page = Page.load(page_name)

        page.name = self.request.get('name')
        page.post_content = self.request.get('content')
        page.post_format = self.request.get('format')

        page.save()
        self.redirect(page.view_url())

    def delete(self, page_name):
        """Request DELETE handling method"""

        page = Page.load(page_name)

        page.remove()

def main():
    application = webapp.WSGIApplication([(r'/(.*)#?', WikiPage)],
                                         debug=True)

    run_wsgi_app(application)

if __name__ == '__main__':
    main()
