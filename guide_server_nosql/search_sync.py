'''
Simple search sync service

'''
import json

__author__ = 'alex'
__version__  = '0.0.2'


from elasticsearch import Elasticsearch
import redis

import conf

r = redis.StrictRedis(**conf.REDIS)

if __name__ == '__main__':
    print "Search sync v %s for noSQL solution" % __version__
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    subscriber = r.pubsub()
    subscriber.subscribe(['web::guide::delete', 'web::guide::update'])

    for message in subscriber.listen():
        try:
            if message['channel'] == 'web::guide::update':
                print 'update', message['data']
                obj = json.loads(message['data']) #todo: I think we need to use id and a comma ',' separator in protocol instead of json loading
                es.index(index='webguide', doc_type='guide', id=obj['id'], body=message['data'])
            if message['channel'] == 'web::guide::delete':
                print 'delete', message['data']
                es.delete(index='webguide', doc_type='guide', id=int(message['data']))
        except Exception as e:
            print e.message





