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
import hashlib


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
                CREATE TABLE item (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, shoppinglistid INTEGER NOT NULL); \
                CREATE UNIQUE INDEX itidname ON item (id, shoppinglistid); \
                CREATE TABLE itemlanguage (id INTEGER PRIMARY KEY AUTOINCREMENT, language TEXT NOT NULL UNIQUE); \
                CREATE UNIQUE INDEX idlanguage ON itemlanguage (id, language ASC); \
                CREATE TABLE itemtranslation (id INTEGER PRIMARY KEY AUTOINCREMENT, itemid INTEGER NOT NULL, itemlanguageid INTEGER NOT NULL, translation TEXT NOT NULL); \
                CREATE UNIQUE INDEX iditemlanguageid ON itemtranslation (id, itemlanguageid ASC); \
                CREATE TABLE shoppinglist (id INTEGER PRIMARY KEY AUTOINCREMENT, hash TEXT NOT NULL UNIQUE); \
                CREATE UNIQUE INDEX idhash ON shoppinglist (id, hash ASC); \
                CREATE TABLE shoppinglistitems (id INTEGER PRIMARY KEY AUTOINCREMENT, shoppinglistid INTEGER NOT NULL, itemid INTEGER NOT NULL, amount INTEGER NOT NULL, bought INTEGER); \
                CREATE UNIQUE INDEX idshoppinglistid ON shoppinglistitems (id, shoppinglistid ASC); \
                CREATE TABLE store (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE); \
                CREATE UNIQUE INDEX stidname ON store (id, name ASC); \
                CREATE TABLE price (id INTEGER PRIMARY KEY AUTOINCREMENT, itemid INTEGER NOT NULL, storeid INTEGER NOT NULL, price REAL NOT NULL); \
                CREATE UNIQUE INDEX pridstoreid ON price (id, storeid ASC); \
                CREATE TABLE shoppingorder (id INTEGER PRIMARY KEY AUTOINCREMENT, storeid INTEGER NOT NULL, itemid INTEGER NOT NULL, shorder INTEGER NOT NULL); \
                CREATE UNIQUE INDEX soidstoreid ON shoppingorder (id, storeid ASC); \
                CREATE UNIQUE INDEX soidstoreiditemid ON shoppingorder (id, storeid, itemid ASC); \
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

    def find_store(self, name):
        """"Find stores by their name."""
        if name[0] == "":
            return self.cursor.execute('select id, name from store')
        else:
            return self.cursor.execute('select id, name from store \
                where store.name = "%s"' % name[0])

    def find_languages(self, lang):
        """Find languages and their ids by the name."""
        if lang[0] == "":
            return self.cursor.execute('select * from itemlanguage')
        else:
            return self.cursor.execute('select * from itemlanguage \
                where language= "%s"' % lang[0])



    def get_list_items(self, a_list):  # NOT UPDATED FOR ECOSL II
        """"Get all items for a single shopping list"""
        return self.cursor.execute('select items.itemid, listitems.amount, items.itemname from items, listitems, lists where lists.listhash = "%s" and listitems.listid = lists.listid and listitems.itemid = items.itemid' % a_list)

    #
    # Adding, modifying and removing items to database

    def add_item(self, item):
        """"Add new item."""
        if self.connection:
            t = (item[0], item[1], )
            self.cursor.execute('insert into item (name, shoppinglistid) values (?, ?)', t)
            self.connection.commit()

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
            t = (language[0], )
            self.cursor.execute('insert into itemlanguage (language) values (?)', t)
            self.connection.commit()

    def add_translationid(self, trid):
        """Add new translation by item id for an item."""
        if self.connection:
            t = (trid[0], trid[1], trid[2], )
            self.cursor.execute('insert into itemtranslation (itemid, itemlanguageid, translation) values (?, ?, ?)', t)
            self.connection.commit()

    def add_translationname(self, trname):
        """Add new translation by item name for an item."""
        if self.connection:
            for item in self.find_item_name([trname[0], '0']):
                t = (item[0], trname[1], trname[2], )
                self.cursor.execute('insert into itemtranslation (itemid, itemlanguageid, translation) values (?, ?, ?)', t)
            self.connection.commit()

    def add_store(self, store):
        """"Add new store"""
        if self.connection:
            t = (store[0], )
            self.cursor.execute('insert into store (name) values (?)', t)
            self.connection.commit()

    def add_shoppinglist(self, slist):
        """"Add a new shopping list"""
        t = (hashlib.md5(slist[0].encode('utf-8')).hexdigest(), )
        self.cursor.execute('insert into shoppinglist (hash) values (?)', t)
        self.connection.commit()

    def add_price(self, price):
        """"Add a price to an item for a store"""
        r = self.cursor.execute('select id, itemid, storeid, price from price where (itemid = %s and storeid = %s)' % (price[0], price[1])).fetchall()

        # Check if price for this item in this store exists: if it does, update, if not, insert.
        if r == []:
            t = (price[0], price[1], price[2], )
            self.cursor.execute('insert into price (itemid, storeid, price) values (?, ?, ?)', t)
            self.connection.commit()
        else:
            if r[0][3] != float(price[2]):
                t = (price[2], price[0], price[1], )
                self.cursor.execute('update price set price = ? where (itemid = ? and storeid = ?)', t)
                self.connection.commit()

    def add_to_list(self, listname, itemlist):
        """"Add a given amount of items to shopping list"""
        # itemlist is a nested list so that we can easily add several items to a shopping list at once.
        
        # get list id
        t = (hashlib.md5(listname.encode('utf-8')).hexdigest(), )
        listid = self.cursor.execute('select id, hash from shoppinglist where hash = ?', t).fetchall()
        if listid != []:
            for item in itemlist:
                t = (listid[0][0], item[0], item[1], )
                self.cursor.execute('insert into shoppinglistitems (shoppinglistid, itemid, amount, bought) values (?, ?, ?, 0)', t) 
                self.connection.commit()
        else:
            print('the list does not exist.')


    def add_shoppingorder(self, order):
        """Set a shopping order for an item to a store, and move existing items, if needed."""
        for a_store in self.find_store(order):

            # move existing items lower in shopping order
            t = (int(order[2]), )
            self.cursor.execute('update shoppingorder set shorder = (shorder + 1) where shorder >= ?', t)
            self.connection.commit()

            # check if the item exists. if it does, update it, otherwise insert new item
            t = (a_store[0], int(order[1]), )
            items = self.cursor.execute('select id, storeid, itemid, shorder \
                    from shoppingorder \
                    where storeid = ? and itemid = ?', t)
            for an_item in items:
                #print(an_item)  # debug
                #print('items found, updating...')  # debug
                t = (int(order[2]), int(an_item[0]), )
                self.cursor.execute('update shoppingorder set shorder = ? where id = ?', t)
                self.connection.commit()
                break
            else:
                #print('items not found, inserting....')  # debug
                t = (a_store[0], int(order[1]), int(order[2]), )
                self.cursor.execute('insert into shoppingorder (storeid, itemid, shorder) values (?, ?, ?)', t)
                self.connection.commit()

            break
        #else:
        #    print('no stores found')


    #
    # Adding, modifying and removing shopping lists

    def update_shoppinglist(self, slistid, slisthash):  # NOT UPDATED FOR ECOSL II
        self.cursor.execute('update lists set listhash = "%s" where listid = "%s"' % (slisthash, slistid))
        self.connection.commit()

    def removefromlist(self, listhash, itemind):  # NOT UPDATED FOR ECOSL II
        """"Remove an item from a shopping list"""
        # get list id
        listid = self.cursor.execute('select listid from lists where listhash = "%s"' % listhash).fetchall()[0]
        print('removing itemind, listid: %s, %s' % (itemind, listid[0]))
        r = self.cursor.execute('delete from listitems where (itemid = "%s" and listid = "%s")' % (itemind, listid[0]))
        self.connection.commit()

    def update_store(self, storeid, storename):  # NOT UPDATED FOR ECOSL II
        self.cursor.execute('update store set storename = "%s" where storeid = "%s"' % (storename, storeid))
        self.connection.commit()

    def find_shopping_list_by_name(self, name):
        """Find shopping list id by it's hash (generated from it's name)."""
        if name[0] != "":
            t = (hashlib.md5(name[0].encode('utf-8')).hexdigest(), )
            return self.cursor.execute('select id, hash from shoppinglist \
                where hash = ?', t).fetchone()
        else:
            return None
            

    def find_shopping_list(self, sl):
        """"Find a shopping list: items, translations and shopping order for the given store."""

        # Check the language. If it's not set, use 1 as default.
        if sl[2] != "":
            #print('language: ', sl[2])
            for a_language in self.find_languages([sl[2]]):
                #print(a_language)
                pass
        else:
            #print('no language')
            a_language = (1, )

        # Check shopping list name, that is needed.
        if sl[0] != "":
            a_list = self.find_shopping_list_by_name([sl[0]])
            #print(a_list)

            if sl[1] != "":
                #print('store name: ', sl[1])
                for a_store in self.find_store([sl[1]]):
                    #print(a_store)
                    pass

                # get list id
                # t = (<shopping list id>, <language id>, <store id>, )
                t = (a_list[0], a_language[0], a_store[0], )
                the_list = self.cursor.execute('select shoppinglistitems.id, shoppinglistitems.shoppinglistid, shoppinglistitems.itemid, \
                    shoppinglistitems.amount, shoppinglistitems.bought, item.id, item.name, \
                    itemlanguage.id, itemlanguage.language, itemtranslation.id, itemtranslation.itemid, \
                    itemtranslation.translation, shoppingorder.id, shoppingorder.storeid, \
                    shoppingorder.itemid, shoppingorder.shorder \
                    from shoppinglistitems, item, itemlanguage, itemtranslation, shoppingorder \
                    where shoppinglistitems.shoppinglistid = ? \
                    and shoppinglistitems.itemid = item.id \
                    and itemlanguage.id = ? \
                    and itemtranslation.itemid = item.id \
                    and itemtranslation.itemlanguageid = itemlanguage.id \
                    and shoppingorder.storeid = ? \
                    and shoppingorder.itemid = item.id \
                    order by shoppingorder.shorder', t)
            else:
                #print('no store name')

                # get list id
                # t = (<shopping list id>, <language id>, )
                t = (a_list[0], a_language[0], )
                the_list = self.cursor.execute('select shoppinglistitems.id, shoppinglistitems.shoppinglistid, shoppinglistitems.itemid, \
                    shoppinglistitems.amount, shoppinglistitems.bought, item.id, item.name, \
                    itemlanguage.id, itemlanguage.language, itemtranslation.id, itemtranslation.itemid, \
                    itemtranslation.translation \
                    from shoppinglistitems, item, itemlanguage, itemtranslation \
                    where shoppinglistitems.shoppinglistid = ? \
                    and shoppinglistitems.itemid = item.id \
                    and itemlanguage.id = ? \
                    and itemtranslation.itemid = item.id \
                    and itemtranslation.itemlanguageid = itemlanguage.id', t)
        else:
            the_list = None

        return the_list


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
    add_parser.add_argument('--shoppinglist', nargs=1, metavar='"<shopping list name>"', help='Add new shopping list <shopping list name>.')
    add_parser.add_argument('--price', nargs=3, metavar=('<item id>', '<store id>', '<price>'), help='Add a price for <item id>, to <store id>, amount of <price> (e.g. 1.25).')
    add_parser.add_argument('--itemtolist', nargs=3, metavar=('"<shopping list name>"', '<item id>', '<amount>'), help='Add <amount> items (<item id>), to <shopping list name>.')
    add_parser.add_argument('--order', nargs=3, metavar=('"<store name>"', '<item id>', '<order>'), help='Add and modify shopping orders (<order>) for <item id> in <store name>.')

    # Subparser for finding and listing table items
    list_parser = subparsers.add_parser('list', help='subcommands for finding and listing database items');
    list_parser.add_argument('--allitems', nargs=1, metavar='<language id>', help='List all available items and their translations for the given language.')
    list_parser.add_argument('--itemname', nargs=2, metavar=('"<item name>"', '<language id>'), help='Find items and their translations by their name for the given language.')
    list_parser.add_argument('--itemid', nargs=2, metavar=('<item id>', '<language id>'), help='Find items and their translations by their ids.')
    list_parser.add_argument('--store', nargs=1, metavar='"<store name>"', dest='findstore', help='Find "<store name>" and the id. If "<store name>" is empty, list all stores.')
    list_parser.add_argument('--lang', nargs=1, metavar='"<language>"', dest='findlang', help='Find "<language>" and the id.')
    list_parser.add_argument('--shoppinglist', nargs=3, metavar=('"<shopping list name>"', '"<store name>"', '"<language>"'), dest='findlist', help='Find "<shopping list name>" for "<store name>" and it\'s items translated to "<language>", ordered in shopping order. If "<store name>" is omitted, the items are not ordered, and if "<language>" is omitted, the default names for items are displayed.')

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
            db.add_translationid(args.translationid)

    # add new translation for an item name
    if hasattr(args, 'translationname'):
        if args.translationname:
            db.add_translationname(args.translationname)
            
    # add new store
    if hasattr(args, 'store'):
        if args.store:
            db.add_store(args.store)

    # add new shopping list
    if hasattr(args, 'shoppinglist'):
        if args.shoppinglist:
            db.add_shoppinglist(args.shoppinglist)

    # add new or update existing price for an item to a store
    if hasattr(args, 'price'):
        if args.price:
            db.add_price(args.price)

    # add items to shopping list
    if hasattr(args, 'itemtolist'):
        if args.itemtolist:
            listname = args.itemtolist[0]
            itemlist = [[args.itemtolist[1], args.itemtolist[2]]]
            db.add_to_list(listname, itemlist)

    # add shopping orders for items in store
    if hasattr(args, 'order'):
        if args.order:
            db.add_shoppingorder(args.order)

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


    # find a store and id for it
    if hasattr(args, 'findstore'):
        if args.findstore:
            for a_store in db.find_store(args.findstore):
                print(a_store)


    # find a language and id for it
    if hasattr(args, 'findlang'):
        if args.findlang:
            for a_language in db.find_languages(args.findlang):
                print(a_language)

    # find a shopping list with all the details
    if hasattr(args, 'findlist'):
        if args.findlist:
            for a_list in db.find_shopping_list(args.findlist):
                print(a_list)


