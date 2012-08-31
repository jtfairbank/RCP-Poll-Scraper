# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter

'''
Exports Poll Items into a CSV file in an order defined by the existing process.

It is currently setup only for the presidential poll items, but should be
modified to work with any poll item.
 - How do we define the item field's order for a general exporter?
    - Define them in the item itself?
 - From BaseItemExporter:
    - fields_to_export (CsvItemExporter will respect the order)
'''
class CsvExportPipeline(object):
    def __init__(self):
        self.files = {}

    # see extensions in scrappy documentation
    # this is the main entry point for the pipeline
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('data/pres_latest.csv', 'w+')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file, fields_to_export=spider.fields_to_export)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
