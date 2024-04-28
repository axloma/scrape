import scrapy
import requests
class AMAZ(scrapy.Spider):
    name = 'amx'
    start_urls = ['https://www.amazon.eg/s?rh=n%3A21858029031&fs=true&language=en&ref=lp_21858029031_sar']
    def parse(self, response):
        print(response.url,"RESOPNS")
        for procudct in response.css('a.s-pagination-next'):
            
            link = procudct.css('a.s-pagination-next').attrib['href']
            next_page_url = ""
            if not link.startswith('http'):
                next_page_url = requests.compat.urljoin(self.start_urls[0], link)                                                      
            item = {
                'name': link ,
                'link ': next_page_url,
             
            }
            #TODO return 

            yield item
        next_p = response.css('a.s-pagination-next').attrib['href']
        if next_p is not None:
            yield response.follow(next_p,callback=self.parse)