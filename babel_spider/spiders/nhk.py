# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
from babel_spider.items import BabelSpiderFeedItem


class NhkSpider(XMLFeedSpider):
    name = 'nhk'
    allowed_domains = ['www3.nhk.or.jp']
    start_urls = ['http://www3.nhk.or.jp/rss/news/cat6.xml']
    iterator = 'xml' # you can change this; see the docs
    itertag = 'item' # change it accordingly

    def parse_node(self, response, selector):
        item = BabelSpiderFeedItem()
        # item['url'] = selector.select('link').extract()[0]
        item['url'] = selector.xpath('//link/text()').extract()
        # item['url'] = response.xpath('//link').extract()
        # print(selector.select('link').xpath('//link/text()'))
        # print("here")
        item['category_id'] = 0
        item['media_id'] = 0
        return item
