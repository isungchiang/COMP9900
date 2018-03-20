# -*- coding: utf-8 -*-
import scrapy
import json
import re
from finance.items import YahooProfile


class YahooSpider(scrapy.Spider):
    name = 'yahoo'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.2,
        'COOKIES_ENABLED': False,
        'RETRY_ENABLED': False,
    }

    def start_requests(self):
        stock_id_list = []
        with open('./us_code.txt') as allcode:
            for line in allcode:
                stock_id_list.append(line.strip())

        for stock_id in stock_id_list:
            url = 'https://finance.yahoo.com/quote/{}/profile?ltr=1'.format(stock_id)
            yield scrapy.Request(url)

    def parse(self, response):
        record = YahooProfile()
        addressList = response.xpath('//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[1]/text()').extract()
        merged = ''
        for address in addressList:
            merged += address + '\t'

        record['Address'] = merged
        record['StockID'] = re.search(r'quote/([0-9a-zA-Z]+)', response.url).group(1)
        record['Corporation'] = response.xpath(
            '//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1/text()').extract_first()
        record['Market'] = response.xpath(
            '//*[@id="quote-header-info"]/div[2]/div[1]/div[2]/span/text()').extract_first()
        record['Contact'] = response.xpath(
            '//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[1]/a[1]/@href').extract_first()
        record['Sector'] = response.xpath(
            '//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/strong[1]/text()').extract_first()
        record['Industry'] = response.xpath(
            '//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/strong[2]/text()').extract_first()
        record['EmployeesNum'] = response.xpath(
            '//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/strong[3]/span/text()').extract_first()
        record['Description'] = response.xpath(
            '//*[@id="Col1-0-Profile-Proxy"]/section/section[2]/p/text()').extract_first()
        yield record
