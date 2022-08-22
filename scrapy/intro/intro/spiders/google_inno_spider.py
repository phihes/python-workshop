import scrapy
from googleapiclient.discovery import build
import re

service = build("customsearch", "v1", developerKey="AIzaSyBhJtIHjbpyKNeRuPIk__LwTRNT1tIjRBM")

class InnoTeamSpider(scrapy.Spider):
    name = "google_inno"

    def start_requests(self):

        # number of results
        num_results = 50

        found_results = 0
        while(found_results < num_results):                

            # execute google search
            res = service.cse().list(
                q='innovation+economics',
                num=10,
                start=found_results+1,
                cx="017215688371507106775:qathmp5izvh",
                lr="lang_de"
            ).execute()

            # crawl each page in google search results
            for item in res["items"]:
                print(item["link"])
                yield scrapy.Request(url=item["link"], callback=self.parse)

            # look for next 10 items
            found_results += 10

    def parse(self, response):
        # find all email addresses in website
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', response.body.decode("utf-8"))
        for e in emails:
            yield({
                'site': response.url,
                'email': e
            })