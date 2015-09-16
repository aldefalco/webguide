from flask.ext.cache import Cache

__author__ = 'alex'

from flask import Flask
import conf

instance = Flask(__name__, static_url_path='', static_folder=conf.STATIC_DIR)

instance.config['SQLALCHEMY_DATABASE_URI'] = conf.DATABASE
#instance.config['SQLALCHEMY_ECHO'] = True

#cache = Cache(instance,config={'CACHE_TYPE': 'simple'})
cache = Cache(instance,config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://@localhost:6379/1' })
api_cache = Cache(instance,config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://@localhost:6379/2' })

