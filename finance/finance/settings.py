# -*- coding: utf-8 -*-

# Scrapy settings for finance project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'finance'

SPIDER_MODULES = ['finance.spiders']
NEWSPIDER_MODULE = 'finance.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'finance (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
COOKIES_DEBUG = False
FEED_EXPORT_ENCODING = 'utf-8'
DOWNLOAD_DELAY = 0.5

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'finance.middlewares.RotateUserAgentMiddleware': 400,
}
ITEM_PIPELINES = {
    'finance.pipelines.FinancePipeline': 300,
}
RETRY_ENABLED = False
DUPEFILTER_DEBUG = True