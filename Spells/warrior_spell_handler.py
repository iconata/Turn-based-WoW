import math

from Heroes.hero_base_stats import IBaseHero


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class CommonSpellsMixin:
    """
    Common Spells Mixin
    This class contains the common spells and abilities of the Warrior.
    """

    # ------------------------------------------------------------------------ #
    def is_rage_spent(self, spell_cost: float) -> bool:
        if self._curr_rage >= spell_cost:
            self._curr_rage -= spell_cost
            return True

        return False

    # ------------------------------------------------------------------------ #
    def check_max_health(self, heal_ammount: float) -> None:
        """
        Check if the amount of incoming heal will overheal and the max health will
        be exceeded. If so, set the health to the max health.
        If not, add the heal amount to the current health.

        Args:
            heal_ammount (float): amount of incoming heal
        """

        if self._health + heal_ammount > self._max_health:
            self._health = self._max_health
        else:
            self._health += heal_ammount

    # ------------------------------------------------------------------------ #
    def check_max_rage(self, rage_ammount: int) -> None:
        """
        Checks if the amount of generated rage will exceed the max rage.
        If so, set the rage to the max rage.

        Args:
            rage_ammount (int): amount of generated rage
        """

        if self._curr_rage + rage_ammount > self._max_rage:
            self._curr_rage = self._max_rage
        else:
            self._curr_rage += rage_ammount


# ---------------------------------------------------------------------------- #
class FuryWarriorSpells(IBaseHero, CommonSpellsMixin):
    # ------------------------------------------------------------------------ #
    def __init__(self):
        """
        Fury Warrior Spells.
        This class contains the spells and abilities of the Fury Warrior.
        It inherits from the IBaseHero class and implements the spells and abilities of the Fury Warrior.
        """

        super().__init__()
        self._curr_rage = 0
        self._health = 1000
        self._secondary_pool = 200
        self._attack_power = 70
        self._max_health = self._health
        self._max_rage = self._secondary_pool
        self._current_damage_red = self._damage_reduction
        self._max_damage_red = 100

    # ------------------------------------------------------------------------ #
    def cast_bladestorm(self) -> dict:
        """
        Become and unstoppable storm of destructive force, striking your enemy,
        dealing Physiscal damage.

        Returns:
            dict: spell damage, cooldown
        """
        rage_generated = 10
        self.check_max_rage(rage_generated)

        spell_attributes = {
            "spell_cost": None,
            "spell_damage": math.ceil(self._attack_power * 140 / 100),
            "cooldown": 8,
        }

        return spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_rampage(self) -> dict:
        """
        Enrages you and unleashes a flurry of brutal attacks, dealing Physical damage.
        The spell requires 80 rage to cast.

        Returns:
            dict: spell_cost, spell_damage
        """

        spell_attributes = {
            "spell_cost": 80,
            "spell_damage": math.ceil(self._attack_power * 230 / 100),
        }

        return (
            spell_attributes
            if self.is_rage_spent(spell_attributes["spell_cost"])
            else None
        )

    # ------------------------------------------------------------------------ #
    def cast_bloodbath(self) -> dict:
        """
        Assault the target in a bloodthirsty craze, dealing Physical damage and
        restoring 3% of your health.

        Returns:
            dict: spell_cost, spell_damage, cooldown
        """
        rage_generated = 8
        health_restored = math.ceil(self._health * 3 / 100)

        self.check_max_rage(rage_generated)
        self.check_max_health(health_restored)

        spell_attributes = {
            "spell_cost": None,
            "spell_damage": math.ceil(self._attack_power * 390 / 100),
            "cooldown": 3,
        }

        return spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_raging_blow(self) -> dict:
        """
        A might blow with both weapons, that deals Physical damage.

        Returns:
            dict: spell_cost, spell_damage, cooldown
        """

        rage_generated = 12
        self.check_max_rage(rage_generated)

        spell_attributes = {
            "spell_cost": None,
            "spell_damage": math.ceil(self._attack_power * 400 / 100),
            "cooldown": 4,
        }

        return spell_attributes


# ---------------------------------------------------------------------------- #
class ProtectionWarriorSpells(IBaseHero, CommonSpellsMixin):
    # ------------------------------------------------------------------------ #
    def __init__(self):
        """
        Protection Warrior Spells.
        This class contains the spells and abilities of the Protection Warrior.
        It inherits from the IBaseHero class and implements the spells and abilities of the Protection Warrior.
        """

        super().__init__()
        self._curr_rage = 0
        self._health = 1500
        self._secondary_pool = 200
        self._attack_power = 50
        self._max_health = self._health
        self._max_rage = self._secondary_pool
        self._current_damage_red = self._damage_reduction
        self._max_damage_red = 100

    # ------------------------------------------------------------------------ #
    def cast_charge(self) -> dict:
        """
        Charge to an enemy dealing physical damage and generating 20 rage.

        Returns:
            dict: spell_cost, spell_damage, cooldown
        """

        rage_generated = 20
        self.check_max_rage(rage_generated)

        spell_attributes = {
            "spell_cost": None,
            "spell_damage": math.ceil(self._attack_power * 50 / 100),
            "cooldown": 7,
        }

        return spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_shield_block(self) -> dict:
        """
        Raise your shield, blocking 100% of incoming damage for 2 turns.

        Returns:
            dict: spell_cost, damage_reduction, cooldown
        """

        if self.is_rage_spent(spell_cost=30):
            spell_attributes = {
                "spell_cost": 30,
                "damage_reduction": self._max_damage_red,
                "cooldown": 2,
            }

            return spell_attributes
        else:
            return None

    # ------------------------------------------------------------------------ #
    def cast_champions_spear(self) -> dict:
        """
        Throw a spear at the target, dealing Physical damage and generating 10 rage.

        Returns:
            dict: spell_damage, cooldown
        """

        rage_generated = 10
        self.check_max_rage(rage_generated)

        self._spell_attributes["spell_damage"] = math.ceil(
            self._attack_power * 240 / 100
        )
        self._spell_attributes["cooldown"] = 10

        return self._spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_shield_charge(self) -> dict:
        """
        Charge to an enemy with your shield, dealing Physical damage and generating 20 rage.

        Returns:
            dict: spell_cost, spell_damage, cooldown
        """

        rage_generated = 20
        self.check_max_rage(rage_generated)

        spell_attributes = {
            "spell_cost": None,
            "spell_damage": math.ceil(self._attack_power * 420 / 100),
            "cooldown": 8,
        }

        return spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_sheild_slam(self) -> dict:
        """
        Slams the target with your shield, dealing Physical damage and generating 15 rage.

        Returns:
            dict: spell_cost, spell_damage, cooldown
        """

        rage_generated = 15
        self.check_max_rage(rage_generated)

        spell_attributes = {
            "spell_cost": None,
            "spell_damage": math.ceil(self._attack_power * 130 / 100),
            "cooldown": 2,
        }

        return spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_ignore_pain(self) -> dict:
        """
        Fight through the pain, ingoring 50% of incoming damage for 1 turn.
        This spell costs 35 rage to cast.

        Returns:
            dict: spell_cost, damage_reduction, cooldown, turns_active
        """

        if self.is_rage_spent(spell_cost=35):
            self._current_damage_red += 50
            spell_attributes = {
                "spell_cost": 35,
                "damage_reduction": self._current_damage_red,
                "cooldown": 0,
                "turns_active": 1,
            }

            return spell_attributes
        else:
            return None


# -------------------------------- End of file ------------------------------- #
