# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


def unicode_serializer(value):
    if value:
        return [item.encode('gbk') for item in value]
    else:
        return None


class ComicsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field(serializer=unicode_serializer)
    author = Field(serializer=unicode_serializer)
    update_time = Field(serializer=unicode_serializer)
    last_update = Field(serializer=unicode_serializer)
    classification = Field(serializer=unicode_serializer)
    introduction = Field(serializer=unicode_serializer)
    url = Field()
