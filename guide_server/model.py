"""
This is the application model based on SQLAlchemy ORM

Simple model's tests:

>>> db.drop_all()
>>> db.create_all()
>>> g = Guide('The How-to instruction for the video making service', 'This instruction helps you to make a video for the Yourtube service')
>>> p1 = Page(g, 1, 'First page', 'p1.png', '{}')
>>> p2 = Page(g, 2, 'Second page', 'p2.png', '{}')
>>> db.session.add(g)
>>> db.session.add(p1)
>>> db.session.add(p2)
>>> db.session.commit()
>>> Guide.query.all()[0].title
u'The How-to instruction for the video making service'
>>> g.pages.all()
[<Page 1>, <Page 2>]
>>> g.pages.all()[0].comment
u'First page'
"""

__author__ = 'alex'

from flask.ext.sqlalchemy  import SQLAlchemy

from app import instance as app

db = SQLAlchemy(app)

class Guide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False)
    description = db.Column(db.String(512), unique=False)

    def __init__(self, title, description):
        self.title = title
        self.description  = description

    def __repr__(self):
        return '<Guide %r>' % self.title


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    guide_id = db.Column(db.Integer, db.ForeignKey('guide.id'))
    guide = db.relationship('Guide',
        backref=db.backref('pages', lazy='dynamic'))
    comment = db.Column(db.String(512), unique=False)
    image = db.Column(db.String(512), unique=False)
    region = db.Column(db.String(256), unique=False)

    def __init__(self, guide, order_id, comment, image, region):
        self.guide = guide
        self.order_id = order_id
        self.image = image
        self.comment  = comment
        self.region = region

    def __repr__(self):
        return '<Page %r>' % self.id


if __name__ == '__main__':
    import doctest
    doctest.testmod()