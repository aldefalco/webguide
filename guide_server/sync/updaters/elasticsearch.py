'''

'''

__author__ = 'alex'

import json
import logging

log = logging.getLogger('sync.updaters.elasticsearch')

def updater(es, index):
    def factory(channel, params):
        def update(id):
            try:
                for type in params:
                    instance = type.query.get(id)
                    doc = json.dumps(instance)
                    es.index(index=index, doc_type=channel, id=id, body=doc)
            except Exception as e:
                log.error(e.message)
        return update
    return factory
