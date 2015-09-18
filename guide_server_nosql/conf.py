'''
Application global settings

'''

__author__ = 'alex'
import os

STATIC_DIR = 'static'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

###############################
# Redis settings
REDIS = { 'db':1 }

################################
# Elasticsearch settings
ES_SETTINGS = [{'host': 'localhost', 'port': 9200}]
ES_INDEX = 'webguide'

