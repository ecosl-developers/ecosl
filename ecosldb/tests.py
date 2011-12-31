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
import os.path
import argparse
import ecosldb


if __name__ == '__main__':
    """"Main function."""

    # Main parser
    print('NOTE:  not updated yet!!!!')

    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--database', nargs=1, metavar='<path/file.db>', required=True, help='The path to the database')
    
    subparsers = ap.add_subparsers(title='Subcommands')

    # Subparser for creating the database
    create_parser = subparsers.add_parser('create', help='subcommand to create a new database or dump the contents to a file.');
    create_parser.add_argument('-e', '--empty', action='store_true', help='Create a new, empty database.')
    create_parser.add_argument('-f', '--file', nargs=1, metavar='<path/file.sql>', dest='inputfile', help='Create a new database and import contents from <path/file.sql>.')
    create_parser.add_argument('-d', '--dump', nargs=1, metavar='<path/file.sql>', dest='dumpfile', help='Create a dump of database contents to <path/file.sql>.')

    # Subparser for adding items
    add_parser = subparsers.add_parser('add', help='subcommands to add items to tables');
    add_parser.add_argument('--item', nargs=2, metavar=('"<name>"', '<list id>'), help='Add new item <name>. <list id> is either a shopping list id or 0, which means the item available for all lists.')
    add_parser.add_argument('--lang', nargs=1, metavar='"<language>"', help='Add new language for item translations.')
    add_parser.add_argument('--tr', nargs=3, metavar=('<item id>', '<language id>', '"<translation>"'), dest='translation', help='Add new translation for an item <item id> to language <language id>. Translated string is "<translation>".')

    # Subparser for listing table items
    list_parser = subparsers.add_parser('list', help='subcommands to list database items');
    list_parser.add_argument('--items', help='List all available items and their translations.')

    args = ap.parse_args()

    print(args) #  debug

    db = EcoDB(args.database[0])


    # Arguments are parsed, do the required tasks.

    # create new, empty database
    if hasattr(args, 'empty'):
        if args.empty:
            db.create_empty_database();

    # dump contents of the database
    if hasattr(args, 'dumpfile'):
        if args.dumpfile:
            db.dump_database(args.dumpfile);

    # create and input contents of the database according to an sql file
    if hasattr(args, 'inputfile'):
        if args.inputfile:
            db.import_database(args.inputfile);

    # add new item
    if hasattr(args, 'item'):
        if args.item:
            db.add_item(args.item)
            #print('new item: %u %s %u' % (index[0], index[1], index[2]))

    # add new translation language
    if hasattr(args, 'lang'):
        if args.lang:
            db.add_language(args.lang)

    # add new translation for an item
    if hasattr(args, 'translation'):
        if args.translation:
            db.add_translation(args.translation)



