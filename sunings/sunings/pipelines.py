# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sunings.settings import FIELDS_TO_EXPORT
from scrapy import signals
from scrapy.exporters import CsvItemExporter
import time
class SuningsPipeline(object):
    def process_item(self, item, spider):
        return item
class CSVPipeline(object):

  def __init__(self):
    self.files = {}

  @classmethod
  def from_crawler(cls, crawler):
    pipeline = cls()
    crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    return pipeline

  def spider_opened(self, spider):
    Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    file = open('%s_苏宁电饭煲%s.csv' % (spider.name,Time), 'wb')
    self.files[spider] = file
    self.exporter = CsvItemExporter(file)
    self.exporter.fields_to_export = FIELDS_TO_EXPORT
    self.exporter.start_exporting()

  def spider_closed(self, spider):
    self.exporter.finish_exporting()
    file = self.files.pop(spider)
    file.close()

  def process_item(self, item, spider):
    self.exporter.export_item(item)
    return item