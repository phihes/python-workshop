import scrapy

class InnoSpider(scrapy.Spider):
    name = "inno"

    custom_settings = {
        'DEPTH_LIMIT': 2
    }    

    def start_requests(self):
        url = 'https://www.inno.tu-berlin.de/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

    	# collect all links from html
        links = response.css('a::attr(href)').getall()
        for l in links:
            yield response.follow(l, callback=self.parse)

    	# get the website title
        site_title = response.css('h1::text').get()
        site_title = ''.join([t for t in site_title if t in [" ",".",",",";"] or t.isalpha()])

        # save title and url
        yield ({
        	'title':site_title,
        	'url': response.url
        })
