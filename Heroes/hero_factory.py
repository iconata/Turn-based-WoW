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
        # instantiate the hero class
        hero_instance = hero_cls()

        # allow the instance to configure its own stats via `create_hero`
        # (many spell handler classes implement a `create_hero(self, hero_instance)`
        # that sets `max_health`, `max_secondary_pool`, `attack_power`, etc.)
        try:
            configured = hero_instance.create_hero(hero_instance)
            # Some implementations return the instance, others modify in-place.
            final = configured if configured is not None else hero_instance
            # ensure current pools/health match configured maxima
            try:
                final.set_health(final.max_health)
            except Exception:
                final._curr_health = final.max_health
            try:
                final.set_secondary_pool(final.max_secondary_pool)
            except Exception:
                if hasattr(final, "_curr_mana"):
                    final._curr_mana = final.max_secondary_pool
                else:
                    final._curr_secondary_pool = final.max_secondary_pool

            return final
        except Exception:
            # If configuration fails for any reason, fall back to the raw instance.
            return hero_instance
