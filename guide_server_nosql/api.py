# -*- encoding: utf-8 -*-
'''
Web guide api implementation


'''
import json

__author__ = 'alex'

import traceback
import logging

from flask.ext import restful
from flask.ext.restful import marshal, fields, Resource
from utils import declare_api, save_base64_image

from app import instance as app

import conf
import redis

from elasticsearch import Elasticsearch

es = Elasticsearch(conf.ES_SETTINGS)
r = redis.StrictRedis(**conf.REDIS)

api = restful.Api(app)
log = logging.getLogger('api')

@declare_api(api, '/ping', [] )
class Ping(Resource):
    def get(self):
        return { 'result' : 'pong'}

@declare_api(api, '/version', [] )
class Version(Resource):
    def get(self):
        return { 'version' : 'v1'}



@declare_api(api, '/v1/guide',
             [('title', str), ('description', str)])
class GuideListApi(Resource):

    def get(self):
        try:
            guides = [ json.loads(r.get('web::guide::obj::%s' % id)) for id in r.smembers('web::guides')]
            return guides
        except Exception as e:
            log.exception(e.message)
            return { 'error': e.message }, 501

    def post(self):
        args = self.parser.parse_args()
        try:
            guide = {}
            #id = r.incr('web::guide::seq')
            with r.pipeline() as pipe:
                while True: #todo: change to counter
                    try:
                        pipe.watch('web::guide::seq')
                        id = pipe.get('web::guide::seq')
                        id = int(0 if not id else id) + 1
                        pipe.multi()
                        pipe.set('web::guide::seq', id)
                        pipe.sadd('web::guides', id)
                        guide = {
                            'id': id,
                            'title': args['title'],
                            'description': args['description']
                        }
                        serial = json.dumps(guide)
                        pipe.set('web::guide::obj::%s' % id,  serial)
                        pipe.publish('web::guide::update', serial)
                        #todo: add publish signal for es
                        pipe.execute()
                        break
                    except redis.WatchError:
                        traceback.print_exc()
                        continue
            return guide, 201
        except Exception as e:
            log.exception(e.message)
            traceback.print_exc()
            return { 'error': e.message }, 501

    def delete(self):
        try:
            with r.pipeline() as pipe:
                while True: #todo: change it to counter
                    try:
                        pipe.watch('web::guide::seq','web::guides')
                        ids = [ id for id in pipe.smembers('web::guides')]
                        pipe.multi()
                        for id in ids:
                            pipe.delete('web::guide::obj::%s' % id)
                            pipe.publish('web::guide::delete', id)
                        pipe.delete('web::guide::seq', 'web::page::seq', 'web::guides')

                        pipe.execute()
                        break
                    except redis.WatchError:
                        continue
            return {}, 204
        except Exception as e:
            log.exception(e.message)
            return { 'error': e.message }, 501


@declare_api(api, '/v1/guide/<int:id>',
             [('title', str), ('description', str)] )
class GuideApi(Resource):

    def get(self, id):
        try:
            return json.loads(r.get('web::guide::obj::%s' % id))
        except Exception as e:
            log.exception(e.message)
            return { 'error': e.message }, 501

    def put(self, id):
        args = self.parser.parse_args()
        try:
            guide = {
                'id': id,
                'title': args['title'],
                'description': args['description']
            }
            serial = json.dumps(guide)
            r.set('web::guide::obj::%s' % id, serial )
            #todo: we need to add a transaction here
            r.publish('web::guide::update', serial)
            return guide, 201
        except Exception as e:
            log.exception(e.message)
            traceback.print_exc()
            return { 'error': e.message }, 501

    def delete(self, id):
        try:
            r.delete('web::guide::obj::%s' % id)
            r.publish('web::guide::delete', id)
            return {  }, 204
        except Exception as e:
            log.exception(e.message)
            return { 'error': e.message }, 501




@declare_api(api, '/v1/guide/<int:guide_id>/page',
             [('src', str),('comment', str),('region', str), ('order', int)] )
class GuidePageListApi(Resource):

    def get(self, guide_id):
        try:
            pages = [ json.loads(r.get('web::page::obj::%s' % id)) for id in r.zrange('web::guide::pages::%s' % guide_id, 0, -1)]
            return pages
        except Exception as e:
            log.exception(e.message)
            return { 'error': e.message }, 501


    def post(self, guide_id):
        args = self.parser.parse_args()
        try:
            page = {}
            with r.pipeline() as pipe:
                while True: #todo: change to counter
                    try:
                        pipe.watch('web::page::seq')
                        id = pipe.get('web::page::seq')
                        id = int(0 if not id else id) + 1
                        pipe.multi()
                        pipe.set('web::page::seq', id)
                        pipe.zadd('web::guide::pages::%s' % guide_id, args['order'], id)
                        page = {
                            'id': id,
                            'comment': args['comment'],
                            'region': args['region'],
                            'order': args['order'],
                            'image': save_base64_image(args['src'])
                        }
                        pipe.set('web::page::obj::%s' % id, json.dumps(page) )
                        #todo: add publish signal for es
                        pipe.execute()
                        break
                    except redis.WatchError:
                        traceback.print_exc()
                        continue
            return page, 201
        except Exception as e:
            log.exception(e.message)
            traceback.print_exc()
            return { 'error': e.message }, 501


    def delete(self, guide_id):
        try:
            page_set = 'web::guide::pages::%s' % guide_id
            with r.pipeline() as pipe:
                while True: #todo: change it to counter
                    try:
                        pipe.watch(page_set)
                        ids = [ id for id in pipe.smembers(page_set)]
                        pipe.multi()
                        for id in ids:
                            pipe.delete('web::page::obj::%s' % id)
                        pipe.delete(page_set)
                        pipe.execute()
                        break
                    except redis.WatchError:
                        continue
            return {}, 204
        except Exception as e:
            log.exception(e.message)
            return { 'error': e.message }, 501



@declare_api(api, '/v1/guide/<int:guide_id>/page/<int:id>',
             [('src', str),('comment', str),('region', str)])
class GuidePageApi(Resource):

    def get(self, guide_id, id):
        try:
            return json.loads(r.get('web::page::obj::%s' % id))
        except Exception as e:
            log.exception(e.message)
            return { 'error': e.message }, 501

    def put(self, guide_id, id):
        args = self.parser.parse_args()
        try:
            page = {
                'id': id,
                'title': args['title'],
                'description': args['description']
            }
            r.set('web::page::obj::%s' % id, json.dumps(page) )
            return page, 201
        except Exception as e:
            log.exception(e.message)
            traceback.print_exc()
            return { 'error': e.message }, 501

    def delete(self, guide_id, id):
        try:
            r.delete('web::page::obj::%s' % id)
            return {  }, 204
        except Exception as e:
            log.exception(e.message)
            return { 'error': e.message }, 501


@declare_api(api, '/v1/search/autocomplete',(('prefix', str),))
class AutocompleteApi(Resource):

    def post(self):
        args = self.parser.parse_args()
        try:
            prefix = args['prefix']
            return es.search(index=conf.ES_INDEX, body={"query": {"prefix" : { "title" : prefix }}})
        except Exception as e:
            log.exception(e.message)
            traceback.print_exc()
            return { 'error': e.message }, 501

@declare_api(api, '/v1/search',(('query', str),))
class SearchApi(Resource):

    def post(self):
        args = self.parser.parse_args()
        try:
            query = args['query']
            return es.search(index=conf.ES_INDEX, body=
            { "query": { "multi_match" : {  "query": query,  "type":"most_fields", "fields": [ "title^10", "description" ] } } } )
        except Exception as e:
            log.exception(e.message)
            traceback.print_exc()
            return { 'error': e.message }, 501

@app.after_request
def fix_headers_for_CORS(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response