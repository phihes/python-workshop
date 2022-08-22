import scrapy

class InnoSpider(scrapy.Spider):
    name = "innovation-economics"

    def start_requests(self):
        url = 'http://innovation-economics.de/'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

    	# get post title
        post_titles = response.css('h2.entry-title a::text').extract()
        post_urls = response.css('h2.entry-title a::attr(href)').extract()

        for title, url in zip(post_titles, post_urls):
	        yield ({
	        	'title':title,
	        	'url': url
	        })
