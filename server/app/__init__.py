# coding=utf-8
import logging
import os
import sys
import inspect

PRODUCTION = (os.getenv("FLASK_ENV") == 'production')
DEBUG = (os.getenv("FLASK_DEBUG") == 'True')
TESTING = (os.getenv("FLASK_TESTING") == 'True')

logging.basicConfig(
    format='%(asctime)s %(levelname)-7s %(module)s.%(funcName)s - %(message)s')
logging.getLogger().setLevel(logging.DEBUG if DEBUG and not TESTING else logging.INFO)
# logging.getLogger().setLevel(logging.DEBUG if DEBUG else logging.INFO)
logging.disable(logging.NOTSET)
logging.info('Loading %s, app version = %s', __name__, os.getenv('CURRENT_VERSION_ID'))

# ---
# fix import paths for internal imports
APP_ROOT = os.path.dirname(__file__)
if APP_ROOT not in sys.path:
    sys.path.insert(0, APP_ROOT)


from components import MyJsonEncoder


class MyConfig(object):
    RESTFUL_JSON = {
      'cls': MyJsonEncoder,
      'indent': 0 if PRODUCTION else 2
    }

    @staticmethod
    def init_app(app):
        import settings
        app.config.from_object(settings)
        config = "config.production" if PRODUCTION else "config.local"
        import importlib
        try:
            cfg = importlib.import_module(config)
            logging.info("Loaded %s" % config)
            app.config.from_object(cfg)
            # app.config['DEBUG'] = DEBUG
        except ImportError:
            logging.warning("Local settings module not found: %s", config)

# --- Initialize Flask

from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(MyConfig)
MyConfig.init_app(app)
api = Api(app)
CORS(app)

# --- Initialize Application

models = []

import components
import settings
import items
import tags
import categories
import estateplan
import smartimport

settings.init(app, api, models)
items.init(app, api, models)
tags.init(app, api, models)
categories.init(app, api, models)
estateplan.init(app, api, models)
smartimport.init(app, api, models)

if not TESTING:
    components.database_init(app, models)
    components.database_connect()

