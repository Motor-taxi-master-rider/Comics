# coding=utf-8

from scrapy.contrib.exporter import JsonLinesItemExporter


class ComicsExporter(JsonLinesItemExporter):
    def serialize_field(self, field, name, value):
        switcher = {
            'url': value,
            'introduction': value[0].encode('utf-8').strip() if value else None,
            'update_time': value[0].encode('utf-8').strip() if value else None,
            'last_update': value[0].encode('utf-8').strip() if value else None,
            'name': value[0].encode('utf-8').strip() if value else None,
        }
        return switcher.get(name, [item.encode('utf-8') for item in value])
