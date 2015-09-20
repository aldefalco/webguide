# -*- encoding: utf-8 -*-
'''
Web guide api implementation


'''
import json

__author__ = 'alex'

import traceback
import logging

from flask.ext import restful
from flask.ext.restful import Resource
from utils import declare_api

from app import instance as app
from model import Guide, Page

import conf


from elasticsearch import Elasticsearch

es = Elasticsearch(conf.ES_SETTINGS)


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
             [
                 ('title', str),
                 ('description', str)
             ])
class GuideListApi(Resource):

    def get(self):
        try:
            return Guide.objects.get_all()
        except Exception as e:
            log.exception(e.message)
            return { 'error': e.message }, 501

    def post(self):
        args = self.parser.parse_args()
        try:
            return Guide.objects.create(**args), 201
        except Exception as e:
            log.exception(e.message)
            traceback.print_exc()
            return { 'error': e.message }, 501

    def delete(self):
        try:
            Guide.objects.delete_all()
            return {}, 204
        except Exception as e:
            log.exception(e.message)
            return { 'error': e.message }, 501


@declare_api(api, '/v1/guide/<int:id>',
             [
                 ('title', str),
                 ('description', str)
             ])
class GuideApi(Resource):

    def get(self, id):
        try:
            return Guide.objects.get(id)
        except Exception as e:
            log.exception(e.message)
            return { 'error': e.message }, 501

    def put(self, id):
        args = self.parser.parse_args()
        try:
            return Guide.objects.update(**args), 201
        except Exception as e:
            log.exception(e.message)
            traceback.print_exc()
            return { 'error': e.message }, 501

    def delete(self, id):
        try:
            Guide.objects.delete(id)
            return {  }, 204
        except Exception as e:
            log.exception(e.message)
            return { 'error': e.message }, 501


@declare_api(api, '/v1/guide/<int:guide_id>/page',
             [
                 ('src', str),
                 ('comment', str),
                 ('region', str),
                 ('order', int)
             ])
class GuidePageListApi(Resource):

    def get(self, guide_id):
        try:
            return Page.objects.get_guide_pages(guide_id)
        except Exception as e:
            log.exception(e.message)
            return { 'error': e.message }, 501


    def post(self, guide_id):
        args = self.parser.parse_args()
        try:
            return Page.objects.create(guide_id, **args), 201
        except Exception as e:
            log.exception(e.message)
            traceback.print_exc()
            return { 'error': e.message }, 501


    def delete(self, guide_id):
        try:
            Page.objects.delete_guide_pages(guide_id)
            return {}, 204
        except Exception as e:
            log.exception(e.message)
            return { 'error': e.message }, 501



@declare_api(api, '/v1/guide/<int:guide_id>/page/<int:id>',
             [
                 ('src', str),
                 ('comment', str),
                 ('region', str)
             ])
class GuidePageApi(Resource):

    def get(self, guide_id, id):
        try:
            return Page.objects.get(id)
        except Exception as e:
            log.exception(e.message)
            return { 'error': e.message }, 501

    def put(self, guide_id, id):
        args = self.parser.parse_args()
        try:
            return Page.objects.update(**args), 201
        except Exception as e:
            log.exception(e.message)
            traceback.print_exc()
            return { 'error': e.message }, 501

    def delete(self, guide_id, id):
        try:
            Page.objects.delete(id)
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