# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
from scrapy.http import Request
from scrapy.exceptions import DropItem

from config import db_config

import pymysql


class ComicsPipeline(object):
    def __init__(self):
        super(ComicsPipeline, self)
        self.conn = pymysql.connect(**db_config)
        self.already_seen = set()

    def open_spider(self, spider):
        print('start pipeline')

    def process_item(self, item, spider):
        if not item['name']:
            print('Missing name in %s' % item)
        if item['url'] in self.already_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.already_seen.add(item['url'])

        return item

    def handle_error(self, e):
        log.err(e)
