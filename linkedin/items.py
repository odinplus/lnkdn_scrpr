# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkedinCompanyItem(scrapy.Item):
    company_name = scrapy.Field()
    industry = scrapy.Field()
    headquarters = scrapy.Field()

class LinkedinUserItem(scrapy.Item):
    page_url = scrapy.Field()
    topcard = scrapy.Field()
    experience = scrapy.Field()
    certifications = scrapy.Field()
    skills = scrapy.Field()
    education = scrapy.Field()
    recommendations = scrapy.Field()
    groups = scrapy.Field()

class GoogleItem(scrapy.Item):
    results = scrapy.Field()
