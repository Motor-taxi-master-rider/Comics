# coding=utf-8

from scrapy.exporters import CsvItemExporter

code='utf-8'

class ComicsExporter(CsvItemExporter):
    def serialize_field(self, field, name, value):
        switcher = {
            'url': value,
            'introduction': value[0].encode(code).strip() if value else None,
            'update_time': value[0].encode(code).strip() if value else None,
            'last_update': value[0].encode(code).strip() if value else None,
            'classification': value[0].encode(code).strip() if value else None,
            'author': value[0].encode(code).strip() if value else None,
            'name': value[0].encode(code).strip() if value else None,
        }
        return switcher.get(name, [item.encode(code) for item in value])
