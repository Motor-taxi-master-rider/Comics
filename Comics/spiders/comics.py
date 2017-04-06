# coding:utf-8

import scrapy
from bs4 import BeautifulSoup


class Comics(scrapy.Spider):

    name = "comics"

    def start_requests(self):
        urls = ['http://manhua.fzdm.com/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
#

    def parse(self, response):s
        content = response.body
        soup = BeautifulSoup(content, "html5lib")
