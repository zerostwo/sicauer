# -*- coding: utf-8 -*-
import scrapy


class QuotesSpiderPySpider(scrapy.Spider):
    name = 'quotes_spider.py'
    allowed_domains = ['http://quotes.toscrape.com/']
    start_urls = ['http://http://quotes.toscrape.com//']

    def parse(self, response):
        pass
