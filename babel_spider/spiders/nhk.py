# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import XMLFeedSpider
from babel_spider.items import BabelSpiderItem
from babel_spider.queries import get_urls_by_media_id, serch_null_image_urls, update_image_url
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class NhkSpider(XMLFeedSpider):
    name = 'nhk'
    allowed_domains = ['www3.nhk.or.jp']
    # TODO: fix hardcoding
    start_urls = ['http://www3.nhk.or.jp/rss/news/cat6.xml']
    iterator = 'iternodes'
    itertag = 'item'
    media_id = 1
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
        title = response.xpath('//span[@class="contentTitle"]/text()').extract_first()
        content = ''.join(response.xpath('//div[@id="news_textbody"]/text()').extract()) + ''.join(response.xpath('//div[@id="news_textmore"]/text()').extract())
        item['title'] = title
        item['content'] = content
        if title and content:
            yield item

    @classmethod
    def insert_image_urls(cls):
        query_results = serch_null_image_urls(cls.media_id)
        for article_id, url in query_results:
            print(url)
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text.encode(r.encoding), 'html.parser')
                    img = soup.find('div', id='news_image_div').find('img')
                    image_url = urljoin(r.url, img['src'])
                    print(image_url)
                    update_image_url(article_id, image_url)
            except Exception as e:
                print(e)
