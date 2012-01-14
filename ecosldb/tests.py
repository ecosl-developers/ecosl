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

dbfile='./unittest.db'
database = EcoDB(dbfile)

items = [
    ('täysmaito', 'täysmaito', 'whole milk', 0.80),                          #  1
    ('rasvatonmaito', 'rasvaton maito', 'skimmed milk', 0.80),               #  2
    ('kevytmaito', 'kevytmaito', 'semi-skimmed milk', 0.80),                 #  3
    ('ruisleipä', 'ruisleipä', 'rye bread', 2.50),                           #  4
    ('ranskanleipä', 'ranskanleipä', 'French bread', 2.25),                  #  5
    ('paahtoleipä, Viisi viljaa', 'paahtoleipä, Viisi viljaa', 'toast, Five Grain', 1.69),                           #  6
    ('Keiju-margariini, 400g', 'Keiju-margariini, 400g', 'Keiju margarine, 400g', 1.59),       #  7
    ('Flora-margariini', 'Flora-margariini', 'Flora margarine', 3.20),       #  8
    ('Oivariini', 'Oivariini', 'Oivariini margarine', 3.80 ),                #  9
    ('leivontamargariini', 'leivontamargariini', 'baking margarine', 1.20),  # 10
    ('Pirkka-kahvi', 'Pirkka-kahvi', 'Pirkka coffee', 4.00),                 # 11
    ('Saludo-kahvi', 'Saludo-kahvi', 'Saludo coffee', 4.20),                 # 12
    ('Presidentti-kahvi', 'Presidentti-kahvi', 'Presidentti coffee', 5.00),   # 13
    ('perunalastu, Taffel', 'perunalastu, Taffel', 'potato chips, Taffel', 2.75),  #
    ('dippi, Taffel', 'dippi, Taffel', 'dip sauce, Taffel', 1.04),  #
    ('dippi, Estrella', 'dippi, Estrella', 'dip sauce, Estrella', 1.50),  #
    ('nakkeja, HK', 'nakkeja, 830g, HK', 'sausages, 830g, HK', 6.99),  #
    ('nautajauheliha, 400g', 'nautajauheliha, 400g', 'minced beef (bovine), 400g', 2.95),  #
    ('nauta-sikajauheliha', 'nauta-sikajauheliha', 'minced beef (bovine, pork)', 1.50),  #
    ('kermaviili, Pirkka', 'kermaviili, Pirkka', 'sour cream, Pirkka', 1.50),  #
    ('kahvikerma', 'kahvikerma', 'coffee cream', 1.50),  #
    ('Marli Vital -mehu', 'Marli Vital -mehu', 'Marli Vital juice', 1.49),  #
    ('Sun-astiapesukoneaine, 70 kpl', 'Sun-astiapesukoneaine, 70 kpl', 'Sun machine dishwasher capsule', 1.50),  #
    ('jogurtti, banaani, Valio, 1 l', 'jogurtti, banaani, Valio, 1 l', 'yoghurt, banana, Valio', 1.50),  #
    ('jogurtti, mansikka Valio, 1 l', 'jogurtti, mansikka Valio, 1 l', 'yoghurt, strawberry, Valio', 1.50),  #
    ('tikkuperunoita', 'tikkuperunoita', 'potato sticks', 1.50),  #
    ('lihapyörykkä, HK', 'lihapyörykkä, HK', 'meat balls, HK', 1.50),  #
    ('nakkeja, Atria', 'nakkeja, Atria', 'sausages, Atria', 1.50),  #
    ('wok-kasvismix', 'wok-kasvismix', 'wok vegetable mix', 1.50),  #
    ('Lipton Yellow Label tee, 50 ps', 'Lipton Yellow Label tee, 50 ps', 'Lipton Yellow Label tea, 50 pcs', 1.50),  #
    ('hammasharja, lasten', 'hammasharja, lasten', 'toothbrush, for kids', 1.50),  #
    ('hammasharja, aikuisten', 'hammasharja, aikuisten', 'toothbrush, for adults', 1.50),  #
    ('ananas, tuore', 'ananas, tuore', 'ananas, fresh', 1.50),  #
    ('suklaanappirulla, Marabou', 'suklaanappirulla, Marabou', 'chocolate buttons, Marabou', 1.50),  #
    ('ylikypsä kinkkuleike, Atria', 'ylikypsä kinkkuleike, Atria', 'mellow ham slices, Atria', 1.50),  #
    ('keittokinkkuleike, Atria', 'keittokinkkuleike, Atria', 'ham slices, Atria', 1.50),  #
    ('Daimrulla, Marabou', 'Daimrulla, Marabou', 'Daim chocolate buttons, Marabou', 1.50),  #
    ('sipuli', 'sipuli', 'onion', 1.50),  #
    ('Lauantaipussi, Malaco', 'Lauantaipussi, Malaco', '', 1.50),  #
    ('Caesar-salaatti, Pirkka', 'Caesar-salaatti, Pirkka', '', 1.50),  #
    ('Ruiskiekko, Putaan Pulla', 'Ruiskiekko, Putaan Pulla', '', 1.50),  #
    ('italian pata -pussi, Blå Band', 'italian pata -pussi, Blå Band', '', 1.50),  #
    ('tex mex -pata -pussi, Blå Band', 'tex mex -pata -pussi, Blå Band', '', 1.50),  #
    ('appelsiinijuomatiiviste, Pirkka', 'appelsiinijuomatiiviste, Pirkka', '', 1.50),  #
    ('herkkutriojäätelö, Pingviini', 'herkkutriojäätelö, Pingviini', '', 1.50),  #
    ('nougatjäätelö, Pingviini', 'nougatjäätelö, Pingviini', '', 1.50),  #
    ('saaristolaisleike, Kalavalmis', 'saaristolaisleike, Kalavalmis', '', 1.50),  #
    ('kirjolohisuikale, Pirkka', 'kirjolohisuikale, Pirkka', '', 1.50),  #
    ('ylikypsä kinkkuleike, Snellman', 'ylikypsä kinkkuleike, Snellman', '', 1.50),  #
    ('muffinsi, kaakao, Pirkka', 'muffinsi, kaakao, Pirkka', '', 1.50),  #
    ('muffinsi, sitruuna, Pirkka', 'muffinsi, sitruuna, Pirkka', '', 1.50),  #
    ('jahtimakkara, Atria', 'jahtimakkara, Atria', '', 1.50),  #
    ('tomaatti, Suomi', 'tomaatti, Suomi', '', 1.50),  #
    ('ruisleipä, Oululainen Reissumies', 'ruisleipä, Oululainen Reissumies', '', 1.50),  #
    ('limsa, Hartwall Jaffa 1.5l, keltainen', 'limsa, Hartwall Jaffa 1.5l, keltainen', '', 1.50),  #
    ('limsa, Coca-Cola 1.5l', 'limsa, Coca-Cola 1.5l', '', 1.50),  #
    ('siideri, mansikka, Kopparberg', 'siideri, mansikka, Kopparberg', '', 1.50),  #
    ('juustosnacks, Taffel', 'juustosnacks, Taffel', '', 1.50),  #
    ('jogurtti, banaani, Valio, 8x125g', 'jogurtti, banaani, Valio, 8x125g', '', 1.50),  #
    ('tortillapohja, 8kpl/360g, Pirkka', 'tortillapohja, 8kpl/360g, Pirkka', '', 1.50),  #
    ('broilerin paistisuikale, Pirkka', 'broilerin paistisuikale, Pirkka', '', 1.50),  #
    ('olut, tumma lager, 0.5l, Pirkka', 'olut, tumma lager, 0.5l, Pirkka', '', 1.50),  #
    ('olut, vaalea lager, 0.33l, Pirkka', 'olut, vaalea lager, 0.33l, Pirkka', '', 0.83),  #
    ('juusto, emmental 400g, Pirkka', 'juusto, emmental 400g, Pirkka', '', 1.50),  #
    ('jääsalaatti, Pirkka', 'jääsalaatti, Pirkka', '', 1.50),  #
    ('tomaattimurska, 390g, Pirkka', 'tomaattimurska, 390g, Pirkka', '', 1.50),  #
    ('meetvursti, valkosipuli, Atria', 'meetvursti, valkosipuli, Atria', '', 1.50),  #
    ('salsadippi, keskivahva, 315g, Pirkka', 'salsadippi, keskivahva, 315g, Pirkka', '', 1.50),  #
    ('sinihomejuusto, Pirkka', 'sinihomejuusto, Pirkka', '', 1.50),  #
    ('valkohomejuusto, Pirkka', 'valkohomejuusto, Pirkka', '', 1.50),  #
    ('tuorekurkku, Suomi', 'tuorekurkku, Suomi', '', 1.50),  #
    ('kalkkunaleike, 250g, Atria', 'kalkkunaleike, 250g, Atria', '', 1.50),  #
    ('kananmuna, 15kpl', 'kananmuna, 15kpl', '', 1.50),  #
    ('kanan koipireisi', 'kanan koipireisi', '', 1.50),  #
    ('WC-paperi', 'WC-paperi', '', 1.50),  #
    ('talouspaperi', 'talouspaperi', '', 1.50),  #
    ('suihkusaippua, Bergamot', 'suihkusaippua, Bergamot', '', 1.50),  #
    ('suihkusaippua, Sport', 'suihkusaippua, Sport', '', 1.50)  #
    ]


languages= [
    'Finnish',
    'English'
    ]


stores= [
    'K-Citymarket Raksila',
    'Prisma Raksila',
    'Siwa Muhos',
    'K-Supermarket Mimmi',
    'S-Market Koskiseutu',
    'K-Citymarket Kaakkuri'
    ]

shoppinglists = [
    ['Ensimmäinen testilista', [[1, 3], [2, 3], [4, 1], [7, 1]]],
    ['The second testlist', [[2, 2], [9, 1], [13, 1], [5, 1], [4, 2], [7, 1]]],
    ['My list', [[1, 3], [2, 2], [13, 2], [5, 1], [4, 2], [7, 1], [10, 2], [11, 2]]]
    ]


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
            #print('list name: %s' % a_listname[0])  # debug
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

    def test_11_list_stores(self):
        stores_found = self.db.find_store([stores[0]])
        for a_store in stores_found:
            #print(a_store)
            pass
        stores_found = self.db.find_store([stores[2]])
        for a_store in stores_found:
            #print(a_store)
            pass
        stores_found = self.db.find_store([''])
        for a_store in stores_found:
            #print(a_store)
            pass

    def test_12_set_shopping_order(self):
        self.db.add_shoppingorder([stores[0], 1, 1])
        self.db.add_shoppingorder([stores[0], 2, 1])
        self.db.add_shoppingorder([stores[0], 3, 3])
        self.db.add_shoppingorder([stores[0], 4, 3])
        self.db.add_shoppingorder([stores[0], 7, 4])
        self.db.add_shoppingorder([stores[0], 9, 5])
        self.db.add_shoppingorder([stores[0], 13, 6])


        self.db.add_shoppingorder([stores[1], 1, 1])
        self.db.add_shoppingorder([stores[1], 2, 2])
        self.db.add_shoppingorder([stores[1], 3, 3])
        self.db.add_shoppingorder([stores[1], 4, 4])
        self.db.add_shoppingorder([stores[1], 7, 5])
        self.db.add_shoppingorder([stores[1], 9, 6])
        self.db.add_shoppingorder([stores[1], 13, 7])

    def test_13_find_languages(self):
        self.db.find_languages([languages[0]])
        self.db.find_languages([languages[1]])
        self.db.find_languages([''])

    def test_14_find_shopping_list_by_name(self):
        a_list = self.db.find_shopping_list_by_name([shoppinglists[0][0]])
        #print(a_list)
        a_list = self.db.find_shopping_list_by_name([shoppinglists[1][0]])
        #print(a_list)

    def test_15_find_shopping_list(self):
        
        #print('Ensimmäinen testilista, K-Citymarket Raksila, Finnish: ')
        for a_list in self.db.find_shopping_list(['Ensimmäinen testilista', 'K-Citymarket Raksila', 'Finnish']):
            #print(a_list)
            pass

        #print('The second testlist, K-Citymarket Raksila, Finnish: ')
        for a_list in self.db.find_shopping_list(['The second testlist', 'K-Citymarket Raksila', 'Finnish']):
            #print(a_list)
            pass

        # No language
        #print('The second testlist, K-Citymarket Raksila, no lang: ')
        for a_list in self.db.find_shopping_list(['The second testlist', 'K-Citymarket Raksila', '']):
            #print(a_list)
            pass

        # No store 
        #print('The second testlist, no store, Finnish: ')
        for a_list in self.db.find_shopping_list(['Ensimmäinen testilista', '', 'Finnish']):
            #print(a_list)
            pass

        # Find by ids
        for a_list in self.db.find_shopping_list_by_id([3, 1, 1]):
            #print(a_list)
            pass

    def test_16_find_shopping_order(self):
        for an_item in self.db.find_shopping_order([stores[0]]):
            #print(an_item)
            pass

        for an_item in self.db.find_shopping_order([stores[1]]):
            #print(an_item)
            pass

        for an_item in self.db.find_shopping_order([stores[2]]):
            #print(an_item)
            pass

    def test_17_modify_item(self):
        #for an_item in self.db.find_all_items('1'):
        #    print(an_item)
        self.db.modify_item([2, 'rasvaton maito'])
        self.db.modify_item([4, 'rukiinen leipä'])
        self.db.modify_item([7, 'keijumargariini'])
        self.db.modify_item([8, 'floramargariini'])
        #for an_item in self.db.find_all_items('1'):
        #    print(an_item)

    def test_18_modify_traslations(self):
        # <item id>, <language id>, "<new translation>"
        #for an_item in self.db.find_all_items('1'):
        #    print(an_item)
        #for an_item in self.db.find_all_items('2'):
        #    print(an_item)
        #print('----------------------------------')
        self.db.modify_translation([2, 1, 'Rasvaton Maito'])
        self.db.modify_translation([2, 2, 'Skimmed Milk'])
        self.db.modify_translation([3, 1, 'Kevyt Maito'])
        self.db.modify_translation([3, 2, 'Semi-Skimmed Milk'])
        self.db.modify_translation([6, 1, 'PaahtoLeipä'])
        self.db.modify_translation([6, 2, 'Toast'])
        #for an_item in self.db.find_all_items('1'):
        #    print(an_item)
        #for an_item in self.db.find_all_items('2'):
        #    print(an_item)

    def test_19_modify_amount_of_items(self):
        #for a_list in self.db.find_shopping_list([shoppinglists[0][0], '', '']):
        #    print(a_list)
        #print('-------------------------------------------')
        # <shopping list id>, <item id>, <amount>
        self.db.modify_amount_of_items([1, 1, 2])
        self.db.modify_amount_of_items([1, 2, 2])
        #for a_list in self.db.find_shopping_list([shoppinglists[0][0], '', '']):
        #    print(a_list)

    def test_20_remove_items_from_list(self):
        #for a_list in self.db.find_shopping_list([shoppinglists[1][0], '', '']):
        #    print(a_list)
        #print('-------------------------------------------')
        #print('removing French bread and Keiju margarine')
        # <shopping list id>, <item id>
        self.db.remove_item_from_list([2, 5])
        self.db.remove_item_from_list([2, 7])
        #print('-------------------------------------------')
        #for a_list in self.db.find_shopping_list([shoppinglists[1][0], '', '']):
        #    print(a_list)

    def test_21_modify_stores(self):
        #for a_store in self.db.find_store(['']):
        #    print(a_store)
        #print('-------------------------------------------')
        self.db.modify_store([1, 'Raksilan Cittari'])
        self.db.modify_store([2, 'Raksilan Prisma'])
        self.db.modify_store([3, 'Muhoksen Siwa'])

        # ...and back
        self.db.modify_store([1, 'K-Citymarket Raksila'])
        self.db.modify_store([2, 'Prisma Raksila'])
        self.db.modify_store([3, 'Siwa Muhos'])
        #for a_store in self.db.find_store(['']):
        #    print(a_store)

    def test_22_mark_items_bought(self):
        # <shopping list id>, <item id>, <bought> (bought = 1, not bought = 0)
        # buy
        self.db.mark_item_bought([3, 1, 1])
        self.db.mark_item_bought([3, 2, 1])
        self.db.mark_item_bought([3, 13, 1])

        # cancel buying
        self.db.mark_item_bought([3, 2, 0])
        self.db.mark_item_bought([3, 13, 0])


if __name__ == '__main__':
    """"Main function."""

    # Running tests one by one:
    # 1. remove the test db and run the script through so that new db is created:
    # $ rm unittest.sb ; ./tests.py
    #
    # 2. run individual tests:
    # $ python3 -m unittest tests.EcoDBTests.test_14_find_shopping_list_by_name
    # $ python3 -m unittest tests.EcoDBTests.test_15_find_shopping_list

    suite = unittest.TestLoader().loadTestsFromTestCase(EcoDBTests)
    unittest.TextTestRunner(verbosity=2).run(suite)


