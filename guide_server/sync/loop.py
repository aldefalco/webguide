'''
Cache sync module

'''

__author__ = 'alex'
__version__  = '0.0.1'

import select
import logging

log = logging.getLogger('sync.loop')

def run(db, update_factory, channel_params):
    cursor = db.cursor()
    updaters = { c: update_factory(c,p) for c,p in channel_params.iteritems() }

    for key in updaters.keys():
        cursor.execute("LISTEN %s;" % key)

    #TODO: remove it
    print "Waiting for notifications on channels"
    while 1:
        if not select.select([db],[],[],5) == ([],[],[]):
            db.poll()
            while db.notifies:
                notify = db.notifies.pop(0)
                id = int(notify.payload)
                update = updaters[notify.channel]
                update(id)
                #TODO: remove it
                print "Got NOTIFY:", notify.pid, notify.channel, notify.payload
        else:
            pass

