# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request
from config import db_config

import pymysql


class ComicsPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(**db_config)

    def process_item(self, item, spider):
        for i in item:
            print(i)
        return item
