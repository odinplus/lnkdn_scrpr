# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkedinItem(scrapy.Item):
    company_name = scrapy.Field()
    industry = scrapy.Field()
    headquarters = scrapy.Field()

class LinkedinUserItem(scrapy.Item):
    page_url = scrapy.Field()
    full_name = scrapy.Field()
    position_name = scrapy.Field()
    position_company = scrapy.Field()
