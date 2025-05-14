"""
Hero Factory which creates a hero based on the input.
"""
from Heroes.hero_base_stats import IBaseHero

# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #


class HeroContext:
    """
    Context class, which creates a hero instance, based on the instance provided.

    Returns:
        IBaseHero: hero instance
    """
    # ------------------------------------------------------------------------ #
    def create_hero(self, hero_type: IBaseHero):

        return hero_type.create_hero(hero_type)
