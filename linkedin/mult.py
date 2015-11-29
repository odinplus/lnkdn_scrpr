# -*- coding: utf-8 -*-
from scrapy.signalmanager import SignalManager
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from multiprocessing import Process,Queue
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from linkedin.spiders.bing import BingSpider


class CrawlerScript():

    def __init__(self):
        settings = get_project_settings()
        settings.set('LOG_ENABLED', False, priority='cmdline')
        #settings.overrides['LOG_ENABLED'] = False
        self.crawler = CrawlerProcess(settings)
        self.items = []
        SignalManager(dispatcher.Any).connect(self._item_passed, signal=signals.item_scraped)

    def _item_passed(self,item,response,spider):
        self.items.append(item)

    def _crawl(self, q, queue):
        self.crawler.crawl(BingSpider, q=q)
        self.crawler.start()
        self.crawler.stop()
        queue.put(self.items)

    def crawl(self, q):
        queue = Queue()
        p = Process(target=self._crawl, args=[q, queue])
        p.start()
        p.join()
        return queue.get(True)

crawler = CrawlerScript()


items = list()
items.append(crawler.crawl("James Isilay, Axpo Group"))
items.append(crawler.crawl("James Isilay, Axpo Group"))
print(len(items))

