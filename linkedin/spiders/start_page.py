import scrapy
from .. import items
from scrapy.shell import inspect_response
from scrapy.http import FormRequest


class StartPageSpider(scrapy.Spider):
    name = "startpage"
    allowed_domains = ["startpage.com"]
    #    start_urls = (
    #        'https://www.google.com/search?q=Salt+Mobile+SA,+Abdelghani+Hannachi',
    #        'https://ch.linkedin.com/directory/people-a-1/',
    #    )

    def __init__(self, q, **kwargs):
        super(StartPageSpider, self).__init__(**kwargs)

    def start_requests(self):
        return [FormRequest("https://startpage.com/do/search",
                            formdata={'abp': '-1',
                                      'cat': 'web',
                                      'cmd': 'process_search',
                                      'enginecount': '1',
                                      'ff': '',
                                      'flag_ac': '0',
                                      'language': 'english',
                                      'nj': '1',
                                      'pl': '',
                                      'query': self.q, #'Salt Mobile SA, Abdelghani Hannachi',
                                      'theme': '',
                                      'ycc': '0'}
                            ,
                            callback=self.parse)]

    def parse(self, response):
        links = response.css('.result .clk>a')
        item = items.GoogleItem()
        item['results'] = []
        #       inspect_response(response, self)
        for link in links:
            href = "".join(link.css('::attr("href")').extract()).strip()
            text = "".join(link.css('::text').extract()).strip()
            if 'linkedin' in href:
                return scrapy.Request(href, callback=self.parse_city_cat, cookies = {'lang':'v=2&lang=en-us&c='})

    def parse_city_cat(self, response):
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
            item['topcard']['member-connections'] = "".join(topcard.css('.member-connections>strong::text').extract()).strip()
            item['topcard']['full_name'] = "".join(topcard.css('#name::text').extract()).strip()
            item['topcard']['headline'] = "".join(topcard.css('.headline.title::text').extract()).strip()
            item['topcard']['locality'] = "".join(topcard.css('.locality::text').extract()).strip()
            item['topcard']['industry'] = "".join(topcard.xpath('.//*[@id="demographics"]/dd[2]/text()').extract()).strip()
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
            els = experience.css('li.certification')
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
            els = experience.css('li.skill')
            for el in els:
                item['skills'].append("".join(el.css('*::text').extract()).strip())
        if education:
            item['education'] = []
            els = experience.css('li.school')
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
            els = experience.css('.recommendation')
            for el in els:
                item['recommendations'].append("".join(el.css('*::text').extract()).strip())
        if groups:
            item['groups'] = []
            els = experience.css('li.group')
            for el in els:
                item['groups'].append("".join(el.css('.item-title>a::text').extract()).strip())
        return item
