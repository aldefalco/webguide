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

__author__ = 'alex'

import json
from utils import save_base64_image

import redis
import conf

GUIDE_OBJ_KEY = 'web:guide:obj:%s'
GUIDE_SET_KEY = 'web:guides'
GUIDE_SEQ_KEY = 'web:guide:seq'

GUIDE_UPDATE_CH = 'web:guide:update'
GUIDE_DELETE_CH = 'web:guide:delete'

PAGE_OBJ_KEY =  'web:page:obj:%s'
PAGE_SEQ_KEY = 'web:page:seq'
PAGE_SET_KEY = 'web:guide:pages:%s'

r = redis.StrictRedis(**conf.REDIS)

class ModelMeta(type):
    def __new__(cls, name, base, attrs):
        c = super(ModelMeta, cls).__new__(cls, name, base, attrs)
        c.objects = c()
        return c


class Guide(object):

    def get_all(self):
        return [ json.loads(r.get(GUIDE_OBJ_KEY % id)) for id in r.smembers(GUIDE_SET_KEY)]

    def create(self, **kwargs):
        guide = kwargs
        #id = r.incr('web:guide:seq')
        with r.pipeline() as pipe:
            while True: #todo: change to counter
                try:
                    pipe.watch(GUIDE_SEQ_KEY)
                    id = pipe.get(GUIDE_SEQ_KEY)
                    guide['id'] = int(0 if not id else id) + 1
                    pipe.multi()
                    pipe.set(GUIDE_SEQ_KEY, id)
                    pipe.sadd(GUIDE_SET_KEY, id)
                    serial = json.dumps(guide)
                    pipe.set(GUIDE_OBJ_KEY % id,  serial)
                    pipe.publish(GUIDE_UPDATE_CH, serial)
                    pipe.execute()
                    break
                except redis.WatchError:
                    continue
        return guide

    def delete_all(self):
        with r.pipeline() as pipe:
            while True: #todo: change it to counter
                try:
                    pipe.watch(GUIDE_SEQ_KEY,GUIDE_SET_KEY)
                    ids = [ id for id in pipe.smembers(GUIDE_SEQ_KEY)]
                    pipe.multi()
                    for id in ids:
                        pipe.delete(GUIDE_OBJ_KEY % id)
                        pipe.publish(GUIDE_DELETE_CH, id)
                    pipe.delete(GUIDE_SEQ_KEY, PAGE_SEQ_KEY, GUIDE_SET_KEY)

                    pipe.execute()
                    break
                except redis.WatchError:
                    continue

    def get(self, id):
        return json.loads(r.get(GUIDE_OBJ_KEY % id))


    def update(self, **guide):
        serial = json.dumps(guide)
        r.set(GUIDE_OBJ_KEY % id, serial )
        #todo: we need to add a transaction here
        r.publish(GUIDE_UPDATE_CH, serial)


    def delete(self, id):
        r.delete(GUIDE_OBJ_KEY % id)
        r.publish(GUIDE_OBJ_KEY, id)

    __metaclass__ = ModelMeta


class Page(object):

    def get_guide_pages(self, guide_id):
        return [ json.loads(r.get(PAGE_OBJ_KEY % id)) for id in r.zrange(PAGE_SET_KEY % guide_id, 0, -1)]

    def create(self, guide_id, **args):
        page = args
        image = save_base64_image(page['src'])
        del page['src']
        with r.pipeline() as pipe:
            while True: #todo: change to counter
                try:
                    pipe.watch(PAGE_SEQ_KEY)
                    id = pipe.get(PAGE_SEQ_KEY)
                    page['id'] = int(0 if not id else id) + 1
                    page['image'] = image
                    pipe.multi()
                    pipe.set(PAGE_SEQ_KEY, id)
                    pipe.zadd(PAGE_SET_KEY % guide_id, args['order'], id)
                    pipe.set(PAGE_OBJ_KEY % id, json.dumps(page) )
                    #todo: add publish signal for es
                    pipe.execute()
                    break
                except redis.WatchError:
                    continue
        return page

    def delete_guide_pages(self, guide_id):
        page_set = PAGE_SET_KEY % guide_id
        with r.pipeline() as pipe:
            while True: #todo: change it to counter
                try:
                    pipe.watch(page_set)
                    ids = [ id for id in pipe.smembers(page_set)]
                    pipe.multi()
                    for id in ids:
                        pipe.delete(PAGE_OBJ_KEY % id)
                    pipe.delete(page_set)
                    pipe.execute()
                    break
                except redis.WatchError:
                    continue

    def get(self, id):
        return json.loads(r.get(PAGE_OBJ_KEY % id))

    def update(self, **args):
        r.set(PAGE_OBJ_KEY % id, json.dumps(args) )
        return args

    def delete(self, id):
        r.delete(PAGE_OBJ_KEY % id)


    __metaclass__ = ModelMeta



