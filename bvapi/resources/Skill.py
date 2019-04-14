import logging

from flask import json

from .SkillStoreResource import SkillStoreResource
from .util import *


class Skill(SkillStoreResource):
    """This is a resource class for managing CRUD of skills."""

    def get_canonical_skill_name_or_die(self, skill_name: str):
        """Get the cleaned name of a skill in the database or return a 404 to
        the client

        Args:
            skill_name (str): Name of the skill.

        Returns:
            The cleaned up name
        """
        canonical_skill_name = canonicalize_skill_name(skill_name)
        if canonical_skill_name not in self.skill_store:
            raise SkillNotFound(skill_name)
        return skill_name

    def get(self, skill_name: str):
        """Get the original skill definition from storage :param skill_name:
        Name of the skill.

        Args:
            skill_name (str):

        Returns:
            The skill definition as json
        """

        skill_name = self.get_canonical_skill_name_or_die(skill_name)

        try:
            found_skill = self.skill_store[skill_name]
        except KeyError:
            raise SkillNotFound(skill_name)

        try:
            dataset_metadata = found_skill['src']
        except KeyError:
            raise BeevesBackendException("Couldn't find skill '%s' source code" % skill_name)
        return {skill_name: dataset_metadata}

    def delete(self, skill_name: str):
        """Remove the skill from storage :param skill_name: Name of the skill.

        Args:
            skill_name (str):

        Returns:
            HTTP 204 No Content
        """
        skill_name = self.get_canonical_skill_name_or_die(skill_name)
        del self.skill_store[skill_name]
        return 204

    def put(self, skill_name: str):
        """Create and register the skill :param skill_name: Name of the skill.

        Args:
            skill_name (str):

        Returns:
            HTTP 201 Created
        """
        skill_name = canonicalize_skill_name(skill_name)

        if skill_name in self.skill_store:
            logging.getLogger().info('Replacing skill "%s" with a new one' % skill_name)
        sp = json.loads(request.get_data(as_text=True))
        self.skill_store[skill_name] = sp
        return 201
