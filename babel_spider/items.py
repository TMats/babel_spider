# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BabelSpiderFeedItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    category_id = scrapy.Field()
    media_id = scrapy.Field()
    published_at = scrapy.Field()
    pass
