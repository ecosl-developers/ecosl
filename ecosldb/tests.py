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

    def test_07_add_stores(self):
        for a_store in stores:
            self.db.add_store([a_store])

    def test_08_add_shoppinglists(self):
        for a_listname in shoppinglists:
            self.db.add_shoppinglist([a_listname[0]])

    def test_09_add_and_update_price(self):
        index = 1
        for an_item in items:
            #print(an_item[0] + ' costs ' + str(an_item[3]))
            self.db.add_price([index, 1, str(an_item[3])])
            index += 1

        # Changing a few prices
        self.db.add_price([1, 1, 0.85])
        self.db.add_price([4, 1, 3.50])
        self.db.add_price([10, 1, 1.50])

        # Adding the same price again for few
        self.db.add_price([2, 1, 0.75])
        self.db.add_price([5, 1, 2.25])
        self.db.add_price([6, 1, 1.75])

    def test_10_add_items_to_shoppinglist(self):
        for a_list in shoppinglists:
            self.db.add_to_list(a_list[0], a_list[1])



if __name__ == '__main__':
    """"Main function."""

    dbfile='./unittest.db'
    database = EcoDB(dbfile)

    items = [
        ('täysmaito', 'täysmaito', 'whole milk', 0.75),
        ('rasvatonmaito', 'rasvaton maito', 'skimmed milk', 0.75),
        ('kevytmaito', 'kevytmaito', 'semi-skimmed milk', 0.75),
        ('ruisleipä', 'ruisleipä', 'rye bread', 2.50),
        ('ranskanleipä', 'ranskanleipä', 'French bread', 2.25),
        ('paahtoleipä', 'paahtoleipä', 'toast', 1.75),
        ('Keiju-margariini', 'Keiju-margariini', 'Keiju margarine', 3.50),
        ('Flora-margariini', 'Flora-margariini', 'Flora margarine', 3.20),
        ('Oivariini', 'Oivariini', 'Oivariini margarine', 3.80 ),
        ('leivontamargariini', 'leivontamargariini', 'baking margarine', 1.20),
        ('Pirkka-kahvi', 'Pirkka-kahvi', 'Pirkka coffee', 4.00),
        ('Saludo-kahvi', 'Saludo-kahvi', 'Saludo coffee', 4.20),
        ('Presidentti-kahvi', 'Presidentti-kahvi', 'Presidentti coffee', 5.00)
        ]


    languages= [
        'Finnish',
        'English'
        ]


    stores= [
        'K-Citymarket Raksila',
        'Prisma Raksila',
        'Siwa Muhos'
        'K-Supermarket Mimmi',
        'S-Market Koskiseutu',
        'K-Citymarket Kaakkuri'
        ]

    shoppinglists = [
        ['Ensimmäinen testilista', [[1, 3], [2, 3], [4, 1], [7, 1]]],
        ['The second testlist', [[2, 2], [9, 1], [13, 1]]]
        ]


    suite = unittest.TestLoader().loadTestsFromTestCase(EcoDBTests)
    unittest.TextTestRunner(verbosity=2).run(suite)



