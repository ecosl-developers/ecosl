#!/usr/bin/python
# -*- coding: UTF-8 -*-

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
from ecosldb import EcoDB
import unittest
import random


class EcoDBTests(unittest.TestCase):

    def setUp(self):
        self.dbfile = dbfile
        self.db = database

    #def tearDown(self):
        #print('removing used database DISABLED')
        #os.remove(dbfile)

    def test_01_create_db(self):
        if not os.path.exists(self.dbfile) or not os.path.isfile(self.dbfile):
            database.create_empty_database();

    def test_02_add_items(self):
        items = ['täysmaito',
            'rasvatonmaito',
            'kevytmaito',
            'ruisleipä',
            'ranskanleipä',
            'paahtoleipä',
            'Keiju-margariini',
            'Flora-margariini',
            'Oivariini',
            'leivontamargariini',
            'Pirkka-kahvi',
            'Saludo-kahvi',
            'Presidentti-kahvi']

        for an_item in items:
            self.db.add_item([an_item, 0])


if __name__ == '__main__':
    """"Main function."""

    dbfile='./unittest.db'
    database = EcoDB(dbfile)

    suite = unittest.TestLoader().loadTestsFromTestCase(EcoDBTests)
    unittest.TextTestRunner(verbosity=2).run(suite)



