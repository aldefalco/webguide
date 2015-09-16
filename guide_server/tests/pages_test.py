__author__ = 'alex'

import unittest
import conf
from flask.ext.cache import Cache

conf.DATABASE = 'sqlite:///:memory:'

from app import instance as app

app.cache = Cache(app,config={'CACHE_TYPE': 'null' })

import pages
import api
import model

class PagesTest(unittest.TestCase):

    def setUp(self):
        model.db.drop_all()
        model.db.create_all()

    def tearDown(self):
        pass

    def test_index(self):
        tester = app.test_client()
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_no_guide(self):
        tester = app.test_client()
        response = tester.get('/guide/000', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    def test_guide(self):
        g = model.Guide('title 1', 'description 1')
        model.db.session.add(g)
        model.db.session.commit()
        tester = app.test_client()
        response = tester.get('/guide/%s' % g.id, content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn('title 1', response.data)

if __name__ == '__main__':
    unittest.main()
