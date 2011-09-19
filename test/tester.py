#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""Test suite & runner module

This is the wrapper module of all the tests for Google App Engine SDK. This will
automatically read `test_*.py` in the same directory and run the tests.
"""

import os
import sys
import unittest

__author__     = u'Yu I.'
__credits__    = [u'None']
__license__    = u'Public domain'
__version__    = u'0.2'

SDK_PATH = os.path.join(os.path.expanduser(u'~'),
                        u'Applications/google_appengine-1.5.4')
APP_PATH = os.path.join(os.path.expanduser(u'~'),
                        u'Workspace/com.appspot.driwak/src')
TEST_PATH = os.path.dirname(__file__)

def main(sdk_path=SDK_PATH, app_path=APP_PATH, test_path=TEST_PATH):
    sys.path.insert(0, sdk_path)
    sys.path.insert(1, app_path)

    import dev_appserver

    dev_appserver.fix_sys_path()

    suite = unittest.loader.TestLoader().discover(test_path, 'test_*.py')

    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()
