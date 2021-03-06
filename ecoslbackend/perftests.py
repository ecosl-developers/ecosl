#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# httplib2 does not work in Python 3 for https://, therefore python and not python3
#

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
import unittest
import random
import httplib2


#
# Responses for the queries

content_languages_html_text = '1;Finnish;\n2;English;\n'

content_languages_xml = '<?xml version="1.0" ?>\n<itemlanguage_table>\n  <itemlanguage>\n    <id>\n      1\n    </id>\n    <language/>\n    Finnish\n  </itemlanguage>\n  <itemlanguage>\n    <id>\n      2\n    </id>\n    <language/>\n    English\n  </itemlanguage>\n</itemlanguage_table>\n\n'

content_stores_html_text = '1;K-Citymarket Raksila;\n2;Prisma Raksila;\n3;Siwa Muhos;\n4;K-Supermarket Mimmi;\n5;S-Market Koskiseutu;\n6;K-Citymarket Kaakkuri;\n7;Limingantullin Prisma;\n'

content_stores_xml = '<?xml version="1.0" ?>\n<store_table>\n  <store>\n    <id>\n      1\n    </id>\n    <name/>\n    K-Citymarket Raksila\n  </store>\n  <store>\n    <id>\n      2\n    </id>\n    <name/>\n    Prisma Raksila\n  </store>\n  <store>\n    <id>\n      3\n    </id>\n    <name/>\n    Siwa Muhos\n  </store>\n  <store>\n    <id>\n      4\n    </id>\n    <name/>\n    K-Supermarket Mimmi\n  </store>\n  <store>\n    <id>\n      5\n    </id>\n    <name/>\n    S-Market Koskiseutu\n  </store>\n  <store>\n    <id>\n      6\n    </id>\n    <name/>\n    K-Citymarket Kaakkuri\n  </store>\n  <store>\n    <id>\n      7\n    </id>\n    <name/>\n    Limingantullin Prisma\n  </store>\n</store_table>\n\n'

content_all_items_html = '1;0;"t\xc3\xa4ysmaito";\n2;0;"rasvaton maito";\n3;0;"kevytmaito";\n4;0;"rukiinen leip\xc3\xa4";\n5;0;"ranskanleip\xc3\xa4";\n6;0;"paahtoleip\xc3\xa4, Viisi viljaa";\n7;0;"keijumargariini";\n8;0;"floramargariini";\n9;0;"Oivariini";\n10;0;"leivontamargariini";\n11;0;"Pirkka-kahvi";\n12;0;"Saludo-kahvi";\n13;0;"Presidentti-kahvi";\n14;0;"perunalastu, Taffel";\n15;0;"dippi, Taffel";\n16;0;"dippi, Estrella";\n17;0;"nakkeja, HK";\n18;0;"nautajauheliha, 400g";\n19;0;"nauta-sikajauheliha";\n20;0;"kermaviili, Pirkka";\n21;0;"kahvikerma";\n22;0;"Marli Vital -mehu";\n23;0;"Sun-astiapesukoneaine, 70 kpl";\n24;0;"jogurtti, banaani, Valio, 1 l";\n25;0;"jogurtti, mansikka Valio, 1 l";\n26;0;"tikkuperunoita";\n27;0;"lihapy\xc3\xb6rykk\xc3\xa4, HK";\n28;0;"nakkeja, Atria";\n29;0;"wok-kasvismix, 1kg";\n30;0;"Lipton Yellow Label tee, 50 ps";\n31;0;"hammasharja, lasten";\n32;0;"hammasharja, aikuisten";\n33;0;"ananas, tuore";\n34;0;"suklaanappirulla, Marabou";\n35;0;"ylikyps\xc3\xa4 kinkkuleike, 250g, Atria";\n36;0;"keittokinkkuleike, 250g, Atria";\n37;0;"Daimrulla, Marabou";\n38;0;"sipuli, 1kg";\n39;0;"Lauantaipussi, 150g, Malaco";\n40;0;"Caesar-salaatti, Pirkka";\n41;0;"ruisleip\xc3\xa4, Ruiskiekko, Putaan Pulla";\n42;0;"Italian pata -pussi, Bl\xc3\xa5 Band";\n43;0;"tex mex -pata -pussi, Bl\xc3\xa5 Band";\n44;0;"appelsiinijuomatiiviste, 1.5l, Pirkka";\n45;0;"j\xc3\xa4\xc3\xa4tel\xc3\xb6, herkkutrio, Pingviini";\n46;0;"j\xc3\xa4\xc3\xa4tel\xc3\xb6, nougat, Pingviini";\n47;0;"saaristolaisleike, Kalavalmis";\n48;0;"kirjolohisuikale, 300g, Pirkka";\n49;0;"ylikyps\xc3\xa4 kinkkuleike, 300g, Snellman";\n50;0;"muffinsi, kaakao, Pirkka";\n51;0;"muffinsi, sitruuna, Pirkka";\n52;0;"jahtimakkara, 250g, Atria";\n53;0;"tomaatti, 1kg, Suomi";\n54;0;"ruisleip\xc3\xa4, Oululainen Reissumies";\n55;0;"limsa, Hartwall Jaffa 1.5l, keltainen";\n56;0;"limsa, Hartwall Jaffa 1.5l, punainen";\n57;0;"limsa, Coca-Cola 1.5l";\n58;0;"siideri, mansikka, Kopparberg";\n59;0;"juustosnacks, 275g, Taffel";\n60;0;"jogurtti, banaani, 8x125g, Valio";\n61;0;"jogurtti, mansikka, 8x125g, Valio";\n62;0;"jogurtti, hedelm\xc3\xa4pommi, 8x125g, Valio";\n63;0;"jogurtti, banaani, 200g, Valio";\n64;0;"jogurtti, mansikka, 200g, Valio";\n65;0;"jogurtti, hedelm\xc3\xa4pommi, 200g, Valio";\n66;0;"karkki, eucalyptus, Fazer";\n67;0;"tortillapohja, 8kpl/360g, Pirkka";\n68;0;"broilerin paistisuikale, Pirkka";\n69;0;"olut, tumma lager, 0.5l, Pirkka";\n70;0;"olut, vaalea lager, 0.33l, Pirkka";\n71;0;"juusto, emmental 400g, Pirkka";\n72;0;"j\xc3\xa4\xc3\xa4salaatti, Pirkka";\n73;0;"tomaattimurska, 390g, Pirkka";\n74;0;"meetvursti, valkosipuli, Atria";\n75;0;"salsadippi, keskivahva, 315g, Pirkka";\n76;0;"sinihomejuusto, 175g, Pirkka";\n77;0;"valkohomejuusto, 175g, Pirkka";\n78;0;"sinihomejuusto, Aura";\n79;0;"tuorekurkku, 1kg, Suomi";\n80;0;"kalkkunaleike, 250g, Atria";\n81;0;"kananmuna, 15kpl";\n82;0;"kanan koipipalat, 1kg";\n83;0;"WC-paperi";\n84;0;"talouspaperi";\n85;0;"suihkusaippua, Bergamot";\n86;0;"suihkusaippua, Sport";\n87;0;"n\xc3\xa4kkileip\xc3\xa4, Kunto";\n'


content_all_items_text = '1;0;t\xc3\xa4ysmaito;\n2;0;rasvaton maito;\n3;0;kevytmaito;\n4;0;rukiinen leip\xc3\xa4;\n5;0;ranskanleip\xc3\xa4;\n6;0;paahtoleip\xc3\xa4, Viisi viljaa;\n7;0;keijumargariini;\n8;0;floramargariini;\n9;0;Oivariini;\n10;0;leivontamargariini;\n11;0;Pirkka-kahvi;\n12;0;Saludo-kahvi;\n13;0;Presidentti-kahvi;\n14;0;perunalastu, Taffel;\n15;0;dippi, Taffel;\n16;0;dippi, Estrella;\n17;0;nakkeja, HK;\n18;0;nautajauheliha, 400g;\n19;0;nauta-sikajauheliha;\n20;0;kermaviili, Pirkka;\n21;0;kahvikerma;\n22;0;Marli Vital -mehu;\n23;0;Sun-astiapesukoneaine, 70 kpl;\n24;0;jogurtti, banaani, Valio, 1 l;\n25;0;jogurtti, mansikka Valio, 1 l;\n26;0;tikkuperunoita;\n27;0;lihapy\xc3\xb6rykk\xc3\xa4, HK;\n28;0;nakkeja, Atria;\n29;0;wok-kasvismix, 1kg;\n30;0;Lipton Yellow Label tee, 50 ps;\n31;0;hammasharja, lasten;\n32;0;hammasharja, aikuisten;\n33;0;ananas, tuore;\n34;0;suklaanappirulla, Marabou;\n35;0;ylikyps\xc3\xa4 kinkkuleike, 250g, Atria;\n36;0;keittokinkkuleike, 250g, Atria;\n37;0;Daimrulla, Marabou;\n38;0;sipuli, 1kg;\n39;0;Lauantaipussi, 150g, Malaco;\n40;0;Caesar-salaatti, Pirkka;\n41;0;ruisleip\xc3\xa4, Ruiskiekko, Putaan Pulla;\n42;0;Italian pata -pussi, Bl\xc3\xa5 Band;\n43;0;tex mex -pata -pussi, Bl\xc3\xa5 Band;\n44;0;appelsiinijuomatiiviste, 1.5l, Pirkka;\n45;0;j\xc3\xa4\xc3\xa4tel\xc3\xb6, herkkutrio, Pingviini;\n46;0;j\xc3\xa4\xc3\xa4tel\xc3\xb6, nougat, Pingviini;\n47;0;saaristolaisleike, Kalavalmis;\n48;0;kirjolohisuikale, 300g, Pirkka;\n49;0;ylikyps\xc3\xa4 kinkkuleike, 300g, Snellman;\n50;0;muffinsi, kaakao, Pirkka;\n51;0;muffinsi, sitruuna, Pirkka;\n52;0;jahtimakkara, 250g, Atria;\n53;0;tomaatti, 1kg, Suomi;\n54;0;ruisleip\xc3\xa4, Oululainen Reissumies;\n55;0;limsa, Hartwall Jaffa 1.5l, keltainen;\n56;0;limsa, Hartwall Jaffa 1.5l, punainen;\n57;0;limsa, Coca-Cola 1.5l;\n58;0;siideri, mansikka, Kopparberg;\n59;0;juustosnacks, 275g, Taffel;\n60;0;jogurtti, banaani, 8x125g, Valio;\n61;0;jogurtti, mansikka, 8x125g, Valio;\n62;0;jogurtti, hedelm\xc3\xa4pommi, 8x125g, Valio;\n63;0;jogurtti, banaani, 200g, Valio;\n64;0;jogurtti, mansikka, 200g, Valio;\n65;0;jogurtti, hedelm\xc3\xa4pommi, 200g, Valio;\n66;0;karkki, eucalyptus, Fazer;\n67;0;tortillapohja, 8kpl/360g, Pirkka;\n68;0;broilerin paistisuikale, Pirkka;\n69;0;olut, tumma lager, 0.5l, Pirkka;\n70;0;olut, vaalea lager, 0.33l, Pirkka;\n71;0;juusto, emmental 400g, Pirkka;\n72;0;j\xc3\xa4\xc3\xa4salaatti, Pirkka;\n73;0;tomaattimurska, 390g, Pirkka;\n74;0;meetvursti, valkosipuli, Atria;\n75;0;salsadippi, keskivahva, 315g, Pirkka;\n76;0;sinihomejuusto, 175g, Pirkka;\n77;0;valkohomejuusto, 175g, Pirkka;\n78;0;sinihomejuusto, Aura;\n79;0;tuorekurkku, 1kg, Suomi;\n80;0;kalkkunaleike, 250g, Atria;\n81;0;kananmuna, 15kpl;\n82;0;kanan koipipalat, 1kg;\n83;0;WC-paperi;\n84;0;talouspaperi;\n85;0;suihkusaippua, Bergamot;\n86;0;suihkusaippua, Sport;\n87;0;n\xc3\xa4kkileip\xc3\xa4, Kunto;\n'


content_all_items_xml = '<?xml version="1.0" ?>\n<item_table>\n  <item languageid="0">\n    <id>\n      1\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      t\xc3\xa4ysmaito\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      2\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      rasvaton maito\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      3\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      kevytmaito\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      4\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      rukiinen leip\xc3\xa4\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      5\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      ranskanleip\xc3\xa4\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      6\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      paahtoleip\xc3\xa4, Viisi viljaa\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      7\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      keijumargariini\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      8\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      floramargariini\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      9\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      Oivariini\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      10\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      leivontamargariini\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      11\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      Pirkka-kahvi\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      12\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      Saludo-kahvi\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      13\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      Presidentti-kahvi\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      14\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      perunalastu, Taffel\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      15\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      dippi, Taffel\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      16\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      dippi, Estrella\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      17\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      nakkeja, HK\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      18\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      nautajauheliha, 400g\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      19\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      nauta-sikajauheliha\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      20\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      kermaviili, Pirkka\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      21\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      kahvikerma\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      22\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      Marli Vital -mehu\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      23\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      Sun-astiapesukoneaine, 70 kpl\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      24\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      jogurtti, banaani, Valio, 1 l\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      25\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      jogurtti, mansikka Valio, 1 l\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      26\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      tikkuperunoita\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      27\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      lihapy\xc3\xb6rykk\xc3\xa4, HK\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      28\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      nakkeja, Atria\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      29\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      wok-kasvismix, 1kg\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      30\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      Lipton Yellow Label tee, 50 ps\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      31\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      hammasharja, lasten\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      32\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      hammasharja, aikuisten\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      33\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      ananas, tuore\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      34\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      suklaanappirulla, Marabou\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      35\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      ylikyps\xc3\xa4 kinkkuleike, 250g, Atria\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      36\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      keittokinkkuleike, 250g, Atria\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      37\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      Daimrulla, Marabou\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      38\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      sipuli, 1kg\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      39\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      Lauantaipussi, 150g, Malaco\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      40\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      Caesar-salaatti, Pirkka\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      41\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      ruisleip\xc3\xa4, Ruiskiekko, Putaan Pulla\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      42\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      Italian pata -pussi, Bl\xc3\xa5 Band\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      43\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      tex mex -pata -pussi, Bl\xc3\xa5 Band\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      44\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      appelsiinijuomatiiviste, 1.5l, Pirkka\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      45\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      j\xc3\xa4\xc3\xa4tel\xc3\xb6, herkkutrio, Pingviini\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      46\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      j\xc3\xa4\xc3\xa4tel\xc3\xb6, nougat, Pingviini\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      47\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      saaristolaisleike, Kalavalmis\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      48\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      kirjolohisuikale, 300g, Pirkka\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      49\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      ylikyps\xc3\xa4 kinkkuleike, 300g, Snellman\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      50\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      muffinsi, kaakao, Pirkka\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      51\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      muffinsi, sitruuna, Pirkka\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      52\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      jahtimakkara, 250g, Atria\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      53\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      tomaatti, 1kg, Suomi\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      54\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      ruisleip\xc3\xa4, Oululainen Reissumies\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      55\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      limsa, Hartwall Jaffa 1.5l, keltainen\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      56\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      limsa, Hartwall Jaffa 1.5l, punainen\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      57\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      limsa, Coca-Cola 1.5l\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      58\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      siideri, mansikka, Kopparberg\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      59\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      juustosnacks, 275g, Taffel\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      60\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      jogurtti, banaani, 8x125g, Valio\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      61\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      jogurtti, mansikka, 8x125g, Valio\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      62\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      jogurtti, hedelm\xc3\xa4pommi, 8x125g, Valio\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      63\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      jogurtti, banaani, 200g, Valio\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      64\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      jogurtti, mansikka, 200g, Valio\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      65\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      jogurtti, hedelm\xc3\xa4pommi, 200g, Valio\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      66\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      karkki, eucalyptus, Fazer\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      67\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      tortillapohja, 8kpl/360g, Pirkka\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      68\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      broilerin paistisuikale, Pirkka\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      69\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      olut, tumma lager, 0.5l, Pirkka\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      70\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      olut, vaalea lager, 0.33l, Pirkka\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      71\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      juusto, emmental 400g, Pirkka\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      72\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      j\xc3\xa4\xc3\xa4salaatti, Pirkka\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      73\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      tomaattimurska, 390g, Pirkka\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      74\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      meetvursti, valkosipuli, Atria\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      75\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      salsadippi, keskivahva, 315g, Pirkka\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      76\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      sinihomejuusto, 175g, Pirkka\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      77\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      valkohomejuusto, 175g, Pirkka\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      78\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      sinihomejuusto, Aura\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      79\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      tuorekurkku, 1kg, Suomi\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      80\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      kalkkunaleike, 250g, Atria\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      81\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      kananmuna, 15kpl\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      82\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      kanan koipipalat, 1kg\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      83\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      WC-paperi\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      84\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      talouspaperi\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      85\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      suihkusaippua, Bergamot\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      86\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      suihkusaippua, Sport\n    </name>\n  </item>\n  <item languageid="0">\n    <id>\n      87\n    </id>\n    <shoppinglistid>\n      0\n    </shoppinglistid>\n    <name>\n      n\xc3\xa4kkileip\xc3\xa4, Kunto\n    </name>\n  </item>\n</item_table>\n\n'


class PerfT(unittest.TestCase):

    def setUp(self):
        self.h = httplib2.Http('/tmp/.cache')
        self.h.disable_ssl_certificate_validation = True
        self.URL1 = 'https://projects.sse.fi/cgi-bin/ecoslbe1/'
        self.URL2 = 'https://projects.sse.fi/ecotest/ecoslbe2.py/'

    def test_01_be1_fetch_languages_html(self):
        response, content = self.h.request(self.URL1 + '?listaction=languages')
        self.assertEqual(content_languages_html_text, content)

    def test_02_be1_fetch_languages_text(self):
        response, content = self.h.request(self.URL1 + '?listaction=languages&type=text')
        self.assertEqual(content_languages_html_text, content)

    def test_03_be1_fetch_languages_xml(self):
        response, content = self.h.request(self.URL1 + '?listaction=languages&type=xml')
        self.assertEqual(content_languages_xml, content)

    def test_04_be1_fetch_stores_html(self):
        response, content = self.h.request(self.URL1 + '?listaction=stores')
        self.assertEqual(content_stores_html_text, content)

    def test_05_be1_fetch_stores_text(self):
        response, content = self.h.request(self.URL1 + '?listaction=stores&type=text')
        self.assertEqual(content_stores_html_text, content)

    def test_06_be1_fetch_stores_xml(self):
        response, content = self.h.request(self.URL1 + '?listaction=stores&type=xml')
        self.assertEqual(content_stores_xml, content)

    def test_07_be1_fetch_all_items_html(self):
        response, content = self.h.request(self.URL1 + '?listaction=allitems')
        #self.assertEqual(content_all_items_html, content)

    def test_08_be1_fetch_all_items_text(self):
        response, content = self.h.request(self.URL1 + '?listaction=allitems&type=text')
        #self.assertEqual(content_all_items_text, content)

    def test_09_be1_fetch_all_items_xml(self):
        response, content = self.h.request(self.URL1 + '?listaction=allitems&type=xml')
        #self.assertEqual(content_all_items_xml, content)

    def test_10_be1_fetch_single_items_html(self):
        for ind in range(1, 40):
            response, content = self.h.request(self.URL1 + '?listaction=item&itemid=%u&languageid=1' % ind)

    def test_11_be1_fetch_single_items_text(self):
        for ind in range(1, 40):
            response, content = self.h.request(self.URL1 + '?listaction=item&itemid=%u&languageid=1&type=text' % ind)

    def test_12_be1_fetch_single_items_xml(self):
        for ind in range(1, 40):
            response, content = self.h.request(self.URL1 + '?listaction=item&itemid=%u&languageid=1&type=xml' % ind)

    def test_13_be1_fetch_shopping_list_html(self):
        response, content = self.h.request(self.URL1 + '?listaction=shoppinglist&shoppinglistid=4&languageid=2&storeid=1')

    def test_14_be1_fetch_shopping_list_text(self):
        response, content = self.h.request(self.URL1 + '?listaction=shoppinglist&shoppinglistid=4&languageid=2&storeid=1&type=text')

    def test_15_be1_fetch_shopping_list_xml(self):
        response, content = self.h.request(self.URL1 + '?listaction=shoppinglist&shoppinglistid=4&languageid=2&storeid=1&type=xml')

    def test_16_be2_fetch_languages_html(self):
        response, content = self.h.request(self.URL2 + 'languages?outputtype=html')
        self.assertEqual(content_languages_html_text, content)

    def test_17_be2_fetch_languages_text(self):
        response, content = self.h.request(self.URL2 + 'languages?outputtype=text')
        self.assertEqual(content_languages_html_text, content)

    def test_18_be2_fetch_languages_xml(self):
        response, content = self.h.request(self.URL2 + 'languages?outputtype=xml')
        self.assertEqual(content_languages_xml, content)

    def test_19_be2_fetch_stores_html(self):
        response, content = self.h.request(self.URL2 + 'stores?outputtype=html')
        self.assertEqual(content_stores_html_text, content)

    def test_20_be2_fetch_stores_text(self):
        response, content = self.h.request(self.URL2 + 'stores?outputtype=text')
        self.assertEqual(content_stores_html_text, content)

    def test_21_be2_fetch_stores_xml(self):
        response, content = self.h.request(self.URL2 + 'stores?outputtype=xml')
        self.assertEqual(content_stores_xml, content)

    def test_22_be2_fetch_all_items_html(self):
        response, content = self.h.request(self.URL2 + 'allitems?lang=0&outputtype=html')
        #self.assertEqual(content_all_items_html, content)

    def test_23_be2_fetch_all_items_text(self):
        response, content = self.h.request(self.URL2 + 'allitems?lang=0&outputtype=text')
        #self.assertEqual(content_all_items_text, content)

    def test_24_be2_fetch_all_items_xml(self):
        response, content = self.h.request(self.URL2 + 'allitems?lang=0&outputtype=xml')
        #self.assertEqual(content_all_items_xml, content)

    def test_25_be2_fetch_single_items_html(self):
        for ind in range(1, 40):
            response, content = self.h.request(self.URL2 + 'singleitem?itemid=%u&lang=1&outputtype=html' % ind)

    def test_26_be2_fetch_single_items_text(self):
        for ind in range(1, 40):
            response, content = self.h.request(self.URL2 + 'singleitem?itemid=%u&lang=1&outputtype=text' % ind)

    def test_27_be2_fetch_single_items_xml(self):
        for ind in range(1, 40):
            response, content = self.h.request(self.URL2 + 'singleitem?itemid=%u&lang=1&outputtype=xml' % ind)

    def test_28_be2_fetch_shopping_list_html(self):
        response, content = self.h.request(self.URL2 + 'shoppinglist?slid=4&lang=2&storeid=1&outputtype=html')

    def test_29_be2_fetch_shopping_list_text(self):
        response, content = self.h.request(self.URL2 + 'shoppinglist?slid=4&lang=2&storeid=1&outputtype=text')

    def test_30_be2_fetch_shopping_list_xml(self):
        response, content = self.h.request(self.URL2 + 'shoppinglist?slid=4&lang=2&storeid=1&outputtype=xml')


if __name__ == '__main__':
    """"Main function."""

    # Running tests one by one:
    # run individual tests:
    # $ python -m unittest perftests.PerfT.test_01_be1_fetch_languages_html
    # $ python -m unittest perftests.PerfT.test_02_be1_fetch_languages_text

    suite = unittest.TestLoader().loadTestsFromTestCase(PerfT)
    unittest.TextTestRunner(verbosity=2).run(suite)


