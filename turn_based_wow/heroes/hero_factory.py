"""
Hero Factory which creates a hero based on the input.
"""

from turn_based_wow.heroes.hero_base_stats import IBaseHero
from turn_based_wow.spells.mage_spell_handler import FireMageSpells
from turn_based_wow.spells.monk_spell_handler import BrewmasterMonkSpells, WindwalkerMonkSpells
from turn_based_wow.spells.paladin_spell_handler import (
    ProtectionPaladinSpells,
    RetributionPaladinSpells,
)
from turn_based_wow.spells.priest_spell_handler import ShadowPriestSpells
from turn_based_wow.spells.shaman_spell_handler import EnhancementShamanSpells
from turn_based_wow.spells.warrior_spell_handler import FuryWarriorSpells, ProtectionWarriorSpells


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
        """Instantiate a concrete hero class from a (class, role) pair.

        The factory accepts case-insensitive `hero_class` and `hero_role`
        and returns a ready-to-use hero instance whose per-spec stats are
        initialized by the concrete spell-handler class.
        """
        key = (hero_class.lower(), hero_role.lower())
        hero_cls = self._hero_registry.get(key)
        if not hero_cls:
            raise ValueError(f"Unknown hero class or role: {hero_class}, {hero_role}")
        return hero_cls()
