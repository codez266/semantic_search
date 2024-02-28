import os
from logging.config import dictConfig
from semantic_search_app import search
# from semantic_search_app.db import get_db
# from semantic_search_app.models import CreateparticipantParticipant, database
from flask import Flask, session, g
from semantic_search_app.defaultsettings import config
from semantic_search_app.config import CONFIG
from playhouse.flask_utils import FlaskDB
from semantic_search_app.lib import get_corpus
from sentence_transformers import SentenceTransformer
from peewee import *
import pickle
import pandas as pd
import pdb

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    DATABASE = {
        'name': 'semantic_search',
        'engine': 'playhouse.pool.PooledMySQLDatabase',
        # 'user': CONFIG.get('db', 'user'),
        'max_connections': 32,
        'stale_timeout': 600,
        # 'password': CONFIG.get('db', 'password'),
        # 'host': CONFIG.get('db', 'host'),
        'charset': 'utf8',
        'sql_mode': 'PIPES_AS_CONCAT',
        'use_unicode': True,
    }

    #db_wrapper = FlaskDB(app, database)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(config['production'])
    else:
        # load the test config if passed in
        app.config.from_object(test_config)

    # from . import db
    # db.init_app(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # if app.config['INFERENCE']:
    #     with open(app.config['MODEL_PATH'], 'rb') as fin:
    #         app.model = pickle.load(fin)

    app.config["data"] = get_corpus()
    app.config["corpus"] = [data[2] for data in app.config["data"]]
    app.config["model"] = SentenceTransformer("all-MiniLM-L6-v2")

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # @app.before_request
    # def load_logged_in_user():
    #     uuid = session.get('sess_secret')
    #     db = get_db()
    #     if not uuid:
    #         g.user = None
    #     else:
    #         import pdb
    #         pdb.set_trace()
    #         g.user = CreateparticipantParticipant.select().where(CreateparticipantParticipant.uuid == uuid).get_or_none()

    app.register_blueprint(search.bp)
    return app
