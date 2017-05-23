# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import XMLFeedSpider
from babel_spider.items import BabelSpiderItem


class ChosenSpider(XMLFeedSpider):
    name = 'chosen'
    allowed_domains = ['chosun.com']
    # TODO: fix hardcoding
    start_urls = ['http://www.chosun.com/site/data/rss/international.xml']
    iterator = 'iternodes'
    itertag = 'item'

    def parse_node(self, response, selector):
        item = BabelSpiderItem()
        url = selector.xpath('link/text()').extract_first()
        print(url)
        item['url'] = url
        item['category_id'] = 1
        item['media_id'] = 5
        item['published_at'] = selector.xpath('pubDate/text()').extract_first()
        request = scrapy.Request(url, callback=self.content_parse)
        request.meta['item'] = item
        yield request

    def content_parse(self, response):
        item = response.meta['item']
        # Not yet
        title = response.xpath('//h1[@id="news_title_text_id"]/text()').extract_first()
        content = ''.join(response.xpath('//div[@class="par"]/text()').extract())
        item['title'] = title
        item['content'] = content
        if title and content:
            yield item
