# -*- coding: utf-8 -*-
#
#
#
from downloader import Downloader

class Gratka():
    
    def __init__(self, city):
        self.city = city
        

    def get_properties(self, page):
        
        url = 'http://dom.gratka.pl/mieszkania-sprzedam/lista/pomorskie,' + self.city + ',40,' + str(page) + ',li,s.html'
        item_pattern = r'<a.*?href="(.*?)".*?>.*?<\/a>'

        d = Downloader()
        result = d.get_sub_pages_links(url, item_pattern)
        
        output = []
        for r in result:
            if 'tresc' in r:
                output.append('http://dom.gratka.pl' + r)

        return output
        
    def get_property_details(self, url):
        
        wanted = {
            'name'  : '<div id="karta-naglowek" class="small-12 columns">.*?<h1>(.*?)</h1>.*?</div>',
            'price' : '<div class="cenaGlowna">.*?<p>.*?<b>(.*?)</b>.*?</p>.*?</div>',
            'locate' : '<h2 class="hide-for-small">.*?mieszkanie na sprzedaż (.*?)</h2>',
            'content': '<div class="opis">.*?<h4>Opis dodatkowy</h4>(.*?)</div>'
        }
        
        d = Downloader()

        output = d.get_link_details(url, wanted)
        return output
        
