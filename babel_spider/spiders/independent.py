# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import XMLFeedSpider
from babel_spider.items import BabelSpiderItem
from babel_spider.queries import get_urls_by_media_id


class IndependentSpider(XMLFeedSpider):
    name = 'independent'
    allowed_domains = ['independent.co.uk']
    # TODO: fix hardcoding
    start_urls = ['http://www.independent.co.uk/news/world/rss']
    iterator = 'iternodes'
    itertag = 'item'
    media_id = 11
    urls_in_db = get_urls_by_media_id(media_id)
    
    def parse_node(self, response, selector):
        url = selector.xpath('link/text()').extract_first()
        if url not in self.urls_in_db:
            item = BabelSpiderItem()
            item['url'] = url
            item['category_id'] = 1
            item['media_id'] = self.media_id
            item['published_at'] = selector.xpath('pubDate/text()').extract_first()
            request = scrapy.Request(url, callback=self.content_parse)
            request.meta['item'] = item
            yield request
        else:
            print('skipped:' + url)
    
    def content_parse(self, response):
        item = response.meta['item']
        title = response.xpath('//h1[@itemprop="headline"]/text()').extract_first()
        content = ''.join(response.xpath('//div[@itemprop="articleBody"]/p/text() | //div[@itemprop="articleBody"]/p/a/text()').extract())
        item['title'] = title
        item['content'] = content
        if title and content:
            yield item
