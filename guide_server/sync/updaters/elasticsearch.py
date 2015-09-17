'''
Elastic search updater
'''


__author__ = 'alex'

import json
import logging
from sqlalchemy.ext.declarative import DeclarativeMeta

log = logging.getLogger('sync.updaters.elasticsearch')

#TODO: move it form this module
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

def updater(es, index):
    def factory(channel, params):
        def update(id):
            try:
                for type in params:
                    instance = type.query.get(id)
                    doc = json.dumps(instance, cls=AlchemyEncoder)
                    es.index(index=index, doc_type=channel, id=id, body=doc)
            except Exception as e:
                log.error(e.message)
        return update
    return factory
