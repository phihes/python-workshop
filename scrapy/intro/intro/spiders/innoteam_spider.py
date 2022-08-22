import scrapy


class InnoTeamSpider(scrapy.Spider):
    name = "innoteam"

    def start_requests(self):
        urls = [
            'https://www.inno.tu-berlin.de/menue/about_us/team/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for cell in response.xpath('//*[@id="main"]//tbody//td[1]//text()'):
            n = cell.get().strip()
            if n != "":
                yield({'name': n})