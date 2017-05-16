# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.spiders import XMLFeedSpider
from babel_spider.items import BabelSpiderFeedItem


class NhkFeedSpider(XMLFeedSpider):
    name = 'nhk_feed'
    allowed_domains = ['www3.nhk.or.jp']
    # TODO: fix hardcoding
    start_urls = ['http://www3.nhk.or.jp/rss/news/cat6.xml']
    iterator = 'iternodes'
    itertag = 'item'

    def parse_node(self, response, selector):
        item = BabelSpiderFeedItem()
        item['url'] = selector.xpath('link/text()').extract()[0]
        item['category_id'] = 0
        item['media_id'] = 0
        item['published_at'] = selector.xpath('pubDate/text()').extract()[0]
        return item


class NhkContentSpider(Spider):
    name = "nhk_content"
    allowed_domains = ["http://www3.nhk.or.jp/"]
    start_urls = ['http://http://www3.nhk.or.jp//']

    def parse(self, response):
        pass
