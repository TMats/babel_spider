# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import XMLFeedSpider
from babel_spider.items import BabelSpiderItem


class LefigaroSpider(XMLFeedSpider):
    name = 'lefigaro'
    allowed_domains = ['lefigaro.fr']
    # TODO: fix hardcoding
    start_urls = ['http://www.lefigaro.fr/rss/figaro_international.xml']
    iterator = 'iternodes'
    itertag = 'item'
    
    def parse_node(self, response, selector):
        item = BabelSpiderItem()
        url = selector.xpath('link/text()').extract_first()
        item['url'] = url
        item['category_id'] = 1
        item['media_id'] = 9
        item['published_at'] = selector.xpath('pubDate/text()').extract_first()
        request = scrapy.Request(url, callback=self.content_parse)
        request.meta['item'] = item
        yield request
    
    def content_parse(self, response):
        item = response.meta['item']
        title = response.xpath('//h1[@itemprop="headline"]/text()').extract_first()
        content = ''.join(response.xpath('//p[@itemprop="about"]/text() | //div[@itemprop="articleBody"]/p/text()| //div[@itemprop="articleBody"]/p/a/text()').extract())
        item['title'] = title
        item['content'] = content
        if title and content:
            yield item
