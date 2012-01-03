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

# http://benspaulding.com/weblog/2008/jun/13/brief-python-sqlite-example/
# http://docs.python.org/library/sqlite3.html
# http://docs.python.org/library/argparse.html


import sys
import os.path
import argparse
import sqlite3
import codecs


class EcoDB:
    """Database abstraction class for Ecological Shopping List II.
       All database related functions are implemented as an API.
    """


    def __init__(self, db_path):
        """Open ecosl database, if it exists."""
        self.connection = False;
        self.db_path = db_path
        if os.path.exists(self.db_path) and os.path.isfile(self.db_path):
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            #print('db opened') #  debug
        else:
            print('db does not exist') #  debug

    def create_empty_database(self):
        """Create a new, empty database."""
        if self.connection:
            print('Database already open! Please choose another file name.')
        else:
            sql='BEGIN TRANSACTION; \
                CREATE TABLE item (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, shoppinglistid INTEGER); \
                CREATE UNIQUE INDEX itidname ON item (id, shoppinglistid); \
                CREATE TABLE itemlanguage (id INTEGER PRIMARY KEY AUTOINCREMENT, language TEXT); \
                CREATE UNIQUE INDEX idlanguage ON itemlanguage (id, language ASC); \
                CREATE TABLE itemtranslation (id INTEGER PRIMARY KEY AUTOINCREMENT, itemid INTEGER, itemlanguageid INTEGER, translation TEXT); \
                CREATE UNIQUE INDEX iditemlanguageid ON itemtranslation (id, itemlanguageid ASC); \
                CREATE TABLE shoppinglist (id INTEGER PRIMARY KEY AUTOINCREMENT, hash TEXT); \
                CREATE UNIQUE INDEX idhash ON shoppinglist (id, hash ASC); \
                CREATE TABLE shoppinglistitems (id INTEGER PRIMARY KEY AUTOINCREMENT, shoppinglistid INTEGER, itemid INTEGER, amount INTEGER); \
                CREATE UNIQUE INDEX idshoppinglistid ON shoppinglistitems (id, shoppinglistid ASC); \
                CREATE TABLE store (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT); \
                CREATE UNIQUE INDEX stidname ON store (id, name ASC); \
                CREATE TABLE price (id INTEGER PRIMARY KEY AUTOINCREMENT, itemid INTEGER, storeid INTEGER, price REAL); \
                CREATE UNIQUE INDEX pridstoreid ON price (id, storeid ASC); \
                CREATE TABLE shoppingorder (id INTEGER PRIMARY KEY AUTOINCREMENT, storeid INTEGER, itemid INTEGER, shorder INTEGER); \
                CREATE UNIQUE INDEX soidstoreid ON shoppingorder (id, storeid ASC); \
                COMMIT;'

            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            self.cursor.executescript(sql)



    def import_database(self, sqlfile):
        """Create new database and import contents of an sql file to it."""
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        if self.connection:
            f = codecs.open(sqlfile[0], encoding='utf-8', mode='r')
            sql = f.read()
            self.cursor.executescript(sql)
            print('db created and contents imported from %s' % sqlfile[0])

    def dump_database(self, sqlfile):
        """Dump contents of the database to a file."""
        if self.connection:
            with codecs.open(sqlfile[0], encoding='utf-8', mode='w') as f:
                for line in self.connection.iterdump():
                    f.write('%s\n' % line)
            print('db dumped to %s' % sqlfile[0])

    def find_all_items(self, langid):
        """"Find all items and their translations for the given language."""
        if langid[0] == '0': # all items without the translations
            return self.cursor.execute('select * from item')
        else:
            return self.cursor.execute('select item.id, item.shoppinglistid, item.name, \
                itemtranslation.id, itemtranslation.itemid, itemtranslation.itemlanguageid, \
                itemtranslation.translation \
                from item \
                left join itemtranslation \
                on itemtranslation.itemlanguageid = "%s" and itemtranslation.itemid = item.id' % langid[0])

    def find_item_name(self, nameid):
        """"Find items and translations by their name for the given language."""
        if nameid[1] == '0':
            return self.cursor.execute('select * from item \
                where item.name = "%s"' % nameid[0])
        else:
            return self.cursor.execute('select item.id, item.name, item.shoppinglistid, \
                itemtranslation.id, itemtranslation.itemid, itemtranslation.itemlanguageid, \
                itemtranslation.translation \
                from item, itemtranslation \
                where item.name = "%s" and itemtranslation.itemlanguageid = "%s" and itemtranslation.itemid = item.id' % (nameid[0], nameid[1]))

    def find_item_id(self, idid):
        """"Find items and translations by their id for the given language."""
        return self.cursor.execute('select item.id, item.shoppinglistid, item.name, \
            itemtranslation.id, itemtranslation.itemid, itemtranslation.itemlanguageid, \
            itemtranslation.translation \
            from item, itemtranslation \
            where item.id = "%s" and itemtranslation.itemlanguageid = "%s" and itemtranslation.itemid = item.id' % (idid[0], idid[1]))

    def get_list_items(self, a_list):  # NOT UPDATED FOR ECOSL II
        """"Get all items for a single shopping list"""
        return self.cursor.execute('select items.itemid, listitems.amount, items.itemname from items, listitems, lists where lists.listhash = "%s" and listitems.listid = lists.listid and listitems.itemid = items.itemid' % a_list)

    #
    # Adding, modifying and removing items to database

    def add_item(self, item):
        """"Add new item."""
        if self.connection:
            self.cursor.execute('insert into item (name, shoppinglistid) values ("%s", "%s")' % (item[0], item[1]))
            self.connection.commit()
            #r = self.cursor.execute('select id, name, shoppinglistid from item where name = "%s"' % item[0]).fetchall()[0]

    def update_item(self, itemid, itemname):  # NOT UPDATED FOR ECOSL II
        """Update the name of an item"""
        self.cursor.execute('update items set itemname = "%s" where itemid = "%s"' % (itemname, itemid))
        self.connection.commit()

    def remove_item(self, item):  # NOT UPDATED FOR ECOSL II
        """"Remove an item completely"""
        r = self.cursor.execute('delete from items where itemname = "%s"' % item)
        self.connection.commit()

    def add_language(self, language):
        """"Add new language for item translations."""
        if self.connection:
            self.cursor.execute('insert into itemlanguage (language) values ("%s")' % language[0])
            self.connection.commit()

    def add_translation(self, trid):
        """Add new translation by item id for an item."""
        if self.connection:
            self.cursor.execute('insert into itemtranslation (itemid, itemlanguageid, translation) values ("%s", "%s", "%s")' % (trid[0], trid[1], trid[2]))
            self.connection.commit()

    def add_translationname(self, trname):
        """Add new translation by item name for an item."""
        if self.connection:
            for item in self.find_item_name([trname[0], '0']):
                self.cursor.execute('insert into itemtranslation (itemid, itemlanguageid, translation) values ("%s", "%s", "%s")' % (item[0], trname[1], trname[2]))
            self.connection.commit()


    #
    # Adding, modifying and removing shopping lists

    def add_shoppinglist(self, slist):  # NOT UPDATED FOR ECOSL II
        """"Add a new shoppinglist"""
        t = (slist, )
        self.cursor.execute('insert into lists (listhash) values (?)', t)
        self.connection.commit()
        r = self.cursor.execute('select listid, listhash from lists where listhash = "%s"' % slist).fetchall()[0]
        return r

    def update_shoppinglist(self, slistid, slisthash):  # NOT UPDATED FOR ECOSL II
        self.cursor.execute('update lists set listhash = "%s" where listid = "%s"' % (slisthash, slistid))
        self.connection.commit()

    def addtolist(self, listhash, itemind, amount):  # NOT UPDATED FOR ECOSL II
        """"Add a given amount of items to shopping list"""
        # get list id
        listid = self.cursor.execute('select listid, listhash from lists where listhash = "%s"' % listhash).fetchall()[0]
        t = (listid[0], itemind, amount)
        self.cursor.execute('insert into listitems (listid, itemid, amount) values (?, ?, ?)', t)
        self.connection.commit()
        r = self.cursor.execute('select listitemsid, listid, itemid, amount from listitems where listid="%s" and itemid = "%s"' % (listid[0], itemind)).fetchall()[0]
        return r

    def removefromlist(self, listhash, itemind):  # NOT UPDATED FOR ECOSL II
        """"Remove an item from a shopping list"""
        # get list id
        listid = self.cursor.execute('select listid from lists where listhash = "%s"' % listhash).fetchall()[0]
        print('removing itemind, listid: %s, %s' % (itemind, listid[0]))
        r = self.cursor.execute('delete from listitems where (itemid = "%s" and listid = "%s")' % (itemind, listid[0]))
        self.connection.commit()

    def add_store(self, store):
        """"Add new store"""
        t = (store[0], )
        self.cursor.execute('insert into store (name) values (?)', t)
        self.connection.commit()

    def update_store(self, storeid, storename):  # NOT UPDATED FOR ECOSL II
        self.cursor.execute('update store set storename = "%s" where storeid = "%s"' % (storename, storeid))
        self.connection.commit()

    def get_all_stores(self):  # NOT UPDATED FOR ECOSL II
        """"Get all stores"""
        return self.cursor.execute('select storeid, storename from store')

    def get_all_shoppinglists(self):  # NOT UPDATED FOR ECOSL II
        """"Get all shoppinglists"""
        return self.cursor.execute('select listid, listhash from lists')

    def add_price(self, itemid, storeid, price):  # NOT UPDATED FOR ECOSL II
        """"Add a price to an item for a store"""
        r = self.cursor.execute('select priceid, itemid, storeid, price from itemprices where (itemid = %s and storeid = %s)' % (itemid, storeid)).fetchall()
        #print r

        # Check if price for this item in this store exists: if it does, update, if not, insert.
        if r == []:
            #print 'price not found, inserting...'
            t = (itemid, storeid, price)
            self.cursor.execute('insert into itemprices (itemid, storeid, price) values (?, ?, ?)', t)
            self.connection.commit()
            #r = self.cursor.execute('select priceid, itemid, storeid, price from itemprices where (itemid = %s and storeid = %s)' % (itemid, storeid)).fetchall()
            #print 'new values:'
            #print r
        else:
            #print 'old (%s) and new (%s) price differ, updating...' % (fetchedprice, price)
            self.cursor.execute('update itemprices set price = "%s" where (itemid = "%s" and storeid = "%s")' % (price, itemid, storeid))
            self.connection.commit()
        #return r

    def list_items_in_order(self, storeind):  # NOT UPDATED FOR ECOSL II
        """"List items in correct order for one store"""
        # Currently only thing that connects an item and a store is shoppingorder
        # table.
        r = self.cursor.execute('select shoppingorder.sorder, shoppingorder.storeid, shoppingorder.itemid, store.storeid, store.storename, items.itemid, items.itemname from shoppingorder, store, items where (store.storeid = %s and items.itemid = shoppingorder.itemid and shoppingorder.storeid = store.storeid) order by shoppingorder.sorder' % storeind).fetchall()
        return r

    def list_items_not_in_store(self, storeind):  # NOT UPDATED FOR ECOSL II
        """"List items that do not exist in store"""
        r = self.cursor.execute('select items.itemid, items.itemname from items where items.itemid not in (select shoppingorder.itemid from shoppingorder, store where store.storeid = "%s" and store.storeid = shoppingorder.storeid) order by items.itemname' % storeind).fetchall()
        return r




#
# main function
#

if __name__ == '__main__':
    """"Main function, to be used for creating the database, developing and testing."""

    # Main parser
    ap = argparse.ArgumentParser(epilog='Note: this library does not work yet!')
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
    add_parser.add_argument('--trid', nargs=3, metavar=('<item id>', '<language id>', '"<translation>"'), dest='translationid', help='Add new translation for an item <item id> to language <language id>. Translated string is "<translation>".')
    add_parser.add_argument('--trname', nargs=3, metavar=('"<item name>"', '<language id>', '"<translation>"'), dest='translationname', help='Add new translation for an item "<item name>" to language <language id>. Translated string is "<translation>".')
    add_parser.add_argument('--store', nargs=1, metavar='"<store name>"', help='Add new store <store name>.')

    # Subparser for finding and listing table items
    list_parser = subparsers.add_parser('list', help='subcommands for finding and listing database items');
    list_parser.add_argument('--allitems', nargs=1, metavar='<language id>', help='List all available items and their translations for the given language.')
    list_parser.add_argument('--itemname', nargs=2, metavar=('"<item name>"', '<language id>'), help='Find items and their translations by their name for the given language.')
    list_parser.add_argument('--itemid', nargs=2, metavar=('<item id>', '<language id>'), help='Find items and their translations by their ids.')

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

    # add new translation for an item id
    if hasattr(args, 'translationid'):
        if args.translationid:
            db.add_translation(args.translationid)

    # add new translation for an item name
    if hasattr(args, 'translationname'):
        if args.translationname:
            db.add_translationname(args.translationname)
            
    # add new store
    if hasattr(args, 'store'):
        if args.store:
            db.add_store(args.store)

    # list all items and their translations for the given language
    if hasattr(args, 'allitems'):
        if args.allitems:
            for an_item in db.find_all_items(args.allitems):
                print(an_item)

    # list items and their translations by their name for the given language
    if hasattr(args, 'itemname'):
        if args.itemname:
            for an_item in db.find_item_name(args.itemname):
                print(an_item)

    # list items and their translations by their id for the given language
    if hasattr(args, 'itemid'):
        if args.itemid:
            for an_item in db.find_item_id(args.itemid):
                print(an_item)


