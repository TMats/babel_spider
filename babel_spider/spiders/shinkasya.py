# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import XMLFeedSpider
from babel_spider.items import BabelSpiderItem
from datetime import datetime


class ShinkasyaSpider(XMLFeedSpider):
    name = 'shinkasya'
    allowed_domains = ['xinhuanet.com']
    # TODO: fix hardcoding
    start_urls = ['http://www.xinhuanet.com/world/news_world.xml']
    iterator = 'iternodes'
    itertag = 'item'

    def parse_node(self, response, selector):
        item = BabelSpiderItem()
        url = selector.xpath('link/text()').extract_first()
        item['url'] = url
        item['category_id'] = 1
        item['media_id'] = 4
        item['published_at'] = datetime.strptime(selector.xpath('text()').extract()[1], '%a,%d-%b-%Y %H:%M:%S %Z')
        # item['published_at'] = None
        request = scrapy.Request(url, callback=self.content_parse)
        request.meta['item'] = item
        yield request

    def content_parse(self, response):
        item = response.meta['item']
        # Not yet
        title = response.xpath('//div[@class="h-title"]/text()').extract_first()
        content = ''.join(response.xpath('//div[@id="p-detail"]/p/text()').extract())
        item['title'] = title
        item['content'] = content
        if title and content:
            yield item
