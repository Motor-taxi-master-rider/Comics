# coding:utf-8
import sys
sys.path.append('..\..\Comics')
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from Comics.items import ComicsItem


class Comics(CrawlSpider):

    name = "comics"
    allowed_domains = ["www.tazhe.com"]
    start_urls = ["http://www.tazhe.com/mh/"]
    rules = [
        Rule(LxmlLinkExtractor(allow=(r'http://www.tazhe.com/mh/\d+')),
             callback="parse_item"),
    ]

    def __init__(self, *args, **kwargs):
        super(Comics, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        sel = response.selector
        item = ComicsItem()
        item['name'] = sel.xpath(
            '//*[@id="intro_l"]/div[1]/h1/text()').extract()
        item['author'] = sel.xpath(
            '//*[@id="intro_l"]/div[2]/p[2]/text()').extract()
        item['update_time'] = sel.xpath(
            '//*[@id="intro_l"]/div[2]/p[1]/span/text()').extract()
        item['last_update'] = sel.xpath(
            '//*[@id="intro_l"]/div[1]/span/font/text()').extract()
        item['classification'] = sel.xpath(
            '//*[@id="intro_l"]/div[2]/p[5]/a/text()').extract()
        item['introduction'] = sel.xpath(
            '//*[@id="intro1"]/p/text()[1]').extract()
        item['url'] = response.url
        return item
