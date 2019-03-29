# import shelve
import shutil
from pathlib import Path

import snips_nlu as sn
import snips_nlu.default_configs

from app import app


class SkillStore(dict):
    """
    The SkillStore object is an interface to snips_nlu.SnipsNLUEngine's persisted trained engines.

    Attributes:
        parent_dir (pathlib.Path): This is where we store arg,
    """

    def __init__(self, parent_dir='./storage-dir', snips_nlu_engine_config=snips_nlu.default_configs.CONFIG_EN):  # noqa
        self.parent_dir = Path(parent_dir)

        self.parent_dir.mkdir(parents=True, exist_ok=True)
        self.snips_nlu_engine_config = snips_nlu_engine_config

    def keys(self):
        return [x.name for x in self.parent_dir.iterdir() if x.is_dir() and x.name[0] != '.']

    def list_skills(self):
        return [x for x in self.parent_dir.iterdir() if x.is_dir() and x.name[0] != '.']

    def __setitem__(self, skill_name, skill_definition):
        engine = sn.SnipsNLUEngine(config=self.snips_nlu_engine_config)
        engine.fit(skill_definition)

        app.logger.info("SkillStore.__setitem__(skill_name=%s)" % skill_name)

        skill_path = self.parent_dir.joinpath(skill_name)
        if skill_path.exists():
            app.logger.info("SkillStore.__setitem__(skill_name=%s) - Overwriting existing skill!" % skill_name)

        engine.persist(self.parent_dir.joinpath(skill_name))

    def __getitem__(self, skill_name):
        engine = sn.SnipsNLUEngine(config=self.snips_nlu_engine_config)
        engine.load_from_path(self.parent_dir, skill_name)
        return engine

    def __delitem__(self, skill_name):
        skill_path = self.parent_dir.joinpath(skill_name)

        if not skill_path.exists():
            app.logger.info("SkillStore.__delitem__(skill_name=%s) - No skill by that name" % skill_name)
        else:
            app.logger.info("SkillStore.__delitem__(skill_name=%s) - deleting" % skill_name)

        shutil.rmtree(skill_path, ignore_errors=True)

    def __contains__(self, skill_name):
        return skill_name in self.list_skills()

    def __len__(self):
        if self.parent_dir.is_dir():
            return len([x for x in self.parent_dir.iterdir() if x.is_dir()])
        else:
            app.logger.info("SkillStore.__len__() - no skills! Returning 0")
            return 0
