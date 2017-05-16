import psycopg2
from babel_spider.settings import STATIC_SETTEINGS


# Maybe this is no longer needed
def get_new_articles(media_id):
    connection = psycopg2.connect(host='localhost', database='babel', user='babel', password=STATIC_SETTEINGS['password'])
    cursor = connection.cursor()
    sql = """
        SELECT
            articles.id,
            articles.url
        FROM
            articles
        LEFT JOIN
            contents
        ON
            articles.id = contents.article_id
        WHERE
            articles.media_id = {}
            AND contents.content IS NULL
        """.format(str(media_id))
    # print(sql)
    cursor.execute(sql)
    query_result = dict(cursor.fetchall())
    return query_result
