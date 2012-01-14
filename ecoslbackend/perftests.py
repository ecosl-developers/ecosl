#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# httplib2 does not work in Python 3 for https://, therefore python and not python3
#

# 
# This file is part of Ecological Shopping List II (ecosl).
# 
# Copyright (C) 2011 - 2012  Mika Tapojärvi
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# http://docs.python.org/library/unittest.html

import sys
import os
import unittest
import random
import httplib2


#
# Responses for the queries

content_languages_html_text = '1;Finnish;\n2;English;\n'
content_languages_xml = '<?xml version="1.0" ?>\n<itemlanguage_table>\n  <itemlanguage>\n    <id>\n      1\n    </id>\n    <language/>\n    Finnish\n  </itemlanguage>\n  <itemlanguage>\n    <id>\n      2\n    </id>\n    <language/>\n    English\n  </itemlanguage>\n</itemlanguage_table>\n\n'
content_stores_html_text = '1;K-Citymarket Raksila;\n2;Prisma Raksila;\n3;Siwa Muhos;\n4;K-Supermarket Mimmi;\n5;S-Market Koskiseutu;\n6;K-Citymarket Kaakkuri;\n7;Limingantullin Prisma;\n'
content_stores_xml = '<?xml version="1.0" ?>\n<store_table>\n  <store>\n    <id>\n      1\n    </id>\n    <name/>\n    K-Citymarket Raksila\n  </store>\n  <store>\n    <id>\n      2\n    </id>\n    <name/>\n    Prisma Raksila\n  </store>\n  <store>\n    <id>\n      3\n    </id>\n    <name/>\n    Siwa Muhos\n  </store>\n  <store>\n    <id>\n      4\n    </id>\n    <name/>\n    K-Supermarket Mimmi\n  </store>\n  <store>\n    <id>\n      5\n    </id>\n    <name/>\n    S-Market Koskiseutu\n  </store>\n  <store>\n    <id>\n      6\n    </id>\n    <name/>\n    K-Citymarket Kaakkuri\n  </store>\n  <store>\n    <id>\n      7\n    </id>\n    <name/>\n    Limingantullin Prisma\n  </store>\n</store_table>\n\n'

class PerfT(unittest.TestCase):

    def setUp(self):
        self.h = httplib2.Http('/tmp/.cache')
        self.h.disable_ssl_certificate_validation = True
        self.URL1 = 'https://projects.sse.fi/cgi-bin/ecoslbe1/'

    #def tearDown(self):
        #print('removing used database DISABLED')
        #os.remove(dbfile)

    def test_01_fetch_languages_html(self):
        response, content = self.h.request(self.URL1 + '?listaction=languages')
        self.assertEqual(content_languages_html_text, content)

    def test_02_fetch_languages_text(self):
        response, content = self.h.request(self.URL1 + '?listaction=languages&type=text')
        self.assertEqual(content_languages_html_text, content)

    def test_03_fetch_languages_xml(self):
        response, content = self.h.request(self.URL1 + '?listaction=languages&type=xml')
        self.assertEqual(content_languages_xml, content)

    def test_04_fetch_stores_html(self):
        response, content = self.h.request(self.URL1 + '?listaction=stores')
        self.assertEqual(content_stores_html_text, content)

    def test_05_fetch_stores_text(self):
        response, content = self.h.request(self.URL1 + '?listaction=stores&type=text')
        self.assertEqual(content_stores_html_text, content)

    def test_06_fetch_stores_xml(self):
        response, content = self.h.request(self.URL1 + '?listaction=stores&type=xml')
        self.assertEqual(content_stores_xml, content)



if __name__ == '__main__':
    """"Main function."""

    # Running tests one by one:
    # run individual tests:
    # $ python -m unittest perftests.PerfT.test_01_fetch_languages_html
    # $ python -m unittest perftests.PerfT.test_02_fetch_languages_text

    suite = unittest.TestLoader().loadTestsFromTestCase(PerfT)
    unittest.TextTestRunner(verbosity=2).run(suite)


