import math

from Heroes.hero_base_stats import IBaseHero


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class ShamanCommonSpells(IBaseHero):
    """
    Common Spells Mixin
    This class contains the common spells and abilities of the Shaman.
    """

    # ------------------------------------------------------------------------ #
    def __init__(self):
        super().__init__()
        self._curr_maelstrom_stacks = 0
        self._max_maelstrom_stacks = 5
        self._curr_health = self.max_health
        self._curr_mana = self.max_secondary_pool
        self._current_damage_red = self.damage_reduction

    # ------------------------------------------------------------------------ #
    @staticmethod
    def __is_flame_shock_active(active_spells: list) -> bool:
        if "flame_shock" in active_spells:
            return True

        return False

    # ------------------------------------------------------------------------ #
    def cast_lighting_bolt(self) -> tuple:
        """
        Hurls a bolt of lightning at the target, dealing nature damage.

        Returns:
            tuple: spell damage, cooldown

        """
        cooldown = 1
        spell_cost = math.ceil(self.max_secondary_pool * 4 / 100)
        spell_damage = math.ceil(self.spell_power * 131 / 100)
        self._secondary_pool -= spell_cost

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_flame_shock(self) -> tuple:
        """
        Sears the target with fire, causing initial damage and then dealing damage over time.

        Returns:
            tuple: initial spell damage, damage over time, cooldown, turns active

        """
        cooldown = 5
        turns_active = 3
        spell_cost = math.ceil(self._max_mana * 5 / 100)
        initial_spell_damage = math.ceil(self.spell_power * 30 / 100)
        damage_over_time = math.ceil(self.spell_power * 120 / 100)
        self._secondary_pool -= spell_cost

        return initial_spell_damage, damage_over_time, cooldown, turns_active

    # ------------------------------------------------------------------------ #
    def cast_primordial_wave(self) -> tuple:
        """
        Blast the target with a Primordial Wave of energy, dealing elemental damage.

        Returns:
            tuple: spell damage, cooldown

        """
        cooldown = 7
        spell_cost = math.ceil(self.max_secondary_pool * 5 / 100)
        spell_damage = math.ceil(self.spell_power * 525 / 100)
        self._secondary_pool -= spell_cost

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_lava_burst(self, active_spells: list) -> tuple:
        """
        Hurls a molten lava ball towards the target, dealing fire damage. Lava Burst will
        always critically strike if the target is affected by Flame Shock.

        Returns:
            tuple: spell damage, cooldown

        """
        cooldown = 2
        spell_cost = math.ceil(self.max_secondary_pool * 5 / 100)
        spell_damage = math.ceil(self.spell_power * 140 / 100)
        self._secondary_pool -= spell_cost

        if self.__is_flame_shock_active(active_spells):
            spell_damage *= 2

        return spell_damage, cooldown

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
        Checks the current amount of maelstrom stacks available to the hero.
        If the maelstrom stacks goes beyond the max maelstrom stacks, the current maelstrom stacks are set to the max

        Args:
            stat_value (int): Add the maelstrom stack to the amount currently available.
        """

        self._curr_maelstrom_stacks += stat_value

        if self._curr_maelstrom_stacks >= self._max_maelstrom_stacks:
            self._curr_maelstrom_stacks = self._max_maelstrom_stacks

    # ------------------------------------------------------------------------ #
    def is_specific_stat_spent(self, stat_value: int) -> bool:
        """
        Boolean check if the hero has enough maelstrom stacks for the spell that was casted.

        Args:
            stat_value (int): cost of the spell

        Returns:
            bool: returns True if there are enough maelstrom stacks for the spell, otherwise returns False
        """
        if self._curr_maelstrom_stacks >= stat_value:
            self._curr_maelstrom_stacks -= stat_value
            return True
        else:
            return False


# ---------------------------------------------------------------------------- #
class EnhancementShamanSpells(ShamanCommonSpells):
    """
    Enhancement Shaman Spells
    This class contains the spells and abilities of the Enhancement Shaman.
    """

    def __init__(self):
        super().__init__()

    # ------------------------------------------------------------------------ #
    def cast_stormstrike(self) -> tuple:
        """
        Energizes both weapons with lightning and delivers a massive blow to your target,
        dealing Physical damage.

        Returns:
            tuple: spell damage, cooldown

        """

        cooldown = 2
        spell_cost = math.ceil(self.max_secondary_pool * 5 / 100)
        spell_damage = math.ceil(self.attack_power * 400 / 100)
        self._secondary_pool -= spell_cost

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_lava_lash(self) -> tuple:
        """
        Charges your off-hand weapon with lava and burns your target, dealing Fire damage.

        Returns:
            tuple: spell damage, cooldown

        """

        cooldown = 2
        spell_cost = math.ceil(self.max_secondary_pool * 3 / 100)
        spell_damage = math.ceil(self.attack_power * 240 / 100)
        self._secondary_pool -= spell_cost

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_tempest(self) -> tuple:
        """
        Calls down a tremendous lightning strike, dealing Nature damage to you target.

        Returns:
            tuple: spell damage, cooldown

        """

        cooldown = 5
        spell_cost = math.ceil(self.max_secondary_pool * 3 / 100)
        spell_damage = math.ceil(self.attack_power * 310 / 100)
        self._secondary_pool -= spell_cost

        return spell_damage, cooldown

    # ------------------------------------------------------------------------ #
    def cast_feral_spirit(self) -> tuple:
        """
        Summon two Spirit Wolves to fight by your side for 4 turns.

        Returns:
            tuple: spell damage, cooldown, turns active

        """

        cooldown = 8
        turns_active = 4
        spell_cost = math.ceil(self.max_secondary_pool * 5 / 100)
        spell_damage = math.ceil(self.attack_power * 80 / 100) + math.ceil(
            self.spell_power * 80 / 100
        )
        self._secondary_pool -= spell_cost

        return spell_damage, cooldown, turns_active


# ---------------------------------------------------------------------------- #
class ElementalShamanSpells(ShamanCommonSpells):
    """
    Elemental Shaman Spells
    This class contains the spells and abilities of the Elemental Shaman.
    """

    def __init__(self):
        super().__init__()

    # ------------------------------------------------------------------------ #
    def cast_earth_shock(self):
        """
        Instantly shocks the target with concussive force, dealing Nature damage.

        Returns:
            tuple: spell damage, cooldown
        """

        cooldown = 3
        spell_cost = math.ceil(self.max_secondary_pool * 10 / 100)
        spell_damage = math.ceil(self.spell_power * 550 / 100)
        self._secondary_pool -= spell_cost

        return spell_damage, cooldown
