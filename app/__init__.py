import os

from flask import Flask

from app.storage import SkillStore

app = Flask(__name__)
app.config.from_object('app.default_settings')
app.config.from_envvar('APP_SETTINGS')

app.skill_store = SkillStore()
app.debug = True

import app.resources

if not app.debug:
    import logging
    from logging.handlers import TimedRotatingFileHandler

    # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
    file_handler = TimedRotatingFileHandler(os.path.join(app.config['LOG_DIR'], 'app.log'), 'midnight')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
    app.logger.addHandler(file_handler)

if __name__ == '__main__':
    app.run(debug=True, static_url_path='./static/')
