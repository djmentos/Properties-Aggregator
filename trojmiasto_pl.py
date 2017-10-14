# -*- coding: utf-8 -*-
#
#
#
from downloader import Downloader

class Trojmiasto():
    
    def __init__(self, city):
        self.city = city
        

    def get_properties(self, page):
        
	if page == 1:
		url = 'http://ogloszenia.trojmiasto.pl/nieruchomosci-sprzedam/'
	else:
        	url = 'http://ogloszenia.trojmiasto.pl/nieruchomosci-sprzedam/?strona=' + str(page)

        item_pattern =  r'<div class="ogl-head">.*?<h2>.*?<a href="(.*?)">.*?</a>.*?</h2>.*?</div>'
        
        d = Downloader()
        output = d.get_sub_pages_links(url, item_pattern)
        
        return output
        
    def get_property_details(self, url):
        
        wanted = {
            'name'   : '<span id="ogl-title">(.*?)</span>',
            'price'  : '<div class="dd font-7">(.*?)</div>',
            'locate' : '<div class="dd">(.*?)</div>',
            'content': '<div class="ogl-description">(.*?)</div>',
        }
        
        d = Downloader()
        output = d.get_link_details(url, wanted)

        return output
        
