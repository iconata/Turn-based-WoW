"""
Handler library, which contains all Priest spells
"""

import math


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class ShadowPriestSpells:

    # ------------------------------------------------------------------------ #
    def __init__(self, hero_instance):
        self._current_health        = hero_instance._health
        self._max_health            = hero_instance._health
        self._current_mana          = hero_instance._secondary_pool
        self._max_mana              = hero_instance._secondary_pool
        self._spell_power           = hero_instance._spell_power

    # ------------------------------------------------------------------------ #
    def cast_mind_blast(self):
        """
        Blast the mind of the target, dealing shadow damage.

        Returns:
            tuple: damage of the spell, cooldown of the spell
        """
        cooldown = 3
        spell_cost           = math.ceil(self._current_mana * 4 / 100)
        spell_damage         = math.ceil(self._spell_power  * 73 / 100)
        self._current_mana  -= spell_cost

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_shadow_word_death(self):
        """
        A word of dark binding, dealing moderate shadow damage. If the target is below 20% hp,
        the damage is increased by 150%. If the target does not die, the caster suffers a backash,
        equal to 5% of the casters max health.

        Returns:
            tuple: damage of the spell, cooldown of the spell
        """
        cooldown = 3
        spell_cost           = math.ceil(self._current_mana * 1 / 100)
        spell_damage         = math.ceil(self._spell_power  * 85 / 100)
        self._current_mana  -= spell_cost

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_devouring_plague(self):
        """
        Afflict the target with a disease, dealing initial shadow damage, damage over time
        and restoring health to the caster.

        Returns:
            tuple: initial spell damage, damage over time, amount of health restored
            to the caster, cooldown of the spell, turns for which the spell is active
        """
        cooldown             = 4
        turns_active         = 3
        spell_cost           = math.ceil(self._current_mana   * 10 / 100)
        initial_spell_damage = math.ceil(self._spell_power    * 155 / 100)
        health_leech         = math.ceil(initial_spell_damage * 30 / 100)
        damage_over_time     = math.ceil(initial_spell_damage * 13 / 100)
        self._current_mana  -= spell_cost

        return initial_spell_damage, damage_over_time, health_leech, cooldown, turns_active

    # ------------------------------------------------------------------------ #
    def cast_flash_heal(self):
        """
        Quick healing spell, healing for moderate amount.
        """
        spell_cost           = math.ceil(self._current_mana * 10 / 100)
        amount_to_heal       = math.ceil(self._spell_power  * 203 / 100)
        self._current_mana  -= spell_cost
        self._heal_up(amount_to_heal)

    # ------------------------------------------------------------------------ #
    def cast_power_word_shield(self):
        """
        Powerfull word that creates a shield around the caster, absorbing a fixed amount of incoming damage.

        Returns:
            tuple: amount of damage that will be absorbed, cooldown of the spell
        """
        cooldown = 5
        spell_cost           = math.ceil(self._current_mana * 10 / 100)
        damage_to_absorb     = math.ceil(self._spell_power  * 336 / 100)
        self._current_mana  -= spell_cost

        return damage_to_absorb, cooldown

    # ------------------------------------------------------------------------ #
    def _heal_up(self, heal_amount):
        """
        Main healing spell logic. Checks the current health of the hero and also the incoming amount.
        If the incoming amount is overhealing, the current health will be set to the max health.

        Args:
            heal_amount (int): value of the incoming heal
        """
        if self._current_health < 0:
            self._current_health = 0

        elif self._current_health + heal_amount > self._max_health:
            self._current_health = self._max_health

    # ------------------------------------------------------------------------ #
