# -*- coding: utf-8 -*-
import scrapy
from .. import items

class CompaniesSpider(scrapy.Spider):
    name = "companies"
    allowed_domains = ["www.linkedin.com"]
    start_urls = (
        'https://www.linkedin.com/directory/companies/',
    )

    def parse(self, response):
        links = response.css('li.content a::attr("href")').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_cat, meta={'proxy':'http://192.168.0.1:5566'})

    def parse_cat(self, response):
        links = response.css('li.content a::attr("href")').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_city_cat, meta={'proxy':'http://192.168.0.1:5566'})

    def parse_city_cat(self, response):
        links = response.css('li.content a::attr("href")').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_company, meta={'proxy':'http://192.168.0.1:5566'})

    def parse_company(self, response):
        item = items.LinkedinItem()
        item['company_name'] = "".join(response.css('.name>span::text').extract()).strip()
        item['industry'] = "".join(response.css('p.industry::text').extract()).strip()
        item['headquarters'] = "".join([ i.strip() for i in response.css('p.adr *::text').extract() ]).strip()
        return item
