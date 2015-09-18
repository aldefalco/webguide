'''
Redis updater
'''
__author__ = 'alex'

import logging

log = logging.getLogger('sync.updaters.redis')

def updater(cache, prefix):
    def factory(channel, params):
        def update(id):
            try:
                for f in params:
                    keys = cache.keys(prefix + f % id)
                    for key in keys:
                        cache.delete(key)
            except Exception as e:
                log.error(e.message)
        return update
    return factory