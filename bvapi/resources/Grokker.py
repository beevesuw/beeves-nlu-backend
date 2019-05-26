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
        print(q)
        skill_name = q.get('skill_name', '')
        text = q.get('text', '')
        top_n = q.get('top_n', None)
        intents = q.get('intents', None)
        ss_keys = [x for x in self.skill_store.keys()]
        print(ss_keys)
        if skill_name not in self.skill_store:
            return {"skill_name": skill_name, "error" : "SkillNotFound"}
        
        
       

        try:
            skill = self.skill_store[ q['skill_name']]
        except KeyError:
            return  {"skill_name": skill_name, "error" : "not found"}

        try:
            parse_result = skill['engine'].parse(text, intents, top_n)
        except KeyError:
            return  {"skill_name": skill_name, "error" : "BeevesBackendException"}
        except SnipsNLUError:
            return  {"skill_name": skill_name, "error" : "SnipsNLUError"}

        return {"skill_name": skill_name, "parse_result": parse_result}
