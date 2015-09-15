__author__ = 'alex'

from flask import Blueprint, render_template
from app import instance as app, cache
import model

page = Blueprint('page', __name__,
                        template_folder='templates')

@page.route('/')
def index():
    return render_template('index.html')


@page.route('/guide/<id>')
@cache.cached()
def get_guide(id):
    guide = model.Guide.query.get(id)
    return render_template('guide.html', guide = guide )


app.register_blueprint(page)