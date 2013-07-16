#!/usr/bin/env python

import unittest

from ExpensesShare import *

db = client['tests']


class UtilitiesTestCase(unittest.TestCase):

    def test_jsonify(self):
        obj = [
            "hello",
            ObjectId('51e4de669e615d19cb1bf486')
        ]
        assert jsonify(obj) == \
            '["hello", {"$oid": "51e4de669e615d19cb1bf486"}]'


class ExpensesShareTestCase(unittest.TestCase):

    def setUp(self):
        db.drop_collection('users')
        db.drop_collection('events')


if __name__ == '__main__':
    unittest.main()
