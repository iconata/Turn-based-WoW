"""
Handler library, that contains all Mage spells.
"""

import math

from Heroes.hero_base_stats import BaseHeroStats


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class FireMageSpells(BaseHeroStats):
    """
    Fire Mage Spells Handler
    This class contains all the spells and abilities of the Fire Mage.
    It inherits from the BaseHeroStats class, which contains the base stats of the hero.
    The Fire Mage is a ranged damage dealer, specializing in fire magic.

    Args:
        BaseHeroStats (cls): Base class for all heroes, containing base stats and methods.
    """

    def __init__(self):
        super().__init__()
        self._health = 700
        self._secondary_pool = 900
        self._spell_power = 110
        self._max_damage_red = 100
        self._max_health = self._health
        self._max_mana = self._secondary_pool
        self._base_damage_red = self._damage_reduction
        self._current_damage_red = self._damage_reduction

    # ------------------------------------------------------------------------ #

    def cast_fireball(self):
        """
        Hurl a fireball to the target, dealing significant fire damage.

        Returns:
            tuple: damage of the spell, cooldown of the spell
        """
        cooldown = 3
        spell_cost = math.ceil(self._max_mana * 2 / 100)
        spell_damage = math.ceil(self._spell_power * 155 / 100)
        self._secondary_pool -= spell_cost

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_fire_blast(self):
        """
        Blast the target with fire, decreasing their damage reduction by 15% for 3 turns.

        Returns:
            tuple: damage of the spell, amount of damage reduction to be applied,
            turns for which the effect is active
        """
        turns_active = 3
        damage_reduction = 15
        spell_cost = math.ceil(self._max_mana * 1 / 100)
        spell_damage = math.ceil(self._spell_power * 82 / 100)
        self._secondary_pool -= spell_cost

        return spell_damage, damage_reduction, turns_active

    # ------------------------------------------------------------------------ #
    def cast_flamestrike(self):
        """
        Ignite the ground under the feet of your target, making them take damage over time for 3 turns.
        Cooldown - 5 turns.

        Returns:
            tuple: damage of the spell, cooldown of the spell, turns for which the spell is active
        """
        turns_active = 3
        cooldown = 5
        spell_cost = math.ceil(self._max_mana * 1 / 100)
        spell_damage = math.ceil(self._spell_power * 57 / 100)
        self._secondary_pool -= spell_cost

        return spell_damage, cooldown, turns_active

    # ------------------------------------------------------------------------ #
    def cast_polymorph(self):
        """
        Pacify the target for 2 turns, making them unable to cast any spells.
        Any damage suffered by the target will break the effect.
        Cooldown - 5 turns.

        Returns:
            tuple: cooldown of the spell, turns for which the spell is active
        """
        turns_active = 2
        cooldown = 5
        spell_cost = math.ceil(self._max_mana * 1 / 100)
        self._secondary_pool -= spell_cost

        return cooldown, turns_active

    # ------------------------------------------------------------------------ #
    def cast_arcane_intellect(self):
        """
        Your arcane understanding, increases your spell power by 10% for 4 turns.
        Cooldown - 4 turns.

        Returns:
            tuple: cooldown of the spell, turns for which the spell is active
        """
        turns_active = 4
        cooldown = 4
        self._spell_power += math.ceil(self._spell_power * 10 / 100)
        spell_cost = math.ceil(self._max_mana * 4 / 100)
        self._secondary_pool -= spell_cost

        return cooldown, turns_active
