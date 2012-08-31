# Scrapy settings for polldata project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

from datetime import datetime

BOT_NAME = 'polldata'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['polldata.spiders']
NEWSPIDER_MODULE = 'polldata.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = [
    'polldata.pipelines.CsvExportPipeline',
]

LOG_FILE = 'logs/%s | %s | %s.txt' % (datetime.today(), BOT_NAME, BOT_VERSION)

ROBOTSTXT_OBEY = True
