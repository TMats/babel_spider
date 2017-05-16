# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import XMLFeedSpider
from babel_spider.items import BabelSpiderItem


class NewYorkTimesSpider(XMLFeedSpider):
    name = 'new_york_times'
    allowed_domains = ['rss.nytimes.com']
    # TODO: fix hardcoding
    start_urls = ['http://rss.nytimes.com/services/xml/rss/nyt/World.xml']
    iterator = 'iternodes'
    itertag = 'item'

    def parse_node(self, response, selector):
        item = BabelSpiderItem()
        url = selector.xpath('link/text()').extract_first()
        item['url'] = url
        print(url)
        item['category_id'] = 1
        item['media_id'] = 2
        item['published_at'] = selector.xpath('pubDate/text()').extract_first()
        request = scrapy.Request(url, callback=self.content_parse)
        request.meta['item'] = item
        yield request

    def content_parse(self, response):
        item = response.meta['item']
        title = response.xpath('//h1[@class="headline"]/text()').extract_first()
        content = ''.join(response.xpath('//p[@class="story-body-text story-content"]/text()').extract())
        item['title'] = title
        item['content'] = content
        print(title)
        print(content)
        yield item
