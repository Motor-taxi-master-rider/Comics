# coding=utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.http import Request
from scrapy.exceptions import DropItem
from exporter import ComicsExporter
from exceptions import IOError

from config import db_config

import pymysql

code='utf-8'

class ComicsPipeline(object):
    '''scrapy pipeline for comics.
    '''
    def __init__(self):
        super(ComicsPipeline, self)
        #self.conn = pymysql.connect(**db_config)
        self.already_seen = set()
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        '''rewrite class method.

        define spider's open adn close action.
        '''
        pipeline = cls()
        crawler.signals.connect(
            pipeline.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(
            pipeline.spider_closed, signal=signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        '''open action.

        open a csv file and start exporting through exporter.
        '''
        try:
            file = open('%s_output.csv' % spider.name,
                        mode='w+')
        except IOError:
            print('==========OPEN FILE ERROR==========')

        print('Writing %s_output.json' % spider.name)
        self.files[spider] = file
        self.exporter = ComicsExporter(file, encoding=code)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        '''close action.

        stop exporting and close file.
        '''
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        '''rewrite class method.

        fields filter.
        '''
        if not item['name']:
            print('Missing name in %s' % item)
        if item['url'] in self.already_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.already_seen.add(item['url'])
            self.exporter.export_item(item)
            return item

    def handle_error(self, e):
        '''rewrite class method.

        error handler.
        '''
        log.err(e)
