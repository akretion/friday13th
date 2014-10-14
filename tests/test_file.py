# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os

from friday13th.jason import File

TESTS_DIRPATH = os.path.abspath(os.path.dirname(__file__))
DATA_DIRPATH = os.path.join(TESTS_DIRPATH, 'data')


class TestFriday13th(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFriday13th, self).__init__(*args, **kwargs)
        self.maxDiff = None

    def setUp(self):
        self.file = File(os.path.join(DATA_DIRPATH, 'test.json'))

if __name__ == '__main__':
    unittest.main()
