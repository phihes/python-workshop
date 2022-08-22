import scrapy
from googleapiclient.discovery import build
import re
from bs4 import BeautifulSoup

service = build("customsearch", "v1", developerKey="AIzaSyBhJtIHjbpyKNeRuPIk__LwTRNT1tIjRBM")

class InnoTeamSpider(scrapy.Spider):
    name = "google_inno_text"

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
        soup = BeautifulSoup(response.body.decode("utf-8"))

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        yield({'site':response.url, 'text': text})