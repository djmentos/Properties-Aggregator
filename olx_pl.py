# -*- coding: utf-8 -*-
#
#
#
from downloader import Downloader

class Olx():
    
    def __init__(self, city):
        self.city = city
        

    def get_properties(self):
        
        url = 'http://olx.pl/nieruchomosci/' + self.city + '/'
        item_pattern = r'<a href="(.*?)" class=".*? detailsLink"><strong>.*?</strong></a>'

        d = Downloader()
        output = d.get_sub_pages_links(url, item_pattern)
        
        print output
        
    def get_property_details(self, url):
        
        wanted = {
            'name' : '<h1 class="brkword lheight28">(.*?)</h1>',
	    'price' : '<div class="pricelabel tcenter">.*?<strong class="xxxx-large margintop7 block arranged">(.*?) zł</strong>.*?</div>',
            'locate' : '<span class="show-map-link link gray cpointer">.*?<strong class="c2b small">(.*?)</strong>.*?</span>',
            'content': '<p class="pding10 lheight20 large">(.*?)</p>',
        }
        
        d = Downloader()
        output = d.get_link_details(url, wanted)
        print output
        
