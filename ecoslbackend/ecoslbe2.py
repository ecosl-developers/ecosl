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

db = EcoDB('/home/mtapoja/code/github/ecosl/ecosldb/unittest.db')
scriptpath = 'https://projects.sse.fi/ecotest/ecoslbe2.py/'

def ecomenu(req):
    req.content_type = 'text/html'

    req.write('<html>')
    req.write('<head><title>Ecological Shopping List II - this is going to be it!</title></head>')
    req.write('<body>')
    req.write('<h2><a href="' + scriptpath + '"handler>Ecological Shopping List II - protocol prototype 1</a></h2>')

    req.write('<ul>')

    # language menu
    req.write('<li><a href="' + scriptpath + '?listaction=languages">list all item languages</a> (<a href="' + scriptpath + '?listaction=languages&type=text">text</a>, <a href="' + scriptpath + '?listaction=languages&type=xml">xml</a>)')


    # store menu
    req.write('<li><a href="' + scriptpath + '?listaction=stores">list all stores</a> (<a href="' + scriptpath + '?listaction=stores&type=text">text</a>, <a href="' + scriptpath + '?listaction=stores&type=xml">xml</a>)')


    # item menus
    req.write('<li><a href="' + scriptpath + '?listaction=allitems">list all items</a> (')
    req.write('<a href="' + scriptpath + '?listaction=allitems&type=text">text</a>, <a href="' + scriptpath + '?listaction=allitems&type=xml">xml</a>)')
    req.write('<ul>')
    for a_lang in db.find_languages(['']):
        req.write('<li><a href="' + scriptpath + '?listaction=allitems&lang=' + str(a_lang[0]) + '">' + a_lang[1] + '</a> (')
        req.write('<a href="' + scriptpath + '?listaction=allitems&lang=' + str(a_lang[0]) + '&type=text">text</a>, <a href="' + scriptpath + '?listaction=allitems&lang=' + str(a_lang[0]) + '&type=xml">xml</a>)')
    req.write('</ul>')
    req.write('<li>single items:')
    req.write('<ul>')
    req.write('<li>item 1, language 1: <a href="' + scriptpath + '?listaction=item&itemid=1&languageid=1">html</a>, ')
    req.write('<a href="' + scriptpath + '?listaction=item&itemid=1&languageid=1&type=text">text</a>, ')
    req.write('<a href="' + scriptpath + '?listaction=item&itemid=1&languageid=1&type=xml">xml</a>')
    req.write('<li>item 80, language 2: <a href="' + scriptpath + '?listaction=item&itemid=80&languageid=2">html</a>, ')
    req.write('<a href="' + scriptpath + '?listaction=item&itemid=80&languageid=1&type=text">text</a>, ')
    req.write('<a href="' + scriptpath + '?listaction=item&itemid=80&languageid=1&type=xml">xml</a>')
    req.write('</ul>')

    # shopping lists (NOTE: this will not be a normal function, shopping lists will not be listed)
    req.write('<li>shopping lists:')
    req.write('<ul>')


    req.write('<li>list 1, language 1, store 1: <a href="' + scriptpath + '?listaction=shoppinglist&shoppinglistid=1&languageid=1&storeid=1">html</a>, ')
    req.write('<a href="' + scriptpath + '?listaction=shoppinglist&shoppinglistid=1&languageid=1&storeid=1&type=text">text</a>, ')
    req.write('<a href="' + scriptpath + '?listaction=shoppinglist&shoppinglistid=1&languageid=1&storeid=1&type=xml">xml</a>')
    req.write('<li>list 4, language 2, store 1: <a href="' + scriptpath + '?listaction=shoppinglist&shoppinglistid=4&languageid=2&storeid=1">html</a>, ')
    req.write('<a href="' + scriptpath + '?listaction=shoppinglist&shoppinglistid=4&languageid=2&storeid=1&type=text">text</a>, ')
    req.write('<a href="' + scriptpath + '?listaction=shoppinglist&shoppinglistid=4&languageid=2&storeid=1&type=xml">xml</a>')
    req.write('</ul>')
    req.write('</ul>')

    req.write('</body>')
    req.write('</html>')

def menu(req):
    ecomenu(req)

def languages(req, outputtype):
    languages = db.find_languages([''])
    if outputtype != '':
        print_data(req, 'languages', languages, outputtype)
    else:
        print_data(req, 'languages', languages, '')



def print_data(req, what, data, how):
    if how == 'html':
        req.content_type = "text/html"
        if what == 'items':
            pass
        elif what == 'languages':
            for a_lang in data:
                req.write('%s;%s;' % (str(a_lang[0]), a_lang[1]))

    elif how == 'text':
        req.content_type = "text/plain"
        pass


    elif how == 'xml':
        req.content_type = "text/xml"
        pass

