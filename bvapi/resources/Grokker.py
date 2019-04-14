from snips_nlu.exceptions import SnipsNLUError
from .SkillStoreResource import SkillStoreResource
from .util import *


class Grokker(SkillStoreResource):
    """Assign intents and slots from a natural-language string

    This is a REST resource that takes an input string (e.g., 'beverage make
    me coffee'), uses its first word as a key to select which skill it should
    dispatch to, asks the NLU engine to parse the result, and returns the object
    that was parsed.

    Example:
        Run this on the command line: $ curl -d '{"q":"beverage make me
        coffee"}' -H "Content-Type: application/json" -X POST
        http://localhost:5000/grok
    """

    def post(self):
        """Process an input string with natural language understanding and
        return the result for intent and slot assignment.

        Returns:
            The parse result and skill name that was found.
        """
        q = request.get_json()
        skill_name = canonicalize_skill_name(q['q'].split(' ', 1)[0])

        try:
            skill = self.skill_store[skill_name]
        except KeyError:
            raise SkillNotFound(skill_name)

        try:
            parse_result = skill['engine'].parse(q["q"])
        except KeyError:
            raise BeevesBackendException("Skill %s did not have engine field" % skill_name)
        except SnipsNLUError:
            raise BeevesBackendException("Skill %s failed to parse" % skill_name)

        return {"skill_name": skill_name, "parse_result": parse_result}
