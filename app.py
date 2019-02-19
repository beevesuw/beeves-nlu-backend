from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask import request, jsonify

from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN

import shelve
import json

app = Flask(__name__)
api = Api(app)

skills = shelve.open('skills.shelve')

nlu_engines = {}



def abort_if_spec_doesnt_exist(skl_id, message=''):
    if skl_id not in skills:
        abort(404, message=message)


class Grokker(Resource):
    '''Attempt to dispatch and resolve request'''

    def post(self):
        q = request.get_json()
        skl_id = q['q'].split(' ', 1)[0].strip().lower()
        abort_if_spec_doesnt_exist(skl_id)

        if (skl_id not in nlu_engines):
            nlu_engines[skl_id] = SnipsNLUEngine(config=CONFIG_EN).fit(skills[skl_id])

        if (nlu_engines[skl_id].fitted == False):  # terrible, do this using  SnipsNLUEngine.persist()
            nlu_engines[skl_id] = SnipsNLUEngine(config=CONFIG_EN).fit(skills[skl_id])

        parseResult = nlu_engines[skl_id].parse(q["q"])
        return {"skillId": skl_id, "parseResult": parseResult}


class Skill(Resource):
    """ GET - return the specification of the skill embodied by the model"""

    def get(self, skl_id):
        skl_id = skl_id.lower()
        abort_if_spec_doesnt_exist(skl_id)
        return skills[skl_id]

    """ DEL - delete the skill"""

    def delete(self, skl_id):
        skl_id = skl_id.lower()
        abort_if_spec_doesnt_exist(skl_id)
        del skills[skl_id]
        skills.sync()
        del nlu_engines[skl_id]
        return '', 204

    """ PUT - create a skill """

    def put(self, skl_id):
        skl_id = skl_id.lower()
        if skl_id in skills:
            abort(404, message="Spec {} does exist".format(skl_id))

        sp = json.loads(request.get_data(as_text=True))
        skills[skl_id] = sp
        return skl_id, 201


class SkillList(Resource):
    """ List skills"""

    def get(self):
        return dict(skills)


api.add_resource(SkillList, '/skills')
api.add_resource(Skill, '/skill/<skl_id>')
api.add_resource(Grokker, '/grok')


@app.route("/")
def home():
    return render_template("ask.html", skills=skills.keys())


from flask import render_template

if __name__ == '__main__':
    app.run(debug=True, static_url_path='')
