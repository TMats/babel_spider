# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
from babel_spider.items import BabelSpiderItem
from babel_spider.settings import STATIC_SETTEINGS


class BabelSpiderPipeline(object):
    def __init__(self):
        self.connection = psycopg2.connect(host='localhost', database='babel', user='babel', password=STATIC_SETTEINGS['password'])
        self.cursor = self.connection.cursor()
    
    def process_item(self, item, spider):
        # check item type to decide which table to insert
        try:
            if type(item) is BabelSpiderItem:
                sql="""
                        INSERT INTO articles
                            (url, category_id, media_id, title, content, published_at)
                        VALUES
                            (%s, %s, %s, %s, %s, %s)
                    """
                self.cursor.execute(sql, (item.get('url'), item.get('category_id'), item.get('media_id'), item.get('title'), item.get('content'), item.get('published_at'),))
            self.connection.commit()
            self.cursor.fetchall()
        except psycopg2.DatabaseError as e:
            print("Error: %s" % e)
            self.connection.rollback()
        return item
