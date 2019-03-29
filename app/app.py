from flask import Flask
from flask_restful import Api, abort

app = Flask(__name__)
api = Api(app)

app.debug = True

app.config.update(JSON_SORT_KEYS=True,
                  JSONIFY_PRETTYPRINT_REGULAR=True,
                  JSON_AS_ASCII=False,
                  DEBUG=True)

import re


def canonicalize_skill_name(skill_name):
    skill_name_ = skill_name.trim().lower()
    lcw_skill_name = re.sub(re.compile(r'\W+'), '', skill_name_)
    if len(lcw_skill_name) == 0:
        lcw_skill_name = None
    return lcw_skill_name


def get_canonical_skill_name_or_die(x_skill_name, die_code=404, msg='Skill not found'):
    skill_name = canonicalize_skill_name(x_skill_name)
    if skill_name not in app.skill_store:
        abort(die_code, msg=msg)
    return skill_name


import app.resources

api.add_resource(app.resources.SkillList, '/skills', '/')
api.add_resource(app.resources.Skill, '/skill/<skill_name>')
api.add_resource(app.resources.Grokker, '/grok')
