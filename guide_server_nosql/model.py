'''
Application model


Data have following schema:

set web:guides - all guide ids
json key web:guide:obj:<id> - content of guide
int key web:guide:seq - guide id sequence


int key web:page:seq - page id sequence
ordered set web:guide:pages:<guide_id> pages ids for the guide
json key web:page:obj:<id> - content of page

'''
import json
from utils import save_base64_image


__author__ = 'alex'
import redis
import conf


r = redis.StrictRedis(**conf.REDIS)

class ModelMeta(type):
    def __new__(cls, name, base, attrs):
        c = super(ModelMeta, cls).__new__(cls, name, base, attrs)
        c.objects = c()
        return c


class Guide(object):

    def get_all(self):
        return [ json.loads(r.get('web:guide:obj:%s' % id)) for id in r.smembers('web:guides')]

    def create(self, **kwargs):
        guide = {}
            #id = r.incr('web:guide:seq')
        with r.pipeline() as pipe:
            while True: #todo: change to counter
                try:
                    pipe.watch('web:guide:seq')
                    id = pipe.get('web:guide:seq')
                    id = int(0 if not id else id) + 1
                    pipe.multi()
                    pipe.set('web:guide:seq', id)
                    pipe.sadd('web:guides', id)
                    guide = {
                        'id': id,
                        'title': kwargs['title'],
                        'description': kwargs['description']
                    }
                    serial = json.dumps(guide)
                    pipe.set('web:guide:obj:%s' % id,  serial)
                    pipe.publish('web:guide:update', serial)
                    #todo: add publish signal for es
                    pipe.execute()
                    break
                except redis.WatchError:
                    continue
        return guide

    def delete_all(self):
        with r.pipeline() as pipe:
            while True: #todo: change it to counter
                try:
                    pipe.watch('web:guide:seq','web:guides')
                    ids = [ id for id in pipe.smembers('web:guides')]
                    pipe.multi()
                    for id in ids:
                        pipe.delete('web:guide:obj:%s' % id)
                        pipe.publish('web:guide:delete', id)
                    pipe.delete('web:guide:seq', 'web:page:seq', 'web:guides')

                    pipe.execute()
                    break
                except redis.WatchError:
                    continue

    def get(self, id):
        return json.loads(r.get('web:guide:obj:%s' % id))


    def update(self, **guide):
        serial = json.dumps(guide)
        r.set('web:guide:obj:%s' % id, serial )
        #todo: we need to add a transaction here
        r.publish('web:guide:update', serial)


    def delete(self, id):
        r.delete('web:guide:obj:%s' % id)
        r.publish('web:guide:delete', id)

    __metaclass__ = ModelMeta


class Page(object):

    def get_guide_pages(self, guide_id):
        return [ json.loads(r.get('web:page:obj:%s' % id)) for id in r.zrange('web:guide:pages:%s' % guide_id, 0, -1)]

    def create(self, guide_id, **args):
        page = {}
        with r.pipeline() as pipe:
            while True: #todo: change to counter
                try:
                    pipe.watch('web:page:seq')
                    id = pipe.get('web:page:seq')
                    id = int(0 if not id else id) + 1
                    pipe.multi()
                    pipe.set('web:page:seq', id)
                    pipe.zadd('web:guide:pages:%s' % guide_id, args['order'], id)
                    page = {
                        'id': id,
                        'comment': args['comment'],
                        'region': args['region'],
                        'order': args['order'],
                        'image': save_base64_image(args['src'])
                    }
                    pipe.set('web:page:obj:%s' % id, json.dumps(page) )
                    #todo: add publish signal for es
                    pipe.execute()
                    break
                except redis.WatchError:
                    continue
        return page

    def delete_guide_pages(self, guide_id):
        page_set = 'web:guide:pages:%s' % guide_id
        with r.pipeline() as pipe:
            while True: #todo: change it to counter
                try:
                    pipe.watch(page_set)
                    ids = [ id for id in pipe.smembers(page_set)]
                    pipe.multi()
                    for id in ids:
                        pipe.delete('web:page:obj:%s' % id)
                    pipe.delete(page_set)
                    pipe.execute()
                    break
                except redis.WatchError:
                    continue

    def get(self, id):
        return json.loads(r.get('web:page:obj:%s' % id))

    def update(self, **args):
        r.set('web:page:obj:%s' % id, json.dumps(args) )
        return args

    def delete(self, id):
        r.delete('web:page:obj:%s' % id)


    __metaclass__ = ModelMeta



