import json
import re

from flask import request
from flask_restful import Resource, abort

from app import app


# noinspection PyMethodMayBeStatic
class Grokker(Resource):
    """The summary line for a class docstring should fit on one line.


    This is a REST resource that takes an input string (e.g., 'beverage make me coffee'),
    uses its first word as a key to select which skill it should dispatch to,
    asks the NLU engine to parse the result,
    and returns the object that was parsed.

    Example:
        Run this on the command line:
        $ curl -d '{"q":"beverage make me coffee"}' -H "Content-Type: application/json" -X POST http://localhost:5000/grok

    """

    def post(self):
        """Process an input string with natural language understanding and return the result for intent and slot assignment.

        Returns:
            The parse result and skill name that was found.

        """
        q = request.get_json()
        skill_name = Skill.canonicalize_skill_name(q['q'].split(' ', 1)[0])

        if skill_name not in app.skill_store.keys():
            abort(404, msg="Skill %s not found" % skill_name)

        skill = app.skill_store[skill_name]

        parse_result = skill['engine'].parse(q["q"])
        return {"skill_name": skill_name, "parse_result": parse_result}


# noinspection PyMethodMayBeStatic
class Skill(Resource):
    """This is a resource class for managing CRUD of skills.
    """

    @staticmethod
    def canonicalize_skill_name(skill_name: str):
        """Function to clean up a skill name

        Args:
            skill_name: Name of the skill.

        Returns:
            The cleaned up name, or None.
        """
        skill_name_ = skill_name.strip().lower()
        lcw_skill_name = re.sub(re.compile(r'\W+'), '', skill_name_)
        if len(lcw_skill_name) == 0:
            lcw_skill_name = None
        return lcw_skill_name

    @staticmethod
    def get_canonical_skill_name_or_die(skill_name: str, die_code: int = 404, msg: str = 'Skill not found'):
        """Get the cleaned name of a skill in the database or return a 404 to the client

        Args:
            skill_name: Name of the skill.
            die_code: HTTP error code that should be returned.
            msg: Error message that should be returned.

        Returns:
            The cleaned up name
        """
        canonical_skill_name = Skill.canonicalize_skill_name(skill_name)
        if canonical_skill_name not in app.skill_store:
            abort(die_code, msg=msg)
        return skill_name

    def get(self, skill_name: str):
        """Get the original skill definition from storage
        Args:
            skill_name: Name of the skill.

        Returns:
            The skill definition as json
        """
        skill_name = self.get_canonical_skill_name_or_die(skill_name)

        found_skill = app.skill_store[skill_name]
        if found_skill:
            dataset_metadata = found_skill['src']
            if not dataset_metadata:
                dataset_metadata = {}
            return {skill_name: dataset_metadata}

    def delete(self, skill_name: str):
        """Remove the skill from storage
        Args:
            skill_name: Name of the skill.

        Returns:
            HTTP 204 No Content
        """
        skill_name = self.get_canonical_skill_name_or_die(skill_name)
        del app.skill_store[skill_name]
        return 204

    def put(self, skill_name: str):
        """Create and register the skill
        Args:
            skill_name: Name of the skill.

        Returns:
            HTTP 201 Created
        """
        skill_name = self.canonicalize_skill_name(skill_name)
        if skill_name in app.skill_store:
            app.logger.info('Replacing skill "%s" with a new one' % skill_name)
        sp = json.loads(request.get_data(as_text=True))

        app.skill_store[skill_name] = sp
        return 201


# noinspection PyMethodMayBeStatic
class SkillList(Resource):
    """ List skills"""

    def get(self):
        """List all the skills

        Returns:
            The list of skills
        """
        return list(app.skill_store.keys())
