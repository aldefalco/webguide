import os
__author__ = 'alex'

STATIC_DIR = 'static'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

#DATABASE = 'sqlite:////tmp/test.db'
DATABASE = 'postgresql://dev:devpass@localhost:5432/webguide'