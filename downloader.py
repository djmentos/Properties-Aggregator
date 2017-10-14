# -*- coding: utf-8 -*-
#
# Module for downloading contents of websites.
#
import re
import pycurl
from StringIO import StringIO

class Downloader():
        
    def __get_site_content(self, url):
        """
        Return HTML of provided URL.
        """
        buffer = StringIO()
        
        c = pycurl.Curl()
        c.setopt(c.URL, url)

        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        
        ret = buffer.getvalue()
        c.close()
        
        return ret
        
        
    def get_sub_pages_links(self, url, pattern):
        """
        Return list of URLs to subpages related to provided pattern.
        """
        print "[DEBUG] Starting download: " + url + "..."
        html = self.__get_site_content(url)
        print "[DEBUG] Download completed. Compiling regex..."
        r = re.compile(pattern, re.S|re.M).findall(html)
        print "[DEBUG] Compilation completed."
        return r
    
    def get_link_details(self, url, dict):
        """
        Return list with wanted params.
        """
        r = {}
        print url
        for i, value in dict.iteritems():
            html = self.__get_site_content(url)
            reg_return = re.compile(value, re.S|re.M).findall(html)
            
            if len(reg_return) > 0:
                r[i] = reg_return[0]
                r[i] = r[i].replace('<br />', ' ')
                r[i] = r[i].replace('<br>', ' ')
                r[i] = re.sub("<.*?>", "", r[i]).strip().replace('&nbsp;', ' ')
                
                if i == 'price':
                    r[i] = r[i].replace('z\xb3', '')
                    r[i] = r[i].replace(' ', '')
                    r[i] = re.sub("[^0-9]", "", r[i])
                    r[i] = r[i].strip()
                
                if i == 'price' and not r[i].isdigit():
                    r[i] = '0'
            else:
                r[i] = ''

        return r
