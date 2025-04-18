import math

from Heroes.hero_base_stats import BaseHeroStats


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class CommonSpellsMixin:
    """
    Common Spells Mixin
    This class contains the common spells and abilities of the Monk.
    """

    def _is_chi_spent(self, chi_cost: int) -> bool:
        """
        Check if the player has enough chi to cast a spell.

        Args:
            chi_cost (int): The cost of the spell.

        Returns:
            bool: True if chi cost is spent, False otherwise.
        """
        if self._curr_chi >= chi_cost:
            self._curr_chi -= chi_cost
            return True

        return False

    # ------------------------------------------------------------------------ #
    def _add_generated_chi(self, chi_generated: int) -> None:
        """
        Adds the generated amount of chi to the currenlty available to the player. If the amount exceeds the maximum,
        the current chi is set to the maximum.

        Args:
            chi_generated (int): The amount of chi generated by the spell.
        """
        self._curr_chi += chi_generated

        self._curr_chi = min(self._curr_chi, self._max_chi)

    # ------------------------------------------------------------------------ #
    def _heal_up(self, heal_ammount: int) -> None:
        """
        Heal the target for a certain amount of health.

        Args:
            heal_ammount (int): The amount of health to heal.
        """
        self._health += heal_ammount

        self._health = min(self._health, self._max_health)

    # ------------------------------------------------------------------------ #
    def cast_spinning_crane_kick(self) -> tuple:
        """
        Spin while kicking in the air, dealing damage to all enemies in the area.

        Returns:
            _type_: _description_
        """
        cooldown = 2
        energy_cost = 40
        damage = math.ceil(self._attack_power * 40 / 100)
        self._secondary_pool -= energy_cost

        return damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_vivify(self) -> None:
        """
        Causes a surge of invigorating mists, healing the target for a certain amount of health.
        The amount of health healed is based on the spell power of the player.
        The spell costs 30 energy and heals for 258% of the spell power.
        The spell can only be cast if the player has enough energy to cast it.
        """

        energy_cost = 30
        amount_to_heal = math.ceil(self._spell_power * 258 / 100)
        if energy_cost >= self._secondary_pool:
            self._secondary_pool -= energy_cost
            self._heal_up(amount_to_heal)


# ---------------------------------------------------------------------------- #
class WindwalkerMonkSpells(BaseHeroStats, CommonSpellsMixin):
    # ------------------------------------------------------------------------ #
    """
    Windwalker Monk Spells
    This class contains the spells and abilities of the Windwalker Monk.
    The Windwalker Monk is a melee DPS spec that uses chi to cast spells and abilities.

    Args:
        BaseHeroStats (cls): _base class for all hero stats
        CommonSpellsMixin (cls): _mixin class for common spells
    """

    def __init__(self):
        super().__init__()
        self._curr_chi = 0
        self._max_chi = 5
        self._health = 800
        self._secondary_pool = 300
        self._attack_power = 65
        self._max_damage_red = 100
        self._max_health = self._health
        self._max_energy = self._secondary_pool
        self._base_damage_red = self._damage_reduction
        self._current_damage_red = self._damage_reduction

    # ------------------------------------------------------------------------ #
    def cast_tiger_palm(self):
        """
        Strike with the palm of you hand, dealing physical damage to the target. Generates 2 chi.

        Returns:
            tuple: spell damage, cooldown
        """
        cooldown = 1
        spell_cost = math.ceil(self._max_energy * 12 / 100)
        spell_damage = math.ceil(self._attack_power * 28 / 100)
        self._secondary_pool -= spell_cost
        self._add_generated_chi(chi_generated=2)

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_rising_sun_kick(self) -> tuple:
        """
        Kick upwards, dealing damage to the target, dealing physical damage

        Returns:
            tuple: spell damage, cooldown
        """
        spell_damage = 0
        cooldown = 1
        chi_cost = 2
        if self._is_chi_spent(chi_cost=chi_cost):
            spell_damage = math.ceil(self._attack_power * 28 / 100)

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_fists_of_fury(self) -> tuple:
        """
        Pummel all targets in front of you, dealing physical damage.

        Returns:
            tuple: spell damage, cooldown
        """
        spell_damage = 0
        cooldown = 2
        chi_cost = 3
        if self._is_chi_spent(chi_cost=chi_cost):
            spell_damage = math.ceil(self._attack_power * 138 / 100)

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_whirling_dragon_punch(self) -> tuple:
        """
        Perform a devastationg whirling upward stike, dealing damage to all targets in front of you.

        Returns:
            tuple: spell damage, cooldown
        """
        cooldown = 5
        spell_damage = math.ceil(self._attack_power * 230 / 100)

        return spell_damage, cooldown


# ---------------------------------------------------------------------------- #
class BrewmasterMonkSpells(BaseHeroStats, CommonSpellsMixin):
    # ------------------------------------------------------------------------ #
    """
    Brewmaster Monk Spells
    This class contains the spells and abilities of the Brewmaster Monk.
    The Brewmaster Monk is a tank spec that uses chi to cast spells and abilities.

    Args:
        BaseHeroStats (cls): _base class for all hero stats
        CommonSpellsMixin (cls): _mixin class for common spells
    """

    def __init__(self):
        super().__init__()
        self._curr_chi = 0
        self._max_chi = 5
        self._health = 1100
        self._secondary_pool = 200
        self._attack_power = 45
        self._attack_power = 30
        self._max_damage_red = 100
        self._max_health = self._health
        self._max_energy = self._secondary_pool
        self._base_damage_red = self._damage_reduction

    # ------------------------------------------------------------------------ #
    def cast_rushing_jade_wind(self) -> tuple:
        """
        Summon a swirling wind around you, dealing damage to all enemies in the area.

        Returns:
            tuple: spell damage, cooldown
        """
        chi_cost = 1
        spell_damage = 0
        cooldown = 1
        if self._is_chi_spent(chi_cost=chi_cost):
            spell_damage = math.ceil(self._attack_power * 14 / 100)

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_chi_burst(self) -> tuple:
        """
        Launch a burst of chi energy, dealing damage to all enemies in the area.

        Returns:
            tuple: spell damage, cooldown
        """
        cooldown = 7
        spell_damage = math.ceil(self._attack_power * 280 / 100)

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_keg_smash(self) -> tuple:
        """
        Smash the target with your keg, dealing damage to the target and reducing the damage taken by 30% for 1 turn.

        Returns:
            tuple: spell damage, cooldown
        """
        energy_cost = 40
        cooldown = 3
        spell_damage = math.ceil(self._attack_power * 100 / 100)
        self._secondary_pool -= energy_cost
        self._damage_reduction += 30  # TODO: reset the damage reduction after 1 turn

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_blackout_kick(self) -> tuple:
        """
        Kick the target with a blast of chi, dealing damage to the target.

        Returns:
            tuple: spell damage, cooldown
        """
        chi_cost = 3
        spell_damage = 0
        cooldown = 1
        if self._is_chi_spent(chi_cost=chi_cost):
            spell_damage = math.ceil(self._attack_power * 85 / 100)

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_breath_of_fire(self) -> tuple:
        """
        Breath fire on the target, dealing fire damage infront of the hero.

        Returns:
            tuple: spell damage, cooldown
        """
        cooldown = 5
        spell_damage = math.ceil(self._attack_power * 54 / 100)

        return spell_damage, cooldown
