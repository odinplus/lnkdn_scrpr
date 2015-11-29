# -*- coding: utf-8 -*-
import scrapy
from users import UsersSpider

class BingSpider(scrapy.Spider):
    name = "bing"
    allowed_domains = ["bing.com", "linkedin.com"]

    def __init__(self, **kwargs):
        super(BingSpider, self).__init__(**kwargs)
        self.us = UsersSpider(u='aaaaaa')

    def start_requests(self):
        return [scrapy.Request("http://www.bing.com/search?q=%s " % self.q,
                               callback=self.parse)]

    def parse(self, response):
        links = response.css('#b_results li h2 a')
        for link in links:
            href = "".join(link.css('::attr("href")').extract()).strip()
            text = "".join(link.css('::text').extract()).strip()
            if 'linkedin.com' in href:
                return scrapy.Request(href, callback=self.us.parse_user_page, cookies={'lang': 'v=2&lang=en-us&c='})

