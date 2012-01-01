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
import argparse
from ecosldb import EcoDB
import unittest


class EcoDBTestSequence(unittest.TestCase):

    self.dbfile='./unittest.db'

    def setUp(self):
        print('creating a test database')
        self.db = EcoDB(dbfile)
        self.db.create_empty_database();

    def tearDown(self):
        print('removing used database DISABLED')
        #os.remove(dbfile)

    def test_add_items(self):
        print('adding items to database')
        self.db.add_item({'maito,sin', 0})

if __name__ == '__main__':
    """"Main function."""

    # Main parser

    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--items', action='store_true', help='test for adding and modifying items.')
    
    #create_parser = subparsers.add_parser('create', help='subcommand to create a new database or dump the contents to a file.');
    #create_parser.add_argument('-e', '--empty', action='store_true', help='Create a new, empty database.')
    #create_parser.add_argument('-f', '--file', nargs=1, metavar='<path/file.sql>', dest='inputfile', help='Create a new database and import contents from <path/file.sql>.')
    #create_parser.add_argument('-d', '--dump', nargs=1, metavar='<path/file.sql>', dest='dumpfile', help='Create a dump of database contents to <path/file.sql>.')
    #add_parser.add_argument('--item', nargs=2, metavar=('"<name>"', '<list id>'), help='Add new item <name>. <list id> is either a shopping list id or 0, which means the item available for all lists.')
    #add_parser.add_argument('--lang', nargs=1, metavar='"<language>"', help='Add new language for item translations.')
    #add_parser.add_argument('--tr', nargs=3, metavar=('<item id>', '<language id>', '"<translation>"'), dest='translation', help='Add new translation for an item <item id> to language <language id>. Translated string is "<translation>".')


    args = ap.parse_args()

    print(args) #  debug



    # Arguments are parsed, do the required tasks.

    # item tests
    if hasattr(args, 'items'):
        print('testing items')
        unittest.main()



