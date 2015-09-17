'''
Cache sync service
'''

__author__ = 'alex'
__version__  = '0.0.1'

import redis
import psycopg2
import psycopg2.extensions

from sync import loop
from updaters.redis import updater

channel_filters = {
    'guide': ['guide/%s',
              'guide/%s/*'],
    'page': ['guide/*/page/%s',
             ]
}

REDIS_PREFIX = "flask_cache_view//v1/"

if __name__ == '__main__':
    print "Cache sync v %s" % __version__
    r = redis.StrictRedis(db=2)
    connection = psycopg2.connect(database="webguide", user="dev", password="devpass")
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    loop.run(connection, updater(r, REDIS_PREFIX), channel_filters)
