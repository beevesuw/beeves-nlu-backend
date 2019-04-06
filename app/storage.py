from collections import UserDict
from pathlib import Path
from threading import Lock

import snips_nlu as sn
import snips_nlu.default_configs
import sqlitedict

from app import app

mutex = Lock()

# TODO: document interfaces
# TODO: examples
# TODO: pytest

"""
'CREATE TABLE engines
             (name text, bytes blob , ctime datetime default current_timestamp, mtime datetime default current_timestamp)' 
"""


class SkillStore(UserDict):
    """
    The SkillStore object is an interface to manage a collection of snips_nlu.SnipsNLUEngines

    Attributes:
        db_path (pathlib.Path): Path to shelf file
        __db: Shelf object
    """

    def __init__(self, db_path='skill_store.db', snips_nlu_config=snips_nlu.default_configs.CONFIG_EN):  # noqa
        self.__db = {}

        self.db_path = Path(db_path)
        if self.db_path.exists():
            app.logger.info(f"'{db_path}' already exists; using that'")

        self.__db = sqlitedict.open(str(self.db_path), autocommit=True)

        self.configs = {'snips_nlu': snips_nlu_config}
        app.logger.info(f"Initialized {self.__class__.__name__} with path '{self.db_path}'")

    def keys(self):
        return self.__db.keys()

    def __setitem__(self, skill_name, skill_definition):

        engine = sn.SnipsNLUEngine(config=self.configs['snips_nlu'])
        engine.fit(skill_definition)

        if skill_name in self.__db:
            app.logger.info(f"Skill with name  '{skill_name}' already exists; overwriting...'")

        engine_bytes = engine.to_byte_array()

        if not engine_bytes:
            app.logger.warning(f"Skill with name  '{skill_name}' couldn't be serialized from the engine; aborting'")
            return

        obj = {'name': skill_name, 'src': skill_definition, 'engine': engine_bytes}

        self.__db[skill_name] = obj
        self.__db.sync()
        app.logger.info(f"Skill with name  '{skill_name}' written to the shelf'")


    def __getitem__(self, skill_name):
        if skill_name in self.__db:
            obj = self.__db[skill_name]
            obj['engine'] = sn.SnipsNLUEngine.from_byte_array(obj['engine'])
        else:
            app.logger.warning(f"Skill '{skill_name}' not found")
            raise KeyError(f"Skill '{skill_name}' not found")
        return obj

    def __delitem__(self, skill_name):
        del self.__db[skill_name]
        self.__db.sync()

    def __contains__(self, skill_name):
        return skill_name in self.__db

    def __len__(self):
        return len(self.__db)
