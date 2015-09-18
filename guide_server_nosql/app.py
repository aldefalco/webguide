'''
Flask application instance

'''

__author__ = 'alex'

from flask.ext.cache import Cache
from flask import Flask
import conf

instance = Flask(__name__, static_url_path='', static_folder=conf.STATIC_DIR)

#instance.config['SQLALCHEMY_DATABASE_URI'] = conf.DATABASE

#cache = Cache(instance,config=conf.PAGE_CACHE)
#api_cache = Cache(instance,config=conf.API_CACHE)

