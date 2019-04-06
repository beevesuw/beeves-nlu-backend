import os

from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app.config.from_object('app.default_settings')

api = Api(app)

app.debug = True

app.config.update(JSON_SORT_KEYS=True,
                  JSONIFY_PRETTYPRINT_REGULAR=True,
                  JSON_AS_ASCII=False,
                  DEBUG=True)

from app.storage import SkillStore

app.skill_store = SkillStore()

import logging
from logging.handlers import TimedRotatingFileHandler

# https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler


# Set up a log file in the LOG_DIR directory specified in default_settings.py:
file_handler = TimedRotatingFileHandler(os.path.join(app.config['LOG_DIR'], 'app.log'), 'midnight')
file_handler.setLevel(level=os.environ.get("LOGLEVEL", "INFO"))
file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
app.logger.addHandler(file_handler)

FORMAT = "[<%(asctime)s> %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)


from app.resources import *

api.add_resource(SkillList, '/skills', '/')
api.add_resource(Skill, '/skill/<skill_name>')
api.add_resource(Grokker, '/grok')

if __name__ == '__main__':
    app.run(debug=app.debug)
