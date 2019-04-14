import logging
import time
from pathlib import Path

import snips_nlu
import snips_nlu.default_configs
import snips_nlu.exceptions
import sqlitedict


class SkillStore(object):
    """
    The SkillStore object persists a dictionary containing:
        'name' : name of the skill
        'src' : source from which it was created
        'engine' : serialized representation of SnipsNLUEngine trained with it


    Attributes:
        db_path (pathlib.Path): Path to shelf file
        __db:
    """

    def __init__(self, db_path: str,
                 default_snips_nlu_config: dict = snips_nlu.default_configs.CONFIG_EN):  # noqa
        """Initialize the store
        Args:
            db_path: Path to which the database should be persisted
            default_snips_nlu_config: Configuration passed to SnipsNLUEngine.
        """

        self.db_path = Path(db_path)
        if self.db_path.exists():
            logging.getLogger().info(f"'{db_path}' already exists; using that'")

        self.__db = sqlitedict.open(str(self.db_path), autocommit=True)
        self.default_snips_nlu_config = default_snips_nlu_config
        logging.getLogger().info(f"Initialized {self.__class__.__name__} with path '{self.db_path}'")

    def keys(self):
        """List the names of the skills in the store
        Returns:
            A list of names.
        """
        return self.__db.keys()

    def __setitem__(self, skill_name: str, skill_definition):
        """Define a skill
        Args:
            skill_name: Skill name
            skill_definition: Skill definition -- this is strictly the format accepted by SnipsNLU Engine.
             TODO: Fix this to be independent.
        """
        snips_nlu_config = skill_definition.setdefault('snips_nlu_config', self.default_snips_nlu_config)

        if skill_name in self.__db:
            logging.getLogger().info(f"Skill with name  '{skill_name}' already exists; overwriting...'")

        logging.getLogger().info(f"Training skill with name  '{skill_name}'...'")
        engine = snips_nlu.SnipsNLUEngine(config=snips_nlu_config)
        start_time = time.time()
        engine.fit(skill_definition)
        end_time = time.time()
        elapsed_time = end_time - start_time

        engine_bytes = engine.to_byte_array()

        logging.getLogger().info(f"Trained skill with name '{skill_name}' in {round(elapsed_time, 2)} s; size is {len(engine_bytes) // 1024} KiB. Going to serialize...")

        obj = {'name'            : skill_name, 'src': skill_definition, 'engine': engine_bytes,
               'snips_nlu_config': snips_nlu_config}

        self.__db[skill_name] = obj
        self.__db.sync()
        logging.getLogger().info(f"Skill with name  '{skill_name}' written to the shelf'")

    def __getitem__(self, skill_name: str):
        """Get the skill definition and resources from the store
        Args:
            skill_name: Name of the skill

        Returns:
           A dictionary with the skill definition and resources
        """
        logging.getLogger().info('666666')
        if skill_name in self.__db:
            obj = self.__db[skill_name]
            if 'engine' in obj:
                obj['engine'] = snips_nlu.SnipsNLUEngine.from_byte_array(obj['engine'])
            else:
                logging.getLogger().warning(f"Skill '{skill_name}' didn't have a persisted engine")
        else:
            logging.getLogger().warning(f"Skill '{skill_name}' not found")
            raise KeyError(f"Skill '{skill_name}' not found")
        return obj

    def __delitem__(self, skill_name: str):
        """Delete a skill
        Args:
            skill_name: Skill name
        """
        del self.__db[skill_name]
        self.__db.sync()

    def __contains__(self, skill_name: str) -> bool:
        """Query whether a skill is in the store
         Args:
             skill_name: Skill name
         """
        return skill_name in self.__db

    def __len__(self) -> int:
        """Get number of skills
         """
        return len(self.__db)
