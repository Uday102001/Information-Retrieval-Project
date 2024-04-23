import scrapy
from pathlib import Path


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]

    start_urls = [
        "http://quotes.toscrape.com/tag/love/",
        "http://quotes.toscrape.com/tag/inspirational/",
        "http://quotes.toscrape.com/tag/life/",
        "http://quotes.toscrape.com/tag/humor/"
    ]

    def __init__(self, max_pages=None, max_depth=None, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.max_pages = int(max_pages) if max_pages else float('inf')
        self.max_depth = int(max_depth) if max_depth else float('inf')
        self.visited_pages = set()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'depth': 1})

    def parse(self, response):
        if response.url not in self.visited_pages:
            self.visited_pages.add(response.url)
            page = response.url.split("/")[-2]
            filename = f"quotes-{page}.html"
            Path(filename).write_bytes(response.body)
            self.log(f"Saved file {filename}")

            if 'depth' in response.meta and response.meta['depth'] < self.max_depth:
                for link in response.css('a::attr(href)').extract():
                    if link.startswith("http://quotes.toscrape.com"):
                        yield response.follow(link, callback=self.parse, meta={'depth': response.meta['depth'] + 1})

            if len(self.visited_pages) >= self.max_pages:
                self.logger.info('Reached maximum pages limit. Crawling stopped.')
                return
