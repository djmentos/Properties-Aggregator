#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Properties aggregator
#
# Authors: 
#  - Mateusz Misiak
#  - Daniel Kossakowski
#
# Requirements:
#  - curl
#  - sqlalchemy (python-sqlalchemy)
#  - mysql (python-mysqldb)
#  - jellyfish (pip)
#  - scipy (python-scipy)
#  - matplotlib (python-matplotlib)
#
import re
from otodom_pl import Otodom
from gratka_pl import Gratka
from olx_pl import Olx
from trojmiasto_pl import Trojmiasto
from manager import *
from hierarchy import calculate_relations

import sys

reload(sys)
sys.setdefaultencoding('utf8')

#dom.gratka.pl
#otodom.pl
#nieruchomosci.pl
#allegro.pl/nieruchomosci
#olx.pl/nieruchomosci
#domiporta.pl

def register_sources():
    """
    It should be done only once, if database is clean.
    """
    add_source('Otodom', 'otodom.pl')
    add_source('Gratka', 'dom.gratka.pl')
    add_source('Olx', 'olx.pl')

def run_crawler(city, page_fixed = None):
    """
    Starts exploring the sources.
    """

    p = Trojmiasto(city)
    trojmiasto_src = get_source_by_name('Trojmiasto')
    print p.get_properties(1)
    for i in p.get_properties(1):
        obj = p.get_property_details(i)
        if obj['price'] == '' or int(obj['price']) < 50000:
            print "Continue"
            continue
        print obj['price']
        add_property(obj['name'], trojmiasto_src, i, obj['locate'], obj['content'][:800], obj['price'].replace('&nbsp;', ''))
    return

    if not page_fixed is None:
        pages = range(int(page_fixed), int(page_fixed)+1)
    else:
        pages = range(1, 20)
        
    #otodom_src = get_source_by_name('Otodom')
    #p = Otodom(city)
    #for page in pages:
    #    print "Otodom, page: %d" % page
    #    for i in p.get_properties(page):
    #        obj = p.get_property_details(i)
    #        add_property(obj['name'], otodom_src, i, obj['locate'], obj['content'][:800], obj['price'].replace(' ', ''))

    gratka_src = get_source_by_name('Gratka')
    p = Gratka(city)
    for page in pages:
        print "[DEBUG] Gratka, page: %d" % page
        for i in p.get_properties(page):
            obj = p.get_property_details(i)
            add_property(obj['name'], gratka_src, i, obj['locate'], obj['content'][:800], obj['price'].replace('&nbsp;', ''))
            

def detect_duplicates():
    data = get_properties_data()
    ids = data['ids']
    linkage, results = calculate_relations(data, False)
    # print linkage
    
    flatList = results.tolist()
    duplikaty = 0
    id = 0
    # print flatList
    visited = []
    for item in flatList:
        if item in visited:
            id = id+1
            continue

        visited.append(item)
        # print "[%d] Cluster: %d" % (id, item)
        # prop1 = get_property_by_id(ids[id])
        # print "[%d] %s" %(prop1.id, prop1.url)

        header_printed = False
        id2 = 0
        for item2 in flatList:
            if item2 == item:
                if id2 != id:

                    if not header_printed:
                        header_printed = True
                        # print "[%d] Cluster: %d" % (id, item)
                        prop1 = get_property_by_id(ids[id])
                        print "[%d] %s" %(prop1.id, prop1.url)

                    prop2 = get_property_by_id(ids[id2])
                    if prop2.source == prop1.source:
                        if prop2.price > prop1.price:
                            print "PODOBNE (tańsze): [%d] %s" %(prop2.id, prop2.url)
                        else:
                            print "PODOBNE (droższe): [%d] %s" %(prop2.id, prop2.url)
                    else:
                        print "DUPLIKAT: [%d] %s" %(prop2.id, prop2.url)
                        duplikaty += 1
                    # print "[%d] (%d) - %s" % (prop2.id, id2, prop2.url)

            id2 = id2+1
        if header_printed:
            print ""
            print "-----"
            print ""
        id = id+1

    print "Liczba duplikatów: %d" % duplikaty
    # for item in results:
    #     itemL = item.tolist()
    #     print itemL
    #     # id1 = ids[int(itemL[0])]
        # id2 = ids[int(itemL[1])]
        # similarity = itemL[2]
        # print id1
        # print id2
        # print similarity

if __name__ == "__main__":
    print "Hello World"

    if len(sys.argv) > 1:
        run_crawler('gdansk', sys.argv[1])
    else:
        run_crawler('gdansk')
    #detect_duplicates()

    #print get_all_sources()
    #print get_all_properties()

    #print get_property_by_id(1)
    #print get_property_by_name('Test')
