import csv
from scrapy.contrib.exporter import CsvItemExporter

class HouseItemExporter(CsvItemExporter):
    def __init__(self, file, **kwargs):
        CsvItemExporter.__init__(self, file, include_headers_line=False, **kwargs)
        self.title_list = []

    def export_item(self, item):
        if item['title'] not in self.title_list:
            headers = ['#' + item['title'], item['candidates']]
            self.csv_writer.writerow(headers)
            self.title_list.append(item['title'])
        CsvItemExporter.export_item(self, item)

