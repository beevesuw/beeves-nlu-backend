import json
import re

from flask import request
from flask_restful import Resource, abort

from app import app


class Grokker(Resource):
    """Attempt to dispatch and resolve request"""

    def post(self):
        q = request.get_json()
        skill_name = q['q'].split(' ', 1)[0].strip().lower()

        if skill_name not in app.skill_store.keys():
            abort(404, msg="Skill %s not found" % skill_name)

        parse_result = app.skill_store[skill_name].parse(q["q"])
        return {"skill_id": skill_name, "parse_result": parse_result}


# noinspection PyMethodMayBeStatic
class Skill(Resource):
    """ GET - return the specification of the skill embodied by the model"""

    @staticmethod
    def canonicalize_skill_name(skill_name):
        skill_name_ = skill_name.strip().lower()
        lcw_skill_name = re.sub(re.compile(r'\W+'), '', skill_name_)
        if len(lcw_skill_name) == 0:
            lcw_skill_name = None
        return lcw_skill_name

    @staticmethod
    def get_canonical_skill_name_or_die(x_skill_name, die_code=404, msg='Skill not found'):
        skill_name = Skill.canonicalize_skill_name(x_skill_name)
        if skill_name not in app.skill_store:
            abort(die_code, msg=msg)
        return skill_name

    def get(self, skill_name):
        skill_name = self.get_canonical_skill_name_or_die(skill_name)

        found_skill = app.skill_store.get(skill_name)
        if found_skill:
            return {skill_name: found_skill}

    """ DEL - delete the skill"""

    def delete(self, skill_name):
        skill_name = self.get_canonical_skill_name_or_die(skill_name)
        del app.skill_store[skill_name]
        return skill_name, 204

    """ PUT - create a skill """

    def put(self, skill_name):
        skill_name = skill_name.strip().lower()
        if skill_name in app.skill_store:
            app.logger.info('Replacing skill "%s" with a new one' % skill_name)
        sp = json.loads(request.get_data(as_text=True))
        app.skill_store[skill_name] = sp
        return skill_name, 201

    def post(self, skill_name):
        skill_name = app.get_canonical_skill_name_or_die(skill_name)
        q = request.get_json()

        parse_result = app.skill_store[skill_name].parse(q["q"])
        return {"skill_id": skill_name, "parse_result": parse_result}


class SkillList(Resource):
    """ List skills"""

    def get(self):
        return dict(app.skill_store)
