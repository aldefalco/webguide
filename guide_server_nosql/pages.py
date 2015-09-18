'''
Simple application's pages

'''

__author__ = 'alex'

from flask import Blueprint, render_template, abort
from app import instance as app


page = Blueprint('page', __name__,
                        template_folder='templates')

@page.route('/')
def index():
    return render_template('index.html')


@page.route('/guide/<id>')
def get_guide(id):
    guide = {}
    if not guide:
        abort(404)
    return render_template('guide.html', guide = guide )


app.register_blueprint(page)