from flask_restful import Resource
from .util import beeves_key_required

class SkillStoreResource(Resource):
    method_decorators = [beeves_key_required]

    def __init__(self, **kwargs):
        """A resource that has a skill_store property

        Args:
            skill_store (Any): the skill store object.

        Returns:
            The cleaned up name
        """
        self.skill_store = kwargs['skill_store']
