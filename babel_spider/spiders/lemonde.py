# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import XMLFeedSpider
from babel_spider.items import BabelSpiderItem


class LemondeSpider(XMLFeedSpider):
    name = 'lemonde'
    allowed_domains = ['lemonde.fr']
    # TODO: fix hardcoding
    start_urls = ['http://www.lemonde.fr/international/rss_full.xml']
    iterator = 'iternodes'
    itertag = 'item'
    
    def parse_node(self, response, selector):
        item = BabelSpiderItem()
        url = selector.xpath('link/text()').extract_first()
        item['url'] = url
        item['category_id'] = 1
        item['media_id'] = 10
        item['published_at'] = selector.xpath('pubDate/text()').extract_first()
        request = scrapy.Request(url, callback=self.content_parse)
        request.meta['item'] = item
        yield request
    
    def content_parse(self, response):
        item = response.meta['item']
        title = response.xpath('//h1[@itemprop="Headline"]/text()').extract_first()
        content = ''.join(response.xpath('//div[@itemprop="articleBody"]/p/text() | //div[@itemprop="articleBody"]/p/a/text() | //div[@itemprop="articleBody"]/p/em/text()| //div[@itemprop="articleBody"]/p/em/a/text()').extract())
        item['title'] = title
        item['content'] = content
        if title and content:
            yield item
