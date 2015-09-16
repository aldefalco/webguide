'''
Search sync service

'''

__author__ = 'alex'
__version__  = '0.0.1'


import psycopg2
import psycopg2.extensions
from elasticsearch import Elasticsearch

import model


from sync import loop
from updaters.elasticsearch import updater

channel_params = {
    'guide': (model.Guide,),
    'page': (model.Page,),
}


if __name__ == '__main__':
    print "Search sync v %s" % __version__

    connection = psycopg2.connect(database="webguide", user="dev", password="devpass")
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    loop.run(connection, updater(es, 'webguide'), channel_params)
