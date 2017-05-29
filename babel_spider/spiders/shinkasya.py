# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import XMLFeedSpider
from babel_spider.items import BabelSpiderItem
from babel_spider.queries import get_urls_by_media_id
from datetime import datetime


class ShinkasyaSpider(XMLFeedSpider):
    name = 'shinkasya'
    allowed_domains = ['xinhuanet.com']
    # TODO: fix hardcoding
    start_urls = ['http://www.xinhuanet.com/world/news_world.xml']
    iterator = 'iternodes'
    itertag = 'item'
    media_id = 4
    urls_in_db = get_urls_by_media_id(media_id)

    def parse_node(self, response, selector):
        url = selector.xpath('link/text()').extract_first()
        if url not in self.urls_in_db:
            item = BabelSpiderItem()
            item['url'] = url
            item['category_id'] = 1
            item['media_id'] = self.media_id
            item['published_at'] = datetime.strptime(selector.xpath('text()').extract()[1], '%a,%d-%b-%Y %H:%M:%S %Z')
            request = scrapy.Request(url, callback=self.content_parse)
            request.meta['item'] = item
            yield request
        else:
            print('skipped:' + url)

    def content_parse(self, response):
        item = response.meta['item']
        # Not yet
        title = response.xpath('//div[@class="h-title"]/text()').extract_first()
        content = ''.join(response.xpath('//div[@id="p-detail"]/p/text()').extract())
        item['title'] = title
        item['content'] = content
        if title and content:
            yield item
