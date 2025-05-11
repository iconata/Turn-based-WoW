"""
Handler library, used to cast different types of Paladin spells, based on the selected role of the hero.
"""

import math

from Heroes.hero_base_stats import IBaseHero


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class PaladinCommonSpells(IBaseHero):
    """
    Common Spells Mixin
    This class contains the common spells and abilities of the Paladin.
    """

    # ------------------------------------------------------------------------ #
    def __init__(self):
        super().__init__()
        self._curr_holy_power = 0
        self._max_holy_power = 5
        self._curr_health = self.max_health
        self._curr_mana = self.max_secondary_pool
        self._base_damage_red = self.damage_reduction
        self._current_damage_red = self.damage_reduction
        self._max_damage_red = 100

    # ------------------------------------------------------------------------ #
    def cast_divine_shield(self) -> tuple:
        """
        Powerfull protection spell, which block all incoming damage for 2 turns.
        Cooldown - 15 turns.

        Returns:
            tuple: cooldown of the spell and for how many turns it is active
        """
        max_damage_reduction = 100
        cooldown = 15
        self._current_damage_red = max_damage_reduction
        turns_active = 2

        return cooldown, turns_active

    # ------------------------------------------------------------------------ #
    def cast_judgement(self) -> tuple:
        """
        Judges the target, dealing damage based on the hero's attack power. Generates 1 Holy Power.

        Returns:
            tuple: damage of the spell, cooldown of the spell
        """
        cooldown = 3
        holy_power_generation = 1
        spell_damage = math.ceil(self.attack_power * 61 / 100)
        spell_cost = math.ceil(self.max_secondary_pool * 5 / 100)
        self._curr_mana -= spell_cost
        self.add_specific_stat(holy_power_generation)

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_word_of_glory(self):
        """
        Fairly strong healing spell, healing for percent amount of the hero's spell power.
        Because of the spell cost, the internal logic will check if there's enough holy power so the spell can be cast.
        """
        cost = 3
        amount_to_heal = math.ceil(self._spell_power * 346 / 100)
        if self._is_holy_power_spent(holy_pow_req=cost):
            self.heal_up(amount_to_heal)

    # ------------------------------------------------------------------------ #
    def display_amount_of_holy_power(self):
        """
        Outputs the current spell power in the terminal
        """
        print(f"Holy power: {self._curr_holy_power}")

    # ------------------------------------------------------------------------ #
    def heal_up(self, heal_amount) -> None:
        """
        Main healing spell logic. Checks the current health of the hero and also the incoming amount.
        If the incoming amount is overhealing, the current health will be set to the max health.

        Args:
            heal_amount (int): value of the incoming heal
        """
        self._curr_health += heal_amount

        if self._curr_health > self.max_health:
            self._curr_health = self.max_health

    # ------------------------------------------------------------------------ #
    def add_specific_stat(self, stat_value: int = 0) -> None:
        """
        Checks the current amount of holy power available to the hero.
        If the holy power goes beyond the max holy power, the current holy power is set to the max

        Args:
            stat_value (int, optional): Adds the generated holy power to the currently available.
        """

        self._curr_holy_power += stat_value

        if self._curr_holy_power >= self._max_holy_power:
            self._curr_holy_power = self._max_holy_power

    # ------------------------------------------------------------------------ #
    def is_specific_stat_spent(self, stat_value: int) -> bool:
        """
        Boolean check if the hero has enough holy power for the spell that was casted.

        Args:
            stat_value (int): cost of the spell

        Returns:
            bool: returns True if there's enough spell power for the spell, otherwise returns False
        """
        if self._curr_holy_power >= stat_value:
            self._curr_holy_power -= stat_value
            return True
        else:
            return False


# ---------------------------------------------------------------------------- #
class RetributionPaladinSpells(PaladinCommonSpells):
    """
    Class that handles the Retribution Paladin spells.
    """

    def __init__(self):
        super().__init__()

    # ------------------------------------------------------------------------ #
    def cast_divine_protection(self) -> tuple:
        """
        Protection spell, which reduces the amount of incoming damage by 20%.
        Cooldown - 4 turns.

        Returns:
            tuple: cooldown of the spell, amount of turns for which it is active
        """
        turns_active = 2
        cooldown = 4
        spell_cost = math.ceil(self.max_secondary_pool * 5 / 100)
        self._current_damage_red = math.ceil(self.attack_power * 20 / 100)
        self._curr_mana -= spell_cost

        return cooldown, turns_active

    # ------------------------------------------------------------------------ #
    def cast_blade_of_justice(self) -> tuple:
        """
        Pierce the target with a blade of light, dealing percent damage based on the hero's attack power.
        Generates 3 Holy Power.
        Cooldown - 3 turns.

        Returns:
            tuple: damage of the spell, cooldown of the spell
        """
        cooldown = 3
        holy_power_generation = 1
        spell_damage = math.ceil(self.attack_power * 135 / 100)
        spell_cost = math.ceil(self.max_secondary_pool * 5 / 100)
        self.max_secondary_pool -= spell_cost
        self.add_specific_stat(holy_power_generation)

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_final_verdict(self) -> int:
        """
        Powerfull spell, dealing percent damage based on the hero's attack power.
        Cost - 3 Holy Power.

        Returns:
            tuple: damage of the spell
        """
        cost = 3
        if self.is_specific_stat_spent(cost):
            spell_damage = math.ceil(self.attack_power * 161 / 100)
            spell_cost = math.ceil(self.max_secondary_pool * 7 / 100)
            self.max_secondary_pool -= spell_cost

            return spell_damage
        else:
            pass  # TODO: do something

    # ------------------------------------------------------------------------ #
    def cast_wake_of_ashes(self) -> tuple:
        """
        Lash out at your enemies, dealing heavy weapon damage. Generates 3 Holy Power.
        Cooldown - 6 turns.

        Returns:
            tuple: spell damage, cooldown of the spell.
        """
        cooldown = 6
        holy_power_generated = 3
        spell_damage = math.ceil(self.attack_power * 293 / 100)
        spell_cost = math.ceil(self.max_secondary_pool * 15 / 100)
        self.max_secondary_pool -= spell_cost

        self.add_specific_stat(holy_power_generated)

        return spell_damage, cooldown


# ---------------------------------------------------------------------------- #
class ProtectionPaladinSpells(PaladinCommonSpells):
    """
    Class that handles the Protection Paladin spells.
    """

    def __init__(self):
        super().__init__()

        # self._curr_holy_power = 0
        # self._max_holy_power = 5
        # self._curr_health = self.health
        # self._max_mana = self._secondary_pool
        # self._base_damage_red = self.damage_reduction
        # self._current_damage_red = self.damage_reduction
        # self._max_damage_red = 100

    # ------------------------------------------------------------------------ #
    def cast_consecration(self) -> tuple:
        """
        Ignite the ground beneath you, dealing damage over time to your enemies.
        Turns active - 3.

        Returns:
            tuple: spell damage per turn, turns for which the spell is active
        """
        turns_active = 3
        spell_damage = math.ceil(self.attack_power * 30 / 100)
        spell_cost = math.ceil(self.max_secondary_pool * 5 / 100)
        self._curr_mana -= spell_cost

        return spell_damage, turns_active

    # ------------------------------------------------------------------------ #
    def cast_blessed_hammer(self) -> tuple:
        """
        Hurl a blessed hammer to your enemies, dealing holy damage and reducing
        damage taked by 30% from your attack power for 1 turn.

        Returns:
            tuple: damage of the spell, cooldown of the spell, turns for which is active
        """
        turns_active = 1
        holy_power_generation = 1
        cooldown = 2
        spell_damage = math.ceil(self.attack_power * 30 / 100)
        spell_cost = math.ceil(self.max_secondary_pool * 5 / 100)
        self._current_damage_red = math.ceil(self.attack_power * 30 / 100)
        self._curr_mana -= spell_cost

        self._add_holy_power(holy_pow_gen=holy_power_generation)

        return spell_damage, cooldown, turns_active

    # ------------------------------------------------------------------------ #
    def cast_shield_of_the_righteous(self) -> int:
        """
        Slam the enemy with your shield, dealing holy damage.
        Cost - 3 Holy Power.

        Returns:
            int: spell damage
        """
        holy_power_cost = 3
        if self._is_holy_power_spent(holy_pow_req=holy_power_cost):
            spell_damage = math.ceil(self.attack_power * 42 / 100)
            spell_cost = math.ceil(self.max_secondary_pool * 5 / 100)
            self._curr_mana -= spell_cost

            return spell_damage
        else:
            pass  # placeholder

    # ------------------------------------------------------------------------ #
    def cast_crusader_strike(self) -> int:
        """
        Strike the target, dealing holy damage. Generates 1 Holy Power.

        Returns:
            int: damage of the spell
        """
        holy_power_generation = 1
        spell_damage = math.ceil(self.attack_power * 110 / 100)
        spell_cost = math.ceil(self._max_mana * 5 / 100)
        self._curr_mana -= spell_cost
        self.add_specific_stat(holy_power_generation)

        return spell_damage
