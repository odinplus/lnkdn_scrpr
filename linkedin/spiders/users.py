# -*- coding: utf-8 -*-
import scrapy
from .. import items


class UsersSpider(scrapy.Spider):
    name = "users"
    allowed_domains = ["www.ch.linkedin.com"]
    start_urls = (
        'https://ch.linkedin.com/directory/people-a-1/',
    )

    def parse(self, response):
        links = response.css('li.content a::attr("href")').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_cat)

    def parse_cat(self, response):
        links = response.css('li.content a::attr("href")').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_city_cat)

    def parse_city_cat(self, response):
        item = items.LinkedinUserItem()
        item['page_url'] = response.url
        item['full_name'] = "".join(response.css('#name::text').extract()).strip()
        present_expirience = response.xpath('.//*[@id="experience"]/ul/li[@class="position"and descendant::span[text()="Present"]]')
        for el in present_expirience:
            item['position_name'] = "".join(el.css('.item-title *::text').extract()).strip()
            item['position_company'] = "".join(el.css('.item-subtitle *::text').extract()).strip()
        return item
