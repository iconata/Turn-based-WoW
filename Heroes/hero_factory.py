"""
Hero Factory which creates a hero based on the input.
"""

from Heroes.hero_base_stats import IBaseHero
from Spells.mage_spell_handler import FireMageSpells
from Spells.monk_spell_handler import BrewmasterMonkSpells, WindwalkerMonkSpells
from Spells.paladin_spell_handler import (
    ProtectionPaladinSpells,
    RetributionPaladinSpells,
)
from Spells.priest_spell_handler import ShadowPriestSpells
from Spells.shaman_spell_handler import EnhancementShamanSpells
from Spells.warrior_spell_handler import FuryWarriorSpells, ProtectionWarriorSpells


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class HeroFactory:
    """
    Factory class, which creates a hero with specific stats and spells, based on the input provided.

    Returns:
        IBaseHero: hero instance
    """

    _hero_registry = {
        ("paladin", "protection"): ProtectionPaladinSpells,
        ("paladin", "retribution"): RetributionPaladinSpells,
        ("warrior", "protection"): ProtectionWarriorSpells,
        ("warrior", "fury"): FuryWarriorSpells,
        ("priest", "shadow"): ShadowPriestSpells,
        ("mage", "fire"): FireMageSpells,
        ("monk", "brewmaster"): BrewmasterMonkSpells,
        ("monk", "windwalker"): WindwalkerMonkSpells,
        ("shaman", "enhancement"): EnhancementShamanSpells,
    }

    # ------------------------------------------------------------------------ #
    def create_hero(self, hero_class: str, hero_role: str) -> IBaseHero:
        key = (hero_class.lower(), hero_role.lower())
        hero_cls = self._hero_registry.get(key)
        if not hero_cls:
            raise ValueError(f"Unknown hero class or role: {hero_class}, {hero_role}")
        return hero_cls()
