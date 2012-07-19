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
import hashlib

dbfile='./unittest.db'
database = EcoDB(dbfile)

items = [
    ('täysmaito', 'täysmaito', 'whole milk', 0.80),                                                                                       #  1
    ('rasvatonmaito', 'rasvaton maito', 'skimmed milk', 0.80),                                                                            #  2
    ('kevytmaito', 'kevytmaito', 'semi-skimmed milk', 0.80),                                                                              #  3
    ('ruisleipä', 'ruisleipä', 'rye bread', 2.50),                                                                                        #  4
    ('ranskanleipä', 'ranskanleipä', 'French bread', 2.25),                                                                               #  5
    ('paahtoleipä, Viisi viljaa', 'paahtoleipä, Viisi viljaa', 'toast, Five Grain', 1.69),                                                #  6
    ('Keiju-margariini, 400g', 'Keiju-margariini, 400g', 'Keiju margarine, 400g', 1.59),                                                  #  7
    ('Flora-margariini', 'Flora-margariini', 'Flora margarine', 3.20),                                                                    #  8
    ('Oivariini', 'Oivariini', 'Oivariini margarine', 3.80 ),                                                                             #  9
    ('leivontamargariini', 'leivontamargariini', 'baking margarine', 1.20),                                                               #  10
    ('Pirkka-kahvi', 'Pirkka-kahvi', 'Pirkka coffee', 4.00),                                                                              #  11
    ('Saludo-kahvi', 'Saludo-kahvi', 'Saludo coffee', 4.20),                                                                              #  12
    ('Presidentti-kahvi', 'Presidentti-kahvi', 'Presidentti coffee', 5.00),                                                               #  13
    ('perunalastu, Taffel', 'perunalastu, Taffel', 'potato chips, Taffel', 2.75),                                                         #  14
    ('dippi, Taffel', 'dippi, Taffel', 'dip sauce, Taffel', 1.04),                                                                        #  15
    ('dippi, Estrella', 'dippi, Estrella', 'dip sauce, Estrella', 1.50),                                                                  #  16
    ('nakkeja, HK', 'nakkeja, 830g, HK', 'sausages, 830g, HK', 6.99),                                                                     #  17
    ('nautajauheliha, 400g', 'nautajauheliha, 400g', 'minced beef (bovine),', 2.95),                                                      #  18
    ('nauta-sikajauheliha', 'nauta-sikajauheliha', 'minced beef (bovine, pork)', 2.49),                                                   #  19
    ('kermaviili, Pirkka', 'kermaviili, Pirkka', 'sour cream, Pirkka', 0.55),                                                             #  20
    ('kahvikerma', 'kahvikerma', 'coffee cream', 1.50),                                                                                   #  21
    ('Marli Vital -mehu', 'Marli Vital -mehu', 'Marli Vital juice', 1.49),                                                                #  22
    ('Sun-astiapesukoneaine, 70 kpl', 'Sun-astiapesukoneaine, 70 kpl', 'Sun machine dishwasher capsule', 1.50),                           #  23
    ('jogurtti, banaani, Valio, 1 l', 'jogurtti, banaani, Valio, 1 l', 'yoghurt, banana, Valio', 2.09),                                   #  24
    ('jogurtti, mansikka Valio, 1 l', 'jogurtti, mansikka Valio, 1 l', 'yoghurt, strawberry, Valio', 2.09),                               #  25
    ('tikkuperunoita', 'tikkuperunoita', 'potato sticks', 1.19),                                                                          #  26
    ('lihapyörykkä, HK', 'lihapyörykkä, HK', 'meat balls, HK', 1.29),                                                                     #  27
    ('nakkeja, Atria', 'nakkeja, Atria', 'sausages, Atria', 1.95),                                                                        #  28
    ('wok-kasvismix, 1kg', 'wok-kasvismix, 1kg', 'wok vegetable mix, 1kg', 2.59),                                                         #  29
    ('Lipton Yellow Label tee, 50 ps', 'Lipton Yellow Label tee, 50 ps', 'Lipton Yellow Label tea, 50 pcs', 2.15),                        #  30
    ('hammasharja, lasten', 'hammasharja, lasten', 'toothbrush, for kids', 1.00),                                                         #  31
    ('hammasharja, aikuisten', 'hammasharja, aikuisten', 'toothbrush, for adults', 2.00),                                                 #  32
    ('ananas, tuore', 'ananas, tuore', 'ananas, fresh', 1.92),                                                                            #  33
    ('suklaanappirulla, Marabou', 'suklaanappirulla, Marabou', 'chocolate buttons, Marabou', 1.50),                                       #  34
    ('ylikypsä kinkkuleike, 250g, Atria', 'ylikypsä kinkkuleike, 250g, Atria', 'mellow ham slices, 250g, Atria', 3.05),                   #  35
    ('keittokinkkuleike, 250g, Atria', 'keittokinkkuleike, 250g, Atria', 'ham slices, 250g, Atria', 3.15),                                #  36
    ('Daimrulla, Marabou', 'Daimrulla, Marabou', 'Daim chocolate buttons, Marabou', 1.59),                                                #  37
    ('sipuli, 1kg', 'sipuli, 1kg', 'onion, 1kg', 1.19),                                                                                   #  38
    ('Lauantaipussi, 150g, Malaco', 'Lauantaipussi, 150g, Malaco', 'Saturday bag candy, 150g, Malaco', 1.64),                             #  39
    ('Caesar-salaatti, Pirkka', 'Caesar-salaatti, Pirkka', 'Caesar salad bag, Pirkka', 2.99),                                             #  40
    ('ruisleipä, Ruiskiekko, Putaan Pulla', 'ruisleipä, Ruiskiekko, Putaan Pulla', 'rye bread, Ruiskiekko, Putaan Pulla', 1.70),          #  41
    ('Italian pata -pussi, Blå Band', 'Italian pata -pussi, Blå Band', 'Italian stew bag, Blå Band', 2.29),                               #  42
    ('tex mex -pata -pussi, Blå Band', 'tex mex -pata -pussi, Blå Band', 'tex mex stew bag, Blå Band', 2.15),                             #  43
    ('appelsiinijuomatiiviste, 1.5l, Pirkka', 'appelsiinijuomatiiviste, 1.5l, Pirkka', 'orange juice concentrate, 1.5l, Pirkka', 2.29),   #  44
    ('jäätelö, herkkutrio, Pingviini', 'jäätelö, herkkutrio, Pingviini', 'ice cream, triple taste, Pingviini', 2.85),                     #  45
    ('jäätelö, nougat, Pingviini', 'jäätelö, nougat, Pingviini', 'ice cream, nougat, Pingviini', 2.85),                                   #  46
    ('saaristolaisleike, Kalavalmis', 'saaristolaisleike, Kalavalmis', 'islanders cold cut, Kalavalmis', 3.49),                           #  47
    ('kirjolohisuikale, 300g, Pirkka', 'kirjolohisuikale, 300g, Pirkka', 'rainbow strout slices, 300g, Pirkka', 4.29),                    #  48
    ('ylikypsä kinkkuleike, 300g, Snellman', 'ylikypsä kinkkuleike, 300g, Snellman', 'mellow ham slices, 300g, Snellman', 3.89),          #  49
    ('muffinsi, kaakao, Pirkka', 'muffinsi, kaakao, Pirkka', 'muffin, cocoa, Pirkka', 2.39),                                              #  50
    ('muffinsi, sitruuna, Pirkka', 'muffinsi, sitruuna, Pirkka', 'muffin, lemon, Pirkka', 2.39),                                          #  51
    ('jahtimakkara, 250g, Atria', 'jahtimakkara, 250g, Atria', 'hunters sausage, 250g, Atria', 2.29),                                     #  52
    ('tomaatti, 1kg, Suomi', 'tomaatti, 1kg, Suomi', 'tomato, 1kg, Finland', 4.00),                                                       #  53
    ('ruisleipä, Oululainen Reissumies', 'ruisleipä, Oululainen Reissumies', 'rye bread, Oululainen Reissumies', 1.50),                   #  54
    ('limsa, Hartwall Jaffa 1.5l, keltainen', 'limsa, Hartwall Jaffa 1.5l, keltainen', 'lemonade, Hartwall Jaffa 1.5l, yellow', 1.50),    #  55
    ('limsa, Hartwall Jaffa 1.5l, punainen', 'limsa, Hartwall Jaffa 1.5l, punainen', 'lemonade, Hartwall Jaffa 1.5l, red', 1.50),         #  56
    ('limsa, Coca-Cola 1.5l', 'limsa, Coca-Cola 1.5l', 'lemonade, Coca-Cola 1.5l', 1.50),                                                 #  57
    ('siideri, mansikka, Kopparberg', 'siideri, mansikka, Kopparberg', 'cider, strawberry, Kopparberg', 2.95),                            #  58
    ('juustosnacks, 275g, Taffel', 'juustosnacks, 275g, Taffel', 'cheese snacks, 275g, Taffel', 2.75),                                    #  59
    ('jogurtti, banaani, 8x125g, Valio', 'jogurtti, banaani, 8x125g, Valio', 'yoghurt, banana, 8x125g, Valio', 3.19),                     #  60
    ('jogurtti, mansikka, 8x125g, Valio', 'jogurtti, mansikka, 8x125g, Valio', 'yoghurt, strawberry, 8x125g, Valio', 3.19),               #  61
    ('jogurtti, hedelmäpommi, 8x125g, Valio', 'jogurtti, hedelmäpommi, 8x125g, Valio', 'yoghurt, fruit bomb, 8x125g, Valio', 3.19),       #  62
    ('jogurtti, banaani, 200g, Valio', 'jogurtti, banaani, 200g, Valio', 'yoghurt, banana, 200g, Valio', 0.47),                           #  63
    ('jogurtti, mansikka, 200g, Valio', 'jogurtti, mansikka, 200g, Valio', 'yoghurt, strawberry, 200g, Valio', 0.47),                     #  64
    ('jogurtti, hedelmäpommi, 200g, Valio', 'jogurtti, hedelmäpommi, 200g, Valio', 'yoghurt, fruit bomb, 200g, Valio', 0.47),             #  65
    ('karkki, eucalyptus, Fazer', 'karkki, eucalyptus, Fazer', 'candies, eucalyptus, Fazer', 2.89),                                       #  66
    ('tortillapohja, 8kpl/360g, Pirkka', 'tortillapohja, 8kpl/360g, Pirkka', 'tortilla base, 8pcs/360g ', 1.52),                          #  67
    ('broilerin paistisuikale, Pirkka', 'broilerin paistisuikale, Pirkka', 'broiler meat slices', 1.50),                                  #  68
    ('olut, tumma lager, 0.5l, Pirkka', 'olut, tumma lager, 0.5l, Pirkka', 'beer, dark lager, 0.5l, Pirkka', 1.79),                       #  69
    ('olut, vaalea lager, 0.33l, Pirkka', 'olut, vaalea lager, 0.33l, Pirkka', 'beer, light lager, 0.33l, Pirkka', 0.98),                 #  70
    ('juusto, emmental 400g, Pirkka', 'juusto, emmental 400g, Pirkka', 'cheese, emmental 400g, Pirkka', 3.69),                            #  71
    ('jääsalaatti, Pirkka', 'jääsalaatti, Pirkka', 'ice salad, Pirkka', 1.19),                                                            #  72
    ('tomaattimurska, 390g, Pirkka', 'tomaattimurska, 390g, Pirkka', 'crushed tomato, 390g, Pirkka', 1.50),                               #  73
    ('meetvursti, valkosipuli, Atria', 'meetvursti, valkosipuli, Atria', 'metwurst sausage, garlic, Atria', 3.49),                        #  74
    ('salsadippi, keskivahva, 315g, Pirkka', 'salsadippi, keskivahva, 315g, Pirkka', 'salsa dip, medium, 315g', 1.71),                    #  75
    ('sinihomejuusto, 175g, Pirkka', 'sinihomejuusto, 175g, Pirkka', 'blue cheese, 175g, Pirkka', 2.25),                                  #  76
    ('valkohomejuusto, 175g, Pirkka', 'valkohomejuusto, 175g, Pirkka', 'white cheese, 175g, Pirkka', 2.25),                               #  77
    ('sinihomejuusto, Aura', 'sinihomejuusto, Aura', 'blue cheese, Aura', 3.50),                                                          #  78
    ('tuorekurkku, 1kg, Suomi', 'tuorekurkku, 1kg, Suomi', 'cucumber, 1kg, Finland', 3.50),                                               #  79
    ('kalkkunaleike, 250g, Atria', 'kalkkunaleike, 250g, Atria', 'turkey cold cut, 250g, Atria ', 2.45),                                  #  80
    ('kananmuna, 15kpl', 'kananmuna, 15kpl', 'eggs, 15pcs', 2.37),                                                                        #  81
    ('kanan koipipalat, 1kg', 'kanan koipipalat, 1kg', 'chicken leg pieces, 1kg', 3.45),                                                  #  82
    ('WC-paperi', 'WC-paperi', 'toilet paper', 1.50),                                                                                     #  83
    ('talouspaperi', 'talouspaperi', 'paper towel', 2.05),                                                                                #  84
    ('suihkusaippua, Bergamot', 'suihkusaippua, Bergamot', 'shower gel, Bergamot', 2.20),                                                 #  85
    ('suihkusaippua, Sport', 'suihkusaippua, Sport', 'shower gel, Sport', 2.45),                                                          #  86
    ('näkkileipä, Kunto', 'näkkileipä, Kunto', 'crispbread, Kunto', 2.69)                                                                 #  87
    ]


languages = [
    'Finnish',
    'English'
    ]


stores = [
    'K-Citymarket Raksila',
    'Prisma Raksila',
    'Siwa Muhos',
    'K-Supermarket Mimmi',
    'S-Market Koskiseutu',
    'K-Citymarket Kaakkuri',
    'Limingantullin Prisma'
    ]

shoppinglists = [
    ['Ensimmäinen testilista', [[1, 3], [2, 3], [4, 1], [7, 1]]],
    ['The second testlist', [[2, 2], [9, 1], [13, 1], [5, 1], [4, 2], [7, 1]]],
    ['My list', [[1, 3], [2, 2], [13, 2], [5, 1], [4, 2], [7, 1], [10, 2], [11, 2]]],
    ['longlist', [[1, 3], [2, 3], [81, 1], [82, 1], [61, 1], [84, 1], [85, 1], [86, 1], [87, 1], [6, 1], [19, 1], [41, 2], [80, 2], [7, 2], [40, 1], [28, 2]]]
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

    def test_14_b_find_shopping_list_by_hash(self):
        #for a_list in self.db.find_shopping_list_by_hash([hashlib.md5(shoppinglists[0][0].encode('utf-8')).hexdigest(), 1, 1]):
        #    pass
        #    #print(a_list)

        # Example for sorting 'None' sorted items as the last, leaving them 
        # behind the sorted items.
        
        non_sorted = []
        for an_item in self.db.find_shopping_list_by_hash([hashlib.md5(shoppinglists[3][0].encode('utf-8')).hexdigest(), 1, 1]):
            #pass
            if an_item[6]:
                print(an_item)
            else:
                non_sorted.append(an_item)

        for a_non_sorted in non_sorted:
            print(a_non_sorted)

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

    def test_22_mark_items_bought_by_list_hash(self):
        # <Shopping list hash>, <item id>, <bought> (bought = 1, not bought = 0)
        # buy
        self.db.mark_item_bought_for_shoppinglist_hash([hashlib.md5(shoppinglists[0][0].encode('utf-8')).hexdigest(), 1, 1])
        self.db.mark_item_bought_for_shoppinglist_hash([hashlib.md5(shoppinglists[0][0].encode('utf-8')).hexdigest(), 2, 1])

        # cancel buying
        self.db.mark_item_bought_for_shoppinglist_hash([hashlib.md5(shoppinglists[0][0].encode('utf-8')).hexdigest(), 1, 0])
        self.db.mark_item_bought_for_shoppinglist_hash([hashlib.md5(shoppinglists[0][0].encode('utf-8')).hexdigest(), 2, 0])


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


