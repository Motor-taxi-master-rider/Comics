# coding:utf-8
import sys
sys.path.append('..\..\Comics')
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from Comics.items import ComicsItem


class Comics(CrawlSpider):

    name = "comics"
    allowed_domains = ["www.tazhe.com"]
    start_urls = ["http://www.tazhe.com/mh/"]
    rules = [
        Rule(SgmlLinkExtractor(allow=(r'http://http://www.tazhe.com/mh/\d+')),
             callback="parse_item"),
    ]
    def parse_item(self, response):
        sel=Selector(response)
        item=ComicsItem()
        item['name']=sel.xpath('//*[@id="intro_l"]/div[1]/h1/text()').extract()
        item['author']=sel.xpath('//*[@id="intro_l"]/div[2]/p[2]/text()').extract()
        item['update_time']=sel.xpath('//*[@id="intro_l"]/div[2]/p[1]/span/text()').extract()
        item['last_update']=sel.xpath('//*[@id="intro_l"]/div[1]/span/font/text()').extract()
        item['classification']=sel.xpath('//*[@id="intro_l"]/div[2]/p[5]/a/text()').extract()
        item['introduction']=sel.xpath('//*[@id="intro1"]/p/text()[1]').extract()
