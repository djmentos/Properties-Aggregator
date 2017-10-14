# -*- coding: utf-8 -*-
#
#
#
from downloader import Downloader

class Otodom():
    
    def __init__(self, city):
        self.city = city
        

    def get_properties(self, page):
        
        if page == 1:
            url = 'http://otodom.pl/sprzedaz/mieszkanie/' + self.city + '/'
        else:
            url = 'http://otodom.pl/sprzedaz/mieszkanie/' + self.city + '/?page=' + str(page)

        item_pattern =  r'<article.*?class="offer-item.*?data-url="(.*?)">.*?<\/article>'
        
        d = Downloader()
        output = d.get_sub_pages_links(url, item_pattern)
        
        return output
        
    def get_property_details(self, url):
        
        wanted = {
            'name'   : '<header class="col-md-8">.*?<h1>(.*?)</h1>.*?</header>',
            'price'  : '<li>cena <span><strong>(.*?) zł</strong></span>.*?</li>',
            'locate' : '<address class="hidden-xs">.*?<p>(.*?)</p>.*?</address>',
            'content': '<div class="col-md-offer-content">.*?<h3>Opis</h3>(.*?)<div class="print-contact visible-print-block">.*</div>.*?<div class="text-details clearfix">.*</div>',
        }
        
        d = Downloader()
        output = d.get_link_details(url, wanted)

        return output
        
