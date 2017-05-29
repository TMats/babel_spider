import psycopg2
from babel_spider.settings import STATIC_SETTEINGS


# Maybe this is no longer needed
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
    except psycopg2.DatabaseError as e:
        connection.rollback()
    query_results = [result[0] for result in query_results]
    return query_results
