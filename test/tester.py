#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test suite & runner module

This is the wrapper module of all the tests. This tester depends on Google App
Engine SDK.
"""

import os
import sys
import unittest

__author__ = 'Yu I.'
__copyright__ = 'Copyright 2011, Yu I.'
__license__ = 'Public domain'
__version__ = '0.1'

SDK_PATH = '/path/to/google_appengine-1.5.4'
APP_PATH = '/path/to/com.appspot.driwak/src'
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
