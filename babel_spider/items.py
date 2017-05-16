# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BabelSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    category_id = scrapy.Field()
    media_id = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    published_at = scrapy.Field()
    pass
