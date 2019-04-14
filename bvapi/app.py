from logging.config import dictConfig
from pathlib import Path

from flask import Flask
from flask import jsonify, json
from flask_restful import Api
import logging

DEFAULT_SETTINGS_PATH = Path(__file__).parent.resolve() / "settings.json"
default_settings = json.load(open(DEFAULT_SETTINGS_PATH, 'r'))
LOGGING_DICT_CONFIG = default_settings['LOGGING_DICT_CONFIG']

dictConfig(LOGGING_DICT_CONFIG)

from resources.Skill import Skill  # noqa
from resources.SkillList import SkillList  # noqa
from resources.Grokker import Grokker  # noqa

import resources.util  # noqa

app = Flask(__name__)
api = Api(app)

app.config.from_json(DEFAULT_SETTINGS_PATH)

dictConfig(app.config['LOGGING_DICT_CONFIG'])

# app.config.from_envvar('BVAPI_SETTINGS')

from storage import SkillStore  # noqa

app.skill_store = SkillStore(Path(__file__).parent.resolve() / app.config['SKILL_DB_PATH'])

app.logger.level = app.config['LOG_LEVEL']

api.add_resource(Skill, '/skill/<skill_name>', resource_class_kwargs={'skill_store': app.skill_store})
api.add_resource(SkillList, '/skills', '/skill', '/', resource_class_kwargs={'skill_store': app.skill_store})
api.add_resource(Grokker, '/grok', resource_class_kwargs={'skill_store': app.skill_store})


@app.errorhandler(resources.util.BeevesBackendException)
def handle_invalid_usage(error):
    """
    Args:
        error:
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    logging.getLogger().warn(str(response))
    return response


if __name__ == '__main__':
    app.run(debug=True, host=app.config['HOST_NAME'], port=app.config['HOST_PORT'])
