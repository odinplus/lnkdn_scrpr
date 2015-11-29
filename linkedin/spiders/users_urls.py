# -*- coding: utf-8 -*-
import scrapy
from .. import items
from urlparse import urljoin

class UsersSpider(scrapy.Spider):
    name = "users_urls"
    allowed_domains = ["linkedin.com"]
    start_urls = (
        'https://ch.linkedin.com',
#        'https://ch.linkedin.com/directory/people-a-1/',
    )

    def parse(self, response):
        links = response.css('.directory>ol>li>a:not(.country)::attr("href")').extract()
        for link in links:
            if not link.startswith('http'):
                l = urljoin(response.url, link)
            else:
                l = link
            yield scrapy.Request(l, callback=self.parse_first_level)

    def parse_first_level(self, response):
        links = response.css('li.content a::attr("href")').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_second_level)

    def parse_second_level(self, response):
        links = response.css('li.content a::attr("href")').extract()
        for link in links:
            if '/dir/' in link:
                continue
            if not link.startswith('http'):
                l = urljoin(response.url, link)
            else:
                l = link
            if '/directory/' in link:
                yield scrapy.Request(l, callback=self.parse_page_list)
            else:
                item = items.LinkedinUserItem()
                item['page_url'] = l
                yield item


    def parse_page_list(self, response):
        links = response.css('li.content a::attr("href")').extract()
        for link in links:
            if '/dir/' in link:
                continue
            if not link.startswith('http'):
                l = urljoin(response.url, link)
            else:
                l = link
            item = items.LinkedinUserItem()
            item['page_url'] = l
            yield item

