import psycopg2
from babel_spider.settings import STATIC_SETTEINGS
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def get_urls_by_media_id(media_id):
    connection = psycopg2.connect(host='localhost', database='babel', user='babel', password=STATIC_SETTEINGS['password'])
    cursor = connection.cursor()
    sql = """
        SELECT
            articles.url
        FROM
            articles
        WHERE
            articles.media_id = {}
        """.format(str(media_id))
    try:
        cursor.execute(sql)
        query_results = cursor.fetchall()
        query_results = [result[0] for result in query_results]
        return query_results
    except psycopg2.DatabaseError as e:
        connection.rollback()


def serch_null_image_urls(media_id):
    connection = psycopg2.connect(host='localhost', database='babel', user='babel', password=STATIC_SETTEINGS['password'])
    cursor = connection.cursor()
    sql = """
        SELECT
            id,
            articles.url
        FROM
            articles
        WHERE
            articles.media_id = {}
            AND image_url IS NULL
        """.format(str(media_id))
    try:
        cursor.execute(sql)
        query_results = cursor.fetchall()
        return query_results
    except psycopg2.DatabaseError as e:
        connection.rollback()


def update_image_url(article_id, image_url):
    connection = psycopg2.connect(host='localhost', database='babel', user='babel', password=STATIC_SETTEINGS['password'])
    cursor = connection.cursor()
    sql = """
        UPDATE
            articles
        SET
            image_url = '{}'
        WHERE
            id = {}
        """.format(image_url, str(article_id))
    try:
        print(sql)
        cursor.execute(sql)
        connection.commit()
    except psycopg2.DatabaseError as e:
        print(e)
        connection.rollback()


# def insert_image_urls(media_id):
#     query_results = serch_null_image_urls(media_id)
#     for article_id, url in query_results[0:1]:
#         r = requests.get(url)
#         if r.status_code == 200:
#             soup = BeautifulSoup(r.text.encode(r.encoding), 'html.parser')
#             img = soup.find('div', id='news_image_div').find('img')
#             if img:
#                 image_url = urljoin(r.url, img['src'])
#                 print(image_url)

