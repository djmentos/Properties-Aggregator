#
#
#
from downloader import Downloader

class Partnerzy():
    
    def __init__(self, city):
	self.city = city

    
    def get_properties(self):

	url = ''
        
        d = Downloader()
        print d.get_sub_pages_links('http://www.wp.pl/', '')
        pass
