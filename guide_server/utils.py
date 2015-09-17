'''
Utils functions for flask api


'''
import base64
from io import BytesIO
import uuid
from PIL import Image

from flask.ext.restful import reqparse
import conf

__author__ = 'alex'

def declare_api(api, route, schema):
    def reg(cls):
        api.add_resource(cls, route)
        cls.parser = reqparse.RequestParser()
        for n, t in schema:
            cls.parser.add_argument(n, type=t)
    return reg


def save_base64_image(src):
    id = uuid.uuid1()
    name = conf.PROJECT_DIR + '/' +  conf.STATIC_DIR +  "/images/%s.png" % id
    i = src.find(',')
    base64_src = src[i + 1:]
    base64_src + '=' * (4 - len(base64_src) % 4)
    image = Image.open(BytesIO(base64.b64decode(base64_src)))
    image.save(name, 'PNG')
    return "images/%s.png" % id