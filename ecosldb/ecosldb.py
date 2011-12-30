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

# http://benspaulding.com/weblog/2008/jun/13/brief-python-sqlite-example/
# http://docs.python.org/library/sqlite3.html
# http://docs.python.org/library/argparse.html


import sys
import os.path
import argparse
import sqlite3


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

    def create(self):
        """Create new database."""
        if self.connection:
            print('Database already open! Please choose another file name.')
        else:
            sql=['CREATE TABLE item (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, shoppinglistid INTEGER);',
                'CREATE UNIQUE INDEX itidname ON item (id, shoppinglistid);',
                'CREATE TABLE itemlanguage (id INTEGER PRIMARY KEY AUTOINCREMENT, language TEXT);',
                'CREATE UNIQUE INDEX idlanguage ON itemlanguage (id, language ASC);',
                'CREATE TABLE itemtranslation (id INTEGER PRIMARY KEY AUTOINCREMENT, itemlanguageid INTEGER, translation TEXT);',
                'CREATE UNIQUE INDEX iditemlanguageid ON itemtranslation (id, itemlanguageid ASC);',
                'CREATE TABLE shoppinglist (id INTEGER PRIMARY KEY AUTOINCREMENT, hash TEXT);',
                'CREATE UNIQUE INDEX idhash ON shoppinglist (id, hash ASC);',
                'CREATE TABLE shoppinglistitems (id INTEGER PRIMARY KEY AUTOINCREMENT, shoppinglistid INTEGER, itemid INTEGER, amount INTEGER);',
                'CREATE UNIQUE INDEX idshoppinglistid ON shoppinglistitems (id, shoppinglistid ASC);',
                'CREATE TABLE store (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);',
                'CREATE UNIQUE INDEX stidname ON store (id, name ASC);',
                'CREATE TABLE price (id INTEGER PRIMARY KEY AUTOINCREMENT, itemid INTEGER, storeid INTEGER, price REAL);',
                'CREATE UNIQUE INDEX pridstoreid ON price (id, storeid ASC);',
                'CREATE TABLE shoppingorder (id INTEGER PRIMARY KEY AUTOINCREMENT, storeid INTEGER, itemid INTEGER, shorder INTEGER);',
                'CREATE UNIQUE INDEX soidstoreid ON shoppingorder (id, storeid ASC);',
                ]

            #print('Creating new database.') #  debug

            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()

            for sql_clause in sql:
                self.cursor.execute(sql_clause)
                self.connection.commit()

            #self.cursor.close()


    def get_all_items(self):
        """"Get all available items"""
        return self.cursor.execute('select itemid, itemname from items')

    def get_list_items(self, a_list):
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

    def update_item(self, itemid, itemname):
        """Update the name of an item"""
        self.cursor.execute('update items set itemname = "%s" where itemid = "%s"' % (itemname, itemid))
        self.connection.commit()

    def remove_item(self, item):
        """"Remove an item completely"""
        r = self.cursor.execute('delete from items where itemname = "%s"' % item)
        self.connection.commit()

    def add_language(self, language):
        """"Add new language for item translations."""
        if self.connection:
            self.cursor.execute('insert into itemlanguage (language) values ("%s")' % language[0])
            self.connection.commit()
    #
    # Adding, modifying and removing shopping lists

    def add_shoppinglist(self, slist):
        """"Add a new shoppinglist"""
        t = (slist, )
        self.cursor.execute('insert into lists (listhash) values (?)', t)
        self.connection.commit()
        r = self.cursor.execute('select listid, listhash from lists where listhash = "%s"' % slist).fetchall()[0]
        return r

    def update_shoppinglist(self, slistid, slisthash):
        self.cursor.execute('update lists set listhash = "%s" where listid = "%s"' % (slisthash, slistid))
        self.connection.commit()

    def addtolist(self, listhash, itemind, amount):
        """"Add a given amount of items to shopping list"""
        # get list id
        listid = self.cursor.execute('select listid, listhash from lists where listhash = "%s"' % listhash).fetchall()[0]
        t = (listid[0], itemind, amount)
        self.cursor.execute('insert into listitems (listid, itemid, amount) values (?, ?, ?)', t)
        self.connection.commit()
        r = self.cursor.execute('select listitemsid, listid, itemid, amount from listitems where listid="%s" and itemid = "%s"' % (listid[0], itemind)).fetchall()[0]
        return r

    def removefromlist(self, listhash, itemind):
        """"Remove an item from a shopping list"""
        # get list id
        listid = self.cursor.execute('select listid from lists where listhash = "%s"' % listhash).fetchall()[0]
        print('removing itemind, listid: %s, %s' % (itemind, listid[0]))
        r = self.cursor.execute('delete from listitems where (itemid = "%s" and listid = "%s")' % (itemind, listid[0]))
        self.connection.commit()

    def add_store(self, item):
        """"Add new stores"""
        t = (item, )
        self.cursor.execute('insert into store (storename) values (?)', t)
        self.connection.commit()
        r = self.cursor.execute('select storeid, storename from store where storename = "%s"' % item).fetchall()[0]
        return r

    def update_store(self, storeid, storename):
        self.cursor.execute('update store set storename = "%s" where storeid = "%s"' % (storename, storeid))
        self.connection.commit()

    def get_all_stores(self):
        """"Get all stores"""
        return self.cursor.execute('select storeid, storename from store')

    def get_all_shoppinglists(self):
        """"Get all shoppinglists"""
        return self.cursor.execute('select listid, listhash from lists')

    def add_price(self, itemid, storeid, price):
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

    def list_items_in_order(self, storeind):
        """"List items in correct order for one store"""
        # Currently only thing that connects an item and a store is shoppingorder
        # table.
        r = self.cursor.execute('select shoppingorder.sorder, shoppingorder.storeid, shoppingorder.itemid, store.storeid, store.storename, items.itemid, items.itemname from shoppingorder, store, items where (store.storeid = %s and items.itemid = shoppingorder.itemid and shoppingorder.storeid = store.storeid) order by shoppingorder.sorder' % storeind).fetchall()
        return r

    def list_items_not_in_store(self, storeind):
        """"List items that do not exist in store"""
        r = self.cursor.execute('select items.itemid, items.itemname from items where items.itemid not in (select shoppingorder.itemid from shoppingorder, store where store.storeid = "%s" and store.storeid = shoppingorder.storeid) order by items.itemname' % storeind).fetchall()
        return r




def helptext():
    '''DEPRECATED! Remember to remove'''
    print('Known parameters:\n\
    help, --help                         FIX THIS    this help\n\
    list                                 FIX THIS    list contents of all tables\n\
    list [items, stores, lists]          FIX THIS    list contents of one table\n\
    showlist "list"                      FIX THIS    show items and amounts for a shopping list\n\
    additem "new item"                   FIX THIS    add new item\n\
    updateitem itemid "new itemname"     FIX THIS    update itemname\n\
    addtolist "list name" itemind amount FIX THIS    add new item and amount to shopping list\n\
    addstore "new store"                 FIX THIS    add new store\n\
    updatestore storeid "new storename"  FIX THIS    update storename\n\
    addlist "new list"                   FIX THIS    add new shopping list\n\
    updatelist listid "list name"        FIX THIS    update shopping list\n\
    rmitems "item" ["item2" "itemN"...]  FIX THIS    remove item\n\
    addprice itemid storeid price        NOT IMPLE   add or update price to an item to a store\n\
    rmprice itemid storeid               NOT IMPLE   remove price of an item from a store\n\
    getprice itemid storeid              NOT IMPLE   get price of an item from a store\n\
    getprices listid storeid             NOT IMPLE   get prices for a list for a store\n\
    order storeind                       FIX THIS    list all items in order for the store\n\
    notin storeind                       FIX THIS    list all items that are not in the store')

def shorthelptext():
    '''DEPRECATED! Remember to remove'''
    print('Ecological Shopping List II database functions:\n\
usage: ' + sys.argv[0] + ' [ -h | --help | <function> [parameters]]\n\n\
Note: this library does not work yet!')


if __name__ == '__main__':
    """"Main function, to be used for creating the database, developing and testing."""

    ap = argparse.ArgumentParser(epilog='Note: this library does not work yet!')
    ap.add_argument('-d', '--database', nargs=1, metavar='<path/file.db>', required=True, help='The path to the database')
    ap.add_argument('-a', '--add', nargs=2, metavar='"<name>" <list id>', help='Add new item <name>. <list id> is either a shopping list id or 0, which means the item available for all lists.')
    ap.add_argument('-c', '--create', action='store_true', help='Create a new database.')
    ap.add_argument('-l', '--lang', nargs=1, metavar='<language>', help='Add new language.')
    args = ap.parse_args()

    print(args) #  debug

    db = EcoDB(args.database[0])

    # Arguments are parsed, do the required tasks.

    if args.create:
        db.create();

    if args.add:
        db.add_item(args.add)
        #print('new item: %u %s %u' % (index[0], index[1], index[2]))

    if args.lang:
        db.add_language(args.lang)

    sys.exit(0)


    if True:
        #print sys.argv[1]
        #print 'parameter count: %g' % (len(sys.argv) - 1)
        if (sys.argv[1] == '-h') or (sys.argv[1] == '--help') or (sys.argv[1] == 'help'):
            helptext()

        # only one parameter, sys.argv length = 2
        elif len(sys.argv) == 2:

            if sys.argv[1] == 'list':
                index = 1
                #print '\nall items:\n------------------------------------------------------------'
                for an_item in db.get_all_items():
                    #print u'{0:3}:  {1:4}   {2}'.format(index, an_item[0], an_item[1])
                    #print u'%u:  %u   %s' % (index, an_item[0], an_item[1])
                    index = index + 1

                #print '\nall stores:\n------------------------------------------------------------'
                index = 1
                for a_store in db.get_all_stores():
                    #print u'{0:3}:  {1:4}   {2}'.format(index, a_store[0], a_store[1])
                    #print u'%u:  %u   %s' % (index, a_store[0], a_store[1])
                    index = index + 1

                index = 1
                #print '\nall lists:\n------------------------------------------------------------'
                for a_list in db.get_all_shoppinglists():
                    #print u'{0:3}:  {1:4}   {2}'.format(index, a_list[0], a_list[1])
                    #print u'%u:  %u   %s' % (index, a_list[0], a_list[1])
                    index = index + 1

            else:
                print('Unknown parameter')

        elif sys.argv[1] == 'list':
            if sys.argv[2] == 'items':
                index = 1
                for an_item in db.get_all_items():
                    #print u'{0:3}:  {1:4}   {2}'.format(index, an_item[0], an_item[1])
                    #print u'%u:  %u   %s' % (index, an_item[0], an_item[1])
                    index = index + 1

            elif sys.argv[2] == 'stores':
                index = 1
                for a_store in db.get_all_stores():
                    #print u'{0:3}:  {1:4}   {2}'.format(index, a_store[0], a_store[1])
                    #print u'%u:  %u   %s' % (index, a_store[0], a_store[1])
                    index = index + 1

            elif sys.argv[2] == 'lists':
                index = 1
                for a_list in db.get_all_shoppinglists():
                    #print u'{0:3}:  {1:15}   {2}'.format(index, a_list[0], a_list[1])
                    #print u'%u:  %u   %s' % (index, a_list[0], a_list[1])
                    index = index + 1


        elif sys.argv[1] == 'showlist':
            index = 1
            #print u'ind    id   amount  item'
            #print u'------------------------------------------------'
            for an_item in db.get_list_items(sys.argv[2]):
                # itemid, amount, itemname
                #    0       1       2
                #print u'{0:3}: {1:4} {2:4}      {3:25}'.format(index, an_item[0], an_item[1], an_item[2])
                #print u'%u: %u %u      %s' % (index, an_item[0], an_item[1], an_item[2])
                index = index + 1

        elif sys.argv[1] == 'updateitem':
            #print u'update item: %s %s' % (sys.argv[2], sys.argv[3])
            db.update_item(sys.argv[2], sys.argv[3])

        elif sys.argv[1] == 'addtolist':
            #print 'add ' + sys.argv[4] + ' pcs of ' + sys.argv[3] + ' to list ' + sys.argv[2]
            added_item = db.addtolist(sys.argv[2], sys.argv[3], sys.argv[4])
            #print added_item
            #print u'listitemsid: %u  listid: %s  itemid: %u  amount: %u' % (added_item[0], added_item[1], added_item[2], added_item[3])

        elif sys.argv[1] == 'addstore':
            index = db.add_store(sys.argv[2])
            #print u'new store: {0} {1}'.format(index[0], index[1])
            #print u'new store: %u %s' % (index[0], index[1])

        elif sys.argv[1] == 'updatestore':
            #print u'update store: %s %s' % (sys.argv[2], sys.argv[3])
            db.update_store(sys.argv[2], sys.argv[3])

        elif sys.argv[1] == 'addlist':
            index = db.add_shoppinglist(sys.argv[2])
            #print u'new shoppinglist: {0} {1}'.format(index[0], index[1])
            #print u'new shoppinglist: %u %s' % (index[0], index[1])

        elif sys.argv[1] == 'updatelist':
            db.update_shoppinglist(sys.argv[2], sys.argv[3])

        elif sys.argv[1] == 'rmitems':
            for ind in range (2, len(sys.argv)):
                db.remove_item(sys.argv[ind])

        elif sys.argv[1] == 'addprice':
            r = db.add_price(sys.argv[2], sys.argv[3], sys.argv[4]) 

        elif sys.argv[1] == 'rmprice':
            print('rmprice: not yet implemented')

        elif sys.argv[1] == 'getprice':
            print('getprice: not yet implemented')

        elif sys.argv[1] == 'getprices':
            print('getprices: not yet implemented')

        elif sys.argv[1] == 'order':
            index = 1
            #print u'ind  order  item                       store'
            #print u'----------------------------------------------------------'
            for an_item in db.list_items_in_order(sys.argv[2]):
                # sorder, storeid, itemid, storeid, storename, itemid, itemname
                #    0       1       2       3         4         5         6
                #print u'{0:3}: {1:4}   {2:25}  {3}'.format(index, an_item[0], an_item[6], an_item[4])
                #print u'%u: %u   %s  %s' % (index, an_item[0], an_item[6], an_item[4])
                index = index + 1

        elif sys.argv[1] == 'notin':
            index = 1
            #print u'ind    id  item'
            #print u'-------------------------------------------'
            for an_item in db.list_items_not_in_store(sys.argv[2]):
                #print u'{0:3}: {1:4}   {2:25}'.format(index, an_item[0], an_item[1])
                #print u'%u: %u   %s' % (index, an_item[0], an_item[1])
                index = index + 1



