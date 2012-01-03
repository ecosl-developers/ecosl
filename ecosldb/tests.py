#!/usr/bin/python3
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
        for an_item in items:
            self.db.add_item([an_item[0], 0])

    def test_03_add_languages(self):
        for a_lang in languages:
            self.db.add_language([a_lang])

    def test_04_add_translations(self):
        for an_item in items:
            self.db.add_translationname([an_item[0], '1', an_item[1]])
            self.db.add_translationname([an_item[0], '2', an_item[2]])

    def test_05_find_all_items(self):
        for an_item in self.db.find_all_items('1'):
            #print(an_item)
            pass

        for an_item in self.db.find_all_items('2'):
            #print(an_item)
            pass

    def test_06_find_single_items(self):
        for an_item in self.db.find_item_name(['täysmaito', '0']):
            #print(an_item)
            pass

        for an_item in self.db.find_item_name(['täysmaito', '1']):
            #print(an_item)
            pass

        for an_item in self.db.find_item_name(['täysmaito', '2']):
            #print(an_item)
            pass

if __name__ == '__main__':
    """"Main function."""

    dbfile='./unittest.db'
    database = EcoDB(dbfile)

    items = [('täysmaito', 'täysmaito', 'whole milk'),
        ('rasvatonmaito', 'rasvaton maito', 'skimmed milk'),
        ('kevytmaito', 'kevytmaito', 'semi-skimmed milk'),
        ('ruisleipä', 'ruisleipä', 'rye bread'),
        ('ranskanleipä', 'ranskanleipä', 'French bread'),
        ('paahtoleipä', 'paahtoleipä', 'toast'),
        ('Keiju-margariini', 'Keiju-margariini', 'Keiju margarine'),
        ('Flora-margariini', 'Flora-margariini', 'Flora margarine'),
        ('Oivariini', 'Oivariini', 'Oivariini margarine'),
        ('leivontamargariini', 'leivontamargariini', 'baking margarine'),
        ('Pirkka-kahvi', 'Pirkka-kahvi', 'Pirkka coffee'),
        ('Saludo-kahvi', 'Saludo-kahvi', 'Saludo coffee'),
        ('Presidentti-kahvi', 'Presidentti-kahvi', 'Presidentti coffee')]


    languages= ['Finnish',
        'English']



    suite = unittest.TestLoader().loadTestsFromTestCase(EcoDBTests)
    unittest.TextTestRunner(verbosity=2).run(suite)



