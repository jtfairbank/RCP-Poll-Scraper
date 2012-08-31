# Scrapy settings for polldata project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'polldata'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['polldata.spiders']
NEWSPIDER_MODULE = 'polldata.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

FEED_FORMAT = 'csv'
FEED_URI = '../data/pres_latest.csv'
