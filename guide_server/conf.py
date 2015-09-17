'''
Application global settings

'''

__author__ = 'alex'
import os

STATIC_DIR = 'static'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

###############################
# DB settings
#DATABASE = 'sqlite:////tmp/test.db'
DATABASE = 'postgresql://dev:devpass@localhost:5432/webguide'

################################
# Elasticsearch settings
ES_SETTINGS = [{'host': 'localhost', 'port': 9200}]
ES_INDEX = 'webguide'

################################
# Cache settings
PAGE_CACHE = {'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://@localhost:6379/1' }
API_CACHE = {'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://@localhost:6379/2' }
