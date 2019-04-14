from functools import wraps
from os import getenv

from flask import request

import re


class BeevesBackendException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """
        Args:
            message:
            status_code:
            payload:
        """
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class SkillNotFound(BeevesBackendException):
    status_code = 404
    message = "Skill not found"

    def __init__(self, skill_name: str):
        """
        Args:
            skill_name (str):
        """
        self.payload = {'skill_name': skill_name}


class AuthenticationError(BeevesBackendException):
    status_code = 403
    message = "Invalid key"
    payload = {}

    def __init__(self):
        pass


def canonicalize_skill_name(skill_name: str):
    """Function to clean up a skill name

    Args:
        skill_name (str): Name of the skill.

    Returns:
        The cleaned up name, or None.
    """
    skill_name_ = skill_name.strip().lower()
    lcw_skill_name = re.sub(re.compile(r'\W+'), '', skill_name_)
    if len(lcw_skill_name) == 0:
        lcw_skill_name = None
    return lcw_skill_name


def beeves_key_required(f):
    """
    Args:
        f:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        beeves_key = getenv('BEEVES_KEY')
        if beeves_key is not None and request.cookies.get('BEEVES_KEY',
                                                          request.args.get('beeves_key', '')) != beeves_key:
            raise AuthenticationError
        return f(*args, **kwargs)

    return decorated_function
