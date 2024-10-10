"""
Handler library, used to cast different types of Paladin spells, based on the selected role of the hero.
"""
import math

from Heroes.hero_base_stats import BaseHeroStats


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class CommonSpellsMixin:

    # ------------------------------------------------------------------------ #
    def cast_divine_shield(self):
        """
        Powerfull protection spell, which block all incoming damage for 2 turns.
        Cooldown - 15 turns.

        Returns:
            tuple: cooldown of the spell and for how many turns it is active
        """
        cooldown = 15
        self._current_damage_red = self._max_damage_red
        turns_active = 2

        return cooldown, turns_active

    # ------------------------------------------------------------------------ #
    def cast_judgement(self):
        """
        Judges the target, dealing damage based on the hero's attack power. Generates 1 Holy Power.

        Returns:
            tuple: damage of the spell, cooldown of the spell
        """
        cooldown = 3
        holy_power_generation = 1
        spell_damage          = math.ceil(self._attack_power * 61 / 100)
        spell_cost            = math.ceil(self._current_mana * 5 / 100)
        self._current_mana   -= spell_cost
        self._check_holy_power(holy_power_generation)

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
            self._heal_up(amount_to_heal)

        self._check_holy_power()

    # ------------------------------------------------------------------------ #
    def display_amount_of_holy_power(self):
        """
        Outputs the current spell power in the terminal
        """
        print(f"Holy power: {self._curr_holy_power}")

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
    def _check_holy_power(self, holy_pow_gen: int = 0):
        """
        Checks the current amount of holy power available to the hero.
        If the value goes below 0, the holy power is set to 0.
        If the holy power goes beyond the max holy power, the current holy power is set to the max

        Args:
            holy_pow_gen (int, optional): _description_. Defaults to 0.
        """

        self._curr_holy_power += holy_pow_gen

        if self._curr_holy_power < 0:
            self._curr_holy_power = 0

        elif self._curr_holy_power + holy_pow_gen >= self._max_holy_power:
            print("MAX holy power!")
            self._curr_holy_power = self._max_holy_power

    # ------------------------------------------------------------------------ #
    def _is_holy_power_spent(self, holy_pow_req: int):
        """
        Boolean check if the hero has enough holy power for the spell that was casted.

        Args:
            holy_pow_req (int): cost of the spell

        Returns:
            bool: returns True if there's enough spell power for the spell, otherwise returns False
        """
        if self._curr_holy_power < holy_pow_req:
            return False
        elif self._curr_holy_power >= holy_pow_req:
            self._curr_holy_power -= holy_pow_req
            self._check_holy_power()
            return True


# ---------------------------------------------------------------------------- #
class RetributionPaladinSpells(CommonSpellsMixin, BaseHeroStats):

    # ------------------------------------------------------------------------ #
    def __init__(self):
        self._curr_holy_power       = 0
        self._max_holy_power        = 5
        self._health                = 800
        self._secondary_pool        = 300
        self._spell_power           = 30
        self._attack_power          = 75
        self._max_health            = self._health
        self._max_mana              = self._secondary_pool
        self._base_damage_red       = self._damage_reduction
        self._current_damage_red    = self._damage_reduction
        self._max_damage_red        = 100

    # ------------------------------------------------------------------------ #
    def cast_divine_protection(self):
        """
        Protection spell, which reduces the amount of incoming damage by 20%.
        Cooldown - 4 turns.

        Returns:
            tuple: cooldown of the spell, amount of turns for which it is active
        """
        turns_active = 2
        cooldown = 4
        spell_cost                 = math.ceil(self._max_mana * 5 / 100)
        self._current_damage_red   = math.ceil(self._attack_power * 20 / 100)
        self._secondary_pool      -= spell_cost

        return cooldown, turns_active

    # ------------------------------------------------------------------------ #
    def cast_blade_of_justice(self):
        """
        Pierce the target with a blade of light, dealing percent damage based on the hero's attack power.
        Generates 3 Holy Power.
        Cooldown - 3 turns.

        Returns:
            tuple: damage of the spell, cooldown of the spell
        """
        cooldown              = 3
        holy_power_generation = 1
        spell_damage          = math.ceil(self._attack_power * 135 / 100)
        spell_cost            = math.ceil(self._max_mana * 5 / 100)
        self._secondary_pool   -= spell_cost
        self._check_holy_power(holy_power_generation)

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_final_verdict(self):
        """
        Powerfull spell, dealing percent damage based on the hero's attack power.
        Cost - 3 Holy Power.

        Returns:
            tuple: damage of the spell
        """
        cost = 3
        if self._is_holy_power_spent(holy_pow_req=cost):
            spell_damage          = math.ceil(self._attack_power * 161 / 100)
            spell_cost            = math.ceil(self._max_mana * 7 / 100)
            self._secondary_pool   -= spell_cost

            return spell_damage
        else:
            pass  # TODO: do something

    # ------------------------------------------------------------------------ #
    def cast_wake_of_ashes(self):
        """
        Lash out at your enemies, dealing heavy weapon damage. Generates 3 Holy Power.
        Cooldown - 6 turns.

        Returns:
            tuple: spell damage, cooldown of the spell.
        """
        cooldown = 6
        holy_power_generation = 3
        spell_damage          = math.ceil(self._attack_power * 293 / 100)
        spell_cost            = math.ceil(self._max_mana * 15 / 100)
        self._secondary_pool   -= spell_cost

        self._check_holy_power(holy_power_generation)

        return spell_damage, cooldown


# ---------------------------------------------------------------------------- #
class ProtectionPaladinSpells(CommonSpellsMixin, BaseHeroStats):
    def __init__(self):
        self._curr_holy_power       = 0
        self._max_holy_power        = 5
        self._health                = 1200
        self._secondary_pool        = 300
        self._spell_power           = 30
        self._attack_power          = 45
        self._max_health            = self._health
        self._max_mana              = self._secondary_pool
        self._base_damage_red       = self._damage_reduction
        self._current_damage_red    = self._damage_reduction
        self._max_damage_red        = 100

    # ------------------------------------------------------------------------ #
    def cast_consecration(self):
        """
        Ignite the ground beneath you, dealing damage over time to your enemies.
        Turns active - 3.

        Returns:
            tuple: spell damage per turn, turns for which the spell is active
        """
        turns_active         = 3
        spell_damage         = math.ceil(self._attack_power * 30 / 100)
        spell_cost           = math.ceil(self._max_mana * 5 / 100)
        self._secondary_pool  -= spell_cost

        return spell_damage, turns_active

    # ------------------------------------------------------------------------ #
    def cast_blessed_hammer(self):
        """
        Hurl a blessed hammer to your enemies, dealing holy damage and reducing
        damage taked by 30% from your attack power for 1 turn.

        Returns:
            tuple: damage of the spell, cooldown of the spell, turns for which is active
        """
        turns_active               = 1
        holy_power_generation      = 1
        cooldown                   = 2
        spell_damage               = math.ceil(self._attack_power * 30 / 100)
        spell_cost                 = math.ceil(self._max_mana * 5 / 100)
        self._current_damage_red   = math.ceil(self._attack_power * 30 / 100)
        self._secondary_pool        -= spell_cost

        self._check_holy_power(holy_pow_gen=holy_power_generation)

        return spell_damage, cooldown, turns_active

    # ------------------------------------------------------------------------ #
    def cast_shield_of_the_righteous(self):
        """
        Slam the enemy with your shield, dealing holy damage. 
        Cost - 3 Holy Power.

        Returns:
            int: spell damage
        """
        holy_power_cost     = 3
        if self._is_holy_power_spent(holy_pow_req=holy_power_cost):
            spell_damage          = math.ceil(self._attack_power * 42 / 100)
            spell_cost            = math.ceil(self._max_mana * 5 / 100)
            self._secondary_pool -= spell_cost

            return spell_damage
        else:
            pass  # placeholder

    # ------------------------------------------------------------------------ #
    def cast_crusader_strike(self):
        """
        Strike the target, dealing holy damage. Generates 1 Holy Power.

        Returns:
            tuple: damage of the spell
        """
        holy_power_generation   = 1
        spell_damage            = math.ceil(self._attack_power * 110 / 100)
        spell_cost              = math.ceil(self._max_mana * 5 / 100)
        self._secondary_pool     -= spell_cost
        self._check_holy_power(holy_power_generation)

        return spell_damage
