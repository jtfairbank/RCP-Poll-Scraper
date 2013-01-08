import csv
from scrapy.contrib.exporter import CsvItemExporter

class HouseItemExporter(CsvItemExporter):
    def __init__(self, file, **kwargs):
        CsvItemExporter.__init__(self, file, **kwargs)

    def export_item(self, item):
        headers = ['#' + item['title'], item['candidates']]
        self.csv_writer.writerow(headers)
        CsvItemExporter.export_item(self, item)

