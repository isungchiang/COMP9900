# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YahooProfile(scrapy.Item):
    Corporation = scrapy.Field()
    Market = scrapy.Field()
    Address = scrapy.Field()
    Contact = scrapy.Field()
    Sector = scrapy.Field()
    Industry = scrapy.Field()
    EmployeesNum = scrapy.Field()
    Description = scrapy.Field()
    # CorporateGovernance = scrapy.Field()
    StockID = scrapy.Field()
    # KgID = scrapy.Field()