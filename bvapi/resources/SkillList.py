from .SkillStoreResource import SkillStoreResource


class SkillList(SkillStoreResource):
    """List skills"""

    def get(self):
        """List all the skills

        Returns:
            The list of skills
        """
        return list(self.skill_store.keys())
