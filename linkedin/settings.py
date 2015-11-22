# -*- coding: utf-8 -*-

# Scrapy settings for linkedin project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'linkedin'

SPIDER_MODULES = ['linkedin.spiders']
NEWSPIDER_MODULE = 'linkedin.spiders'

USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64)"

CONCURRENT_REQUESTS = 2

#DOWNLOADER_MIDDLEWARES = {
#    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
#}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'linkedin (+http://www.yourdomain.com)'
