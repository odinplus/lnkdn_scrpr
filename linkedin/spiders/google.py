import scrapy
from .. import items

class GoogleSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["google.com"]
    start_urls = (
        'https://www.google.com/search?q=Salt+Mobile+SA,+Abdelghani+Hannachi',
#        'https://ch.linkedin.com/directory/people-a-1/',
    )

    def parse(self, response):
        links = response.css('.g .r>a')
        item = items.GoogleItem()
        item['results'] = []
        for link in links:
            href = link.css('::attr("href")').extract()
            href = href[href.index('http'):href.index('&')]
            text = link.css('::text').extract().strip()
            item['results'].append({ href: text })