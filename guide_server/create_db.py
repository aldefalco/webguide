'''
Create DB from model

'''
__author__ = 'alex'

import traceback
import model


if __name__ == '__main__':
    print 'Recreate all database objects from model'
    try:
        model.db.drop_all()
        model.db.create_all()
        print 'Done.'
    except Exception as e:
        print 'There is some problems with db'
        traceback.print_exc()

