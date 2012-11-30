# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from scrapy.exceptions import DropItem
import json
import hashlib

class CsvExportPipeline(object):
    '''
    Exports Poll Items into a CSV file in an order defined by the existing process.

    It is currently setup only for the presidential poll items, but should be
    modified to work with any poll item.
     - How do we define the item field's order for a general exporter?
        - Define them in the item itself?
     - From BaseItemExporter:
        - fields_to_export (CsvItemExporter will respect the order)
    '''

    # TODO: Track spider names to make sure the same spider isn't running twice.
    #       Use some sort of persistent tracking?  ie a file that indicates a
    #       lock?
    #           - this would prevent the same spider from being run twice by
    #             two different calls to crawl

    def __init__(self):
        self.latest_polls_files = {}
        self.exporters = {}
        self.prev_polls_fNames = {}
        self.prev_polls = {}
        self.newitems = {}

    # see extensions in scrappy documentation
    # this is the main entry point for the pipeline
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        latest_polls_file = open('data/' + spider.name + '_latest.csv', 'w')
        self.latest_polls_files[spider] = latest_polls_file

        exporter = CsvItemExporter(latest_polls_file, fields_to_export=spider.fields_to_export)
        exporter.start_exporting()
        self.exporters[spider] = exporter

        prev_polls_fName = 'data/' + spider.name + '_dict.json'
        try:
            prev_polls_file = open(prev_polls_fName, 'r')
            prev_polls = json.load(prev_polls_file)
            prev_polls_file.close()
        except (IOError):
            # data/dict.json doesn't exist
            prev_polls = []
        except ValueError:
            # dict.json is malformed, should be inspected before being overwritten
            raise ValueError("Malformed prev_polls_file for " + spider.name + ".")
        self.prev_polls_fNames[spider] = prev_polls_fName
        self.prev_polls[spider] = prev_polls

        self.newitems[spider] = []

    def spider_closed(self, spider):
        sorteditems = sorted(self.newitems[spider], key=lambda item: item['state'])
        for item in sorteditems:
            self.exporters[spider].export_item(item)
        self.exporters[spider].finish_exporting()

        latest_polls_file = self.latest_polls_files.pop(spider)
        latest_polls_file.close()

        prev_polls_fName = self.prev_polls_fNames.pop(spider)
        prev_polls_file = open(prev_polls_fName, 'w')
        prev_polls_file.write( json.dumps(self.prev_polls[spider]) )
        prev_polls_file.close()

    def process_item(self, item, spider):
        prev_polls = self.prev_polls[spider]

        identifier = item['dem']+item['end']+item['rep']+str(item['ind'])+item['sample']+item['service']
        hasher = hashlib.md5()
        hasher.update(identifier)

        poll_hash = hasher.hexdigest()
        if poll_hash not in prev_polls:
            prev_polls.append(poll_hash)
            self.newitems[spider].append(item)
            return item
        else:
            raise DropItem("Poll is not new.")
