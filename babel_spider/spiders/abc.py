# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import XMLFeedSpider
from babel_spider.items import BabelSpiderItem


class AbcSpider(XMLFeedSpider):
    name = 'abc'
    allowed_domains = ['abcnews.com']
    # TODO: fix hardcoding
    start_urls = ['http://feeds.abcnews.com/abcnews/internationalheadlines']
    iterator = 'iternodes'
    itertag = 'item'

    def parse_node(self, response, selector):
        item = BabelSpiderItem()
        url = selector.xpath('link/text()').extract_first()
        item['url'] = url
        print(url)
        item['category_id'] = 1
        item['media_id'] = 3
        item['published_at'] = selector.xpath('pubDate/text()').extract_first()
        request = scrapy.Request(url, callback=self.content_parse)
        request.meta['item'] = item
        yield request

    def content_parse(self, response):
        item = response.meta['item']
        print(response)
        title = response.xpath('//header[@class="article-header"]/h1/text()').extract_first()
        print(title)
        content = ''.join(response.xpath('//p[@itemprop="articleBody"]/text()').extract())
        print(content)
        item['title'] = title
        item['content'] = content
        yield item