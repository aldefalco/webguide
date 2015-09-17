# -*- encoding: utf-8 -*-
'''
Web guide api implementation


'''

__author__ = 'alex'

import traceback

from flask.ext import restful
from flask.ext.restful import marshal, fields, Resource
from utils import declare_api, save_base64_image

from app import instance as app, api_cache
from model import db, Guide, Page

import conf

from elasticsearch import Elasticsearch

es = Elasticsearch(conf.ES_SETTINGS)


api = restful.Api(app)

@declare_api(api, '/ping', [] )
class Ping(Resource):
    def get(self):
        return { 'result' : 'pong'}

@declare_api(api, '/version', [] )
class Version(Resource):
    def get(self):
        return { 'version' : 'v1'}

guide_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String
    }


@declare_api(api, '/v1/guide',
             [('title', str), ('description', str)])
class GuideListApi(Resource):

    @api_cache.cached()
    def get(self):
        try:
            all_guides = Guide.query.all()
            return marshal(all_guides, guide_fields)
        except Exception as e:
            return { 'error': e.message }, 501

    def post(self):
        args = self.parser.parse_args()
        try:
            guide = Guide(**args)
            db.session.add(guide)
            #db.session.execute("NOTIFY guide, '%s'" % guide.id)
            db.session.commit()
            return marshal(guide, guide_fields), 201
        except Exception as e:
            traceback.print_exc()
            return { 'error': e.message }, 501

    def delete(self):
        try:
            Guide.query.delete()
            db.session.commit()
            return {}, 204
        except Exception as e:
            return { 'error': e.message }, 501


@declare_api(api, '/v1/guide/<int:id>',
             [('title', str), ('description', str)] )
class GuideApi(Resource):

    @api_cache.cached()
    def get(self, id):
        try:
            guide = Guide.query.get(id)
            return marshal(guide, guide_fields)
        except Exception as e:
            return { 'error': e.message }, 501

    def put(self, id):
        args = self.parser.parse_args()
        try:
            db.session.query(Guide).filter_by(id=id).update(args)
            #db.session.execute("NOTIFY guide, '%s'" % id)
            db.session.commit()
            guide = Guide.query.get(id)
            return marshal(guide, guide_fields), 201
        except Exception as e:
            traceback.print_exc()
            return { 'error': e.message }, 501

    def delete(self, id):
        try:
            guide = Guide.query.get(id)
            db.session.delete(guide)
            db.session.execute("SELECT setval('public.guide_id_seq', 1, true);")
            db.session.commit()
            return {  }, 204
        except Exception as e:
            return { 'error': e.message }, 501

pages_fields = {
    'id': fields.Integer,
    'image': fields.String,
    }


@declare_api(api, '/v1/guide/<int:guide_id>/page',
             [('src', str),('comment', str),('region', str), ('order', int)] )
class GuidePageListApi(Resource):

    @api_cache.cached()
    def get(self, guide_id):
        try:
            guide = Guide.query.get(guide_id)
            return marshal(guide.pages.all(), pages_fields)
        except Exception as e:
            return { 'error': e.message }, 501


    def post(self, guide_id):
        args = self.parser.parse_args()
        try:
            guide = Guide.query.get(guide_id)
            order = args['order'] if args['order'] else guide.pages.count()
            page = Page(guide, order, args['comment'], save_base64_image(args['src']), args['region'] )
            db.session.add(page)
            db.session.commit()
            return marshal(page, pages_fields), 201
        except Exception as e:
            traceback.print_exc()
            return { 'error': e.message }, 501


    def delete(self, guide_id):
        try:
            guide = Guide.query.get(guide_id)
            guide.pages.delete()
            db.session.commit()
            return {  }, 204
        except Exception as e:
            return { 'error': e.message }, 501


page_fields = {
    'id': fields.Integer,
    'image': fields.String,
    'region': fields.String,
    'comment': fields.String
    }


@declare_api(api, '/v1/guide/<int:guide_id>/page/<int:id>',
             [('src', str),('comment', str),('region', str)])
class GuidePageApi(Resource):

    @api_cache.cached()
    def get(self, guide_id, id):
        try:
            guide = Guide.query.get(guide_id)
            page = guide.pages.filter_by(id=id).first()
            return marshal(page, page_fields)
        except Exception as e:
            return { 'error': e.message }, 501

    def put(self, guide_id, id):
        args = self.parser.parse_args()
        try:
            guide = Guide.query.get(guide_id)
            page = guide.pages.filter_by(id=id).first()
            if args['src']:
                page.image = save_base64_image(args['src'])
            if args['comment']:
                page.comment = args['comment']
            if args['region']:
                page.comment = args['region']
            db.session.commit()
            return marshal(page, page_fields), 201
        except Exception as e:
            traceback.print_exc()
            return { 'error': e.message }, 501

    def delete(self, guide_id, id):
        try:
            guide = Guide.query.get(guide_id)
            page = guide.pages.filter_by(id=id).first()
            db.session.delete(page)
            db.session.commit()
            return {  }, 204
        except Exception as e:
            return { 'error': e.message }, 501


@declare_api(api, '/v1/search/autocomplete',(('prefix', str),))
class AutocompleteApi(Resource):

    def post(self):
        args = self.parser.parse_args()
        try:
            prefix = args['prefix']
            return es.search(index=conf.ES_INDEX, body={"query": {"prefix" : { "title" : prefix }}})
        except Exception as e:
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
            traceback.print_exc()
            return { 'error': e.message }, 501

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response