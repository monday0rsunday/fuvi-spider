# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FuviItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    cover = scrapy.Field()
    sapo = scrapy.Field()
    link = scrapy.Field()
    src = scrapy.Field()
    site = scrapy.Field()
    ctime = scrapy.Field()
    catId = scrapy.Field()