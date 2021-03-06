# -*- coding: utf-8 -*-
from pymongo import MongoClient
import scrapy
from .. import items

class UsersSpider(scrapy.Spider):
    name = "users"
    allowed_domains = ["linkedin.com"]

    def __init__(self, **kwargs):
        super(UsersSpider, self).__init__(**kwargs)
        if self.u:
                self.results=[self.u]
        else:
                self.db = MongoClient()
                docs = self.db['linkedin'].users.find({'topcard': {'$exists': False}}, {'page_url': 1, '_id':0}).limit(100000)
                self.results = [ i['page_url'] for i in list(docs) ]
                self.log(len(self.results))
                self.start_urls=["http://ch.linkedin.com"]

    def parse(self, response):
        for l in self.results:
            yield scrapy.Request(l, callback=self.parse_user_page, cookies={'lang': 'v=2&lang=en-us&c='})

    def parse_user_page(self, response):
        item = items.LinkedinUserItem()
        item['page_url'] = response.url
        topcard = response.css('section#topcard')
        experience = response.css('section#experience')
        certifications = response.css('section#certifications')
        skills = response.css('section#skills')
        education = response.css('section#education')
        recommendations = response.css('section#recommendations')
        groups = response.css('section#groups')
        if topcard:
            item['topcard'] = {}
            item['topcard']['member-connections'] = "".join(
                topcard.css('.member-connections>strong::text').extract()).strip()
            item['topcard']['full_name'] = "".join(topcard.css('#name::text').extract()).strip()
            item['topcard']['headline'] = "".join(topcard.css('.headline.title::text').extract()).strip()
            item['topcard']['locality'] = "".join(topcard.css('.locality::text').extract()).strip()
            item['topcard']['industry'] = "".join(
                topcard.xpath('.//*[@id="demographics"]/dd[2]/text()').extract()).strip()
            item['topcard']['current'] = "".join(topcard.css('.org *::text').extract()).strip()
        if experience:
            item['experience'] = []
            els = experience.css('li.position')
            for el in els:
                d = {}
                d['name'] = "".join(el.css('.item-title *::text').extract()).strip()
                d['company'] = "".join(el.css('.item-subtitle *::text').extract()).strip()
                times = el.css('.date-range>time::text')
                if len(times) > 0:
                    d['from'] = times[0].extract()
                if len(times) > 1:
                    d['to'] = times[1].extract()
                d['description'] = "".join(el.css('.description *::text').extract()).strip()
                item['experience'].append(d)
        if certifications:
            item['certifications'] = []
            els = certifications.css('li.certification')
            for el in els:
                d = {}
                d['name'] = "".join(el.css('.item-title *::text').extract()).strip()
                d['company'] = "".join(el.css('.item-subtitle *::text').extract()).strip()
                times = el.css('.date-range>time::text')
                if len(times) > 0:
                    d['from'] = times[0].extract()
                if len(times) > 1:
                    d['to'] = times[1].extract()
                item['certifications'].append(d)
        if skills:
            item['skills'] = []
            els = skills.css('li.skill')
            for el in els:
                item['skills'].append("".join(el.css('*::text').extract()).strip())
        if education:
            item['education'] = []
            els = education.css('li.school')
            for el in els:
                d = {}
                d['name'] = "".join(el.css('.item-title *::text').extract()).strip()
                d['company'] = "".join(el.css('.item-subtitle *::text').extract()).strip()
                times = el.css('.date-range>time::text')
                if len(times) > 0:
                    d['from'] = times[0].extract()
                if len(times) > 1:
                    d['to'] = times[1].extract()
                item['education'].append(d)
        if recommendations:
            item['recommendations'] = []
            els = recommendations.css('.recommendation')
            for el in els:
                item['recommendations'].append("".join(el.css('*::text').extract()).strip())
        if groups:
            item['groups'] = []
            els = groups.css('li.group')
            for el in els:
                item['groups'].append("".join(el.css('.item-title>a::text').extract()).strip())
        if topcard:
            return item
