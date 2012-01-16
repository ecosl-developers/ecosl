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


# The prototype for backend and protocol, the mod_python version

# http://www.modpython.org/live/current/doc-html/contents.html

# start from: https://projects.sse.fi/ecotest/ecoslbe2.py/menu


import sys
from mod_python import apache
sys.path.append('/home/mtapoja/code/github/ecosl/ecosldb')
from ecosldb import EcoDB
from xml.dom.minidom import Document

db = EcoDB('/home/mtapoja/code/github/ecosl/ecosldb/unittest.db')
scriptpath = 'https://projects.sse.fi/ecotest/ecoslbe2.py/'

def ecomenu(req):
    req.content_type = 'text/html'

    req.write('<html>')
    req.write('<head><title>Ecological Shopping List II - this is going to be it!</title></head>')
    req.write('<body>')
    req.write('<h2><a href="' + scriptpath + '"handler>Ecological Shopping List II - protocol prototype 2</a></h2>')

    req.write('<ul>')

    # language menu
    # https://projects.sse.fi/ecotest/ecoslbe2.py/languages?outputtype=html
    req.write('<li>list all item languages: <a href="' + scriptpath + 'languages?outputtype=html">html</a>, \
        <a href="' + scriptpath + 'languages?outputtype=text">text</a>, \
        <a href="' + scriptpath + 'languages?outputtype=xml">xml</a>')


    # store menu
    req.write('<li>list all stores: <a href="' + scriptpath + 'stores?outputtype=html">html</a>, \
        <a href="' + scriptpath + 'stores?outputtype=text">text</a>, \
        <a href="' + scriptpath + 'stores?outputtype=xml">xml</a>')


    # item menus
    req.write('<li>list all items: <a href="' + scriptpath + 'allitems?lang=0&outputtype=html">html</a>, \
        <a href="' + scriptpath + 'allitems?lang=0&outputtype=text">text</a>, \
        <a href="' + scriptpath + 'allitems?lang=0&outputtype=xml">xml</a>')
    req.write('<ul>')
    for a_lang in db.find_languages(['']):
        req.write('<li>' + str(a_lang[1]) + ': \
            <a href="' + scriptpath + 'allitems?lang=' + str(a_lang[0]) + '&outputtype=html"> \
            html</a>,  \
            <a href="' + scriptpath + 'allitems?lang=' + str(a_lang[0]) + '&outputtype=text"> \
            text</a>, \
            <a href="' + scriptpath + 'allitems?lang=' + str(a_lang[0]) + '&outputtype=xml"> \
            xml</a>')
    req.write('</ul>')
    req.write('<li>single items:')
    req.write('<ul>')
    req.write('<li>item 1, language 1: \
        <a href="' + scriptpath + 'singleitem?itemid=1&lang=1&outputtype=html">html</a>, \
        <a href="' + scriptpath + 'singleitem?itemid=1&lang=1&outputtype=text">text</a>, \
        <a href="' + scriptpath + 'singleitem?itemid=1&lang=1&outputtype=xml">xml</a>')
    req.write('<li>item 80, language 2: \
        <a href="' + scriptpath + 'singleitem?itemid=80&lang=2&outputtype=html">html</a>, \
        <a href="' + scriptpath + 'singleitem?itemid=80&lang=1&outputtype=text">text</a>, \
        <a href="' + scriptpath + 'singleitem?itemid=80&lang=1&outputtype=xml">xml</a>')
    req.write('</ul>')

    # shopping lists (NOTE: this will not be a normal function, shopping lists will not be listed)
    req.write('<li>shopping lists:')
    req.write('<ul>')


    req.write('<li>list 1, language 1, store 1: \
        <a href="' + scriptpath + 'shoppinglist?slid=1&lang=1&storeid=1&outputtype=html">html</a>, \
        <a href="' + scriptpath + 'shoppinglist?slid=1&lang=1&storeid=1&outputtype=text">text</a>, \
        <a href="' + scriptpath + 'shoppinglist?slid=1&lang=1&storeid=1&outputtype=xml">xml</a>')
    req.write('<li>list 4, language 2, store 1: \
        <a href="' + scriptpath + 'shoppinglist?slid=4&lang=2&storeid=1&outputtype=html">html</a>, \
        <a href="' + scriptpath + 'shoppinglist?slid=4&lang=2&storeid=1&outputtype=text">text</a>, \
        <a href="' + scriptpath + 'shoppinglist?slid=4&lang=2&storeid=1&outputtype=xml">xml</a>')
    req.write('</ul>')
    req.write('</ul>')

    req.write('</body>')
    req.write('</html>')

def menu(req):
    # https://projects.sse.fi/ecotest/ecoslbe2.py/menu
    ecomenu(req)

def languages(req, outputtype):
    languages = db.find_languages([''])
    print_data(req, 'languages', languages, outputtype)
    #if outputtype != '':
    #    print_data(req, 'languages', languages, outputtype)
    #else:
    #    print_data(req, 'languages', languages, '')

def stores(req, outputtype):
    all_stores = db.find_store([''])
    print_data(req, 'stores', all_stores, outputtype)

def allitems(req, lang, outputtype):
    items = db.find_all_items([int(lang)])
    print_data(req, 'items', items, outputtype)

def singleitem(req, itemid, lang, outputtype):
    items = db.find_item_id([int(itemid), int(lang)])
    print_data(req, 'items', items, outputtype)

def shoppinglist(req, slid, lang, storeid, outputtype):
    the_lists = db.find_shopping_list_by_id([int(slid), int(lang), int(storeid)])
    print_data(req, 'shoppinglist', the_lists, outputtype)


def print_data(req, what, data, how):

    if how == 'html':
        req.content_type = "text/html"
        if what == 'items':
            for an_item in data:
                if an_item[3] == None:
                    req.write('%s;%s;"%s";\n' % 
                        (an_item[0], 
                        an_item[1],
                        an_item[2].encode('utf-8')))
                else:
                    req.write('%s;%s;"%s";%s;%s;"%s";\n' % 
                        (an_item[0], 
                        an_item[1],
                        an_item[2].encode('utf-8'),
                        an_item[3],
                        #an_item[4],
                        an_item[5],
                        an_item[6].encode('utf-8')))

        elif what == 'languages':
            for a_lang in data:
                req.write('%s;%s;\n' % (str(a_lang[0]), a_lang[1]))

        elif what == 'stores':
            for a_store in data:
                req.write('%s;%s;\n' % (str(a_store[0]), a_store[1]))

        elif what == 'shoppinglist':
            for a_list in data:
                req.write('%s;%s;%s;%s;%s;%s;\n' % (
                    a_list[0],                               #  0:   item.id
                    a_list[1].encode('utf-8'),               #  1:   item.name
                    a_list[2],                               #  2:   shoppinglistitems.amount
                    a_list[3],                               #  3:   shoppinglistitems.bought
                    a_list[4].encode('utf-8'),               #  4:   itemtranslation.translation
                    str(a_list[5]),                          #  5:   price.price
                    ))


    elif how == 'text':
        req.content_type = "text/plain"

        if what == 'items':
            for an_item in data:
                if an_item[3] == None:
                    req.write('%s;%s;%s;\n' % 
                        (an_item[0], 
                        an_item[1],
                        #bytes(an_item[2], encoding='utf-8'))) 
                        an_item[2].encode('utf-8')))
                        #str(an_item[2].encode('utf-8'))))
                        #str(an_item[2], encoding = 'ascii'))) ei toimi
                else:
                    req.write('%s;%s;"%s";%s;%s;"%s";\n' % 
                        (an_item[0], 
                        an_item[1],
                        an_item[2].encode('utf-8'),
                        an_item[3],
                        #an_item[4],
                        an_item[5],
                        an_item[6].encode('utf-8')))

        elif what == 'languages':
            for a_lang in data:
                req.write('%s;%s;\n' % (str(a_lang[0]), a_lang[1]))

        elif what == 'stores':
            for a_store in data:
                req.write('%s;%s;\n' % (str(a_store[0]), a_store[1]))


        elif what == 'shoppinglist':
            for a_list in data:
                req.write('%s;%s;%s;%s;%s;%s;\n' % (
                    a_list[0],                               #  0:   item.id
                    a_list[1].encode('utf-8'),               #  1:   item.name
                    a_list[2],                               #  2:   shoppinglistitems.amount
                    a_list[3],                               #  3:   shoppinglistitems.bought
                    a_list[4].encode('utf-8'),               #  4:   itemtranslation.translation
                    str(a_list[5]),                          #  5:   price.price
                    ))


    elif how == 'xml':
        req.content_type = "text/xml"

        if what == 'items':

            doc = Document()
            item_table = doc.createElement('item_table')
            doc.appendChild(item_table)

            for an_item in data:
                if an_item[3] == None:

                    items = doc.createElement('item')
                    items.setAttribute('languageid', '0')
                    item_table.appendChild(items)

                    item_id = doc.createElement('id')
                    items.appendChild(item_id)
                    idtext = doc.createTextNode(str(an_item[0]))
                    item_id.appendChild(idtext)

                    item_shoppinglistid = doc.createElement('shoppinglistid')
                    items.appendChild(item_shoppinglistid)
                    item_shoppinglistidtext = doc.createTextNode(str(an_item[1]))
                    item_shoppinglistid.appendChild(item_shoppinglistidtext)

                    item_name = doc.createElement('name')
                    items.appendChild(item_name)
                    item_nametext = doc.createTextNode(str(an_item[2].encode('utf-8')))
                    item_name.appendChild(item_nametext)

                else:
                    items = doc.createElement('item')
                    items.setAttribute('languageid', str(an_item[5]))
                    item_table.appendChild(items)

                    item_id = doc.createElement('id')
                    items.appendChild(item_id)
                    idtext = doc.createTextNode(str(an_item[0]))
                    item_id.appendChild(idtext)

                    item_shoppinglistid = doc.createElement('shoppinglistid')
                    items.appendChild(item_shoppinglistid)
                    item_shoppinglistidtext = doc.createTextNode(str(an_item[1]))
                    item_shoppinglistid.appendChild(item_shoppinglistidtext)

                    item_name = doc.createElement('name')
                    items.appendChild(item_name)
                    item_nametext = doc.createTextNode(str(an_item[2].encode('utf-8')))
                    item_name.appendChild(item_nametext)

                    item_itemtranslationid = doc.createElement('itemtranslationid')
                    items.appendChild(item_itemtranslationid)
                    item_itemtranslationidtext = doc.createTextNode(str(an_item[3]))
                    item_itemtranslationid.appendChild(item_itemtranslationidtext)

                    item_translation = doc.createElement('translation')
                    items.appendChild(item_translation)
                    item_translationtext = doc.createTextNode(str(an_item[6].encode('utf-8')))
                    item_translation.appendChild(item_translationtext)

            req.write(doc.toprettyxml(indent="  "))

        elif what == 'languages':

            doc = Document()
            itemlanguage_table = doc.createElement('itemlanguage_table')
            doc.appendChild(itemlanguage_table)

            for a_lang in data:
                itemlanguages = doc.createElement('itemlanguage')
                itemlanguage_table.appendChild(itemlanguages)

                itemlanguage_id = doc.createElement('id')
                itemlanguages.appendChild(itemlanguage_id)
                idtext = doc.createTextNode(str(a_lang[0]))
                itemlanguage_id.appendChild(idtext)

                itemlanguage_language = doc.createElement('language')
                itemlanguages.appendChild(itemlanguage_language)
                languagetext = doc.createTextNode(str(a_lang[1]))
                itemlanguages.appendChild(languagetext)

            req.write(doc.toprettyxml(indent="  ") + '\n')

        elif what == 'stores':

            doc = Document()
            store_table = doc.createElement('store_table')
            doc.appendChild(store_table)

            for a_store in data:
                stores = doc.createElement('store')
                store_table.appendChild(stores)

                store_id = doc.createElement('id')
                stores.appendChild(store_id)
                idtext = doc.createTextNode(str(a_store[0]))
                store_id.appendChild(idtext)

                store_name = doc.createElement('name')
                stores.appendChild(store_name)
                nametext = doc.createTextNode(a_store[1])
                stores.appendChild(nametext)

            req.write(doc.toprettyxml(indent="  ") + '\n')

        elif what == 'shoppinglist':

            doc = None

            for a_list in data:
                #print('%s;%s;%s;%s;%s;%s;' % (
                #    a_list[0],                               #  0:   item.id
                #    a_list[1].encode('utf-8'),               #  1:   item.name
                #    a_list[2],                               #  2:   shoppinglistitems.amount
                #    a_list[3],                               #  3:   shoppinglistitems.bought
                #    a_list[4].encode('utf-8'),               #  4:   itemtranslation.translation
                #    str(a_list[5]),                          #  5:   price.price
                #    ))

                if not doc:
                    doc = Document()
                    the_list = doc.createElement('shoppinglist')
                    #the_list.setAttribute('languageid', str(a_list[7]))
                    #the_list.setAttribute('shoppinglistid', str(a_list[1]))
                    doc.appendChild(the_list)

                items = doc.createElement('item')
                the_list.appendChild(items)

                item_id = doc.createElement('id')
                items.appendChild(item_id)
                idtext = doc.createTextNode(str(a_list[0]))
                item_id.appendChild(idtext)

                item_name = doc.createElement('name')
                items.appendChild(item_name)
                item_nametext = doc.createTextNode(str(a_list[1].encode('utf-8')))
                item_name.appendChild(item_nametext)

                item_amount = doc.createElement('amount')
                items.appendChild(item_amount)
                item_amounttext = doc.createTextNode(str(a_list[2]))
                item_amount.appendChild(item_amounttext)

                item_bought = doc.createElement('bought')
                items.appendChild(item_bought)
                item_boughttext = doc.createTextNode(str(a_list[3]))
                item_bought.appendChild(item_boughttext)

                item_translation = doc.createElement('translation')
                items.appendChild(item_translation)
                item_translationtext = doc.createTextNode(str(a_list[4].encode('utf-8')))
                item_translation.appendChild(item_translationtext)

                item_price = doc.createElement('price')
                items.appendChild(item_price)
                item_pricetext = doc.createTextNode(str(a_list[5]))
                item_price.appendChild(item_pricetext)

            req.write(doc.toprettyxml(indent="  ") + '\n')

