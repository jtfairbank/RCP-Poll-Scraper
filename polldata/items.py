# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class PresPollItem(Item):
    # define the fields for your item here like:
    state   = Field()
    service = Field()
    start   = Field()
    end     = Field()
    sample  = Field()
    voters  = Field()
    dem     = Field()
    rep     = Field()
    ind     = Field()
