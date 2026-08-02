"""Per-class spell contract tests.

Each test verifies that a spell:
- Returns a dict (or None when a resource requirement is not met).
- Populates the expected keys with sensible values.
- Correctly handles resource costs (mana, rage, chi, holy power, etc.).
- Does not mutate the shared ``spell_attributes`` template on the class.
"""

import pytest

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
# Helpers
# ---------------------------------------------------------------------------- #

REQUIRED_KEYS = {
    "spell_cost",
    "spell_damage",
    "cooldown",
    "turns_active",
    "damage_reduction",
    "initial_spell_damage",
    "health_leech",
    "damage_over_time",
}


def assert_spell_contract(info: dict) -> None:
    """Assert that a spell result dict contains all required contract keys."""
    assert isinstance(info, dict), "Spell must return a dict"
    for key in REQUIRED_KEYS:
        assert key in info, f"Missing key '{key}' in spell result"


def template_not_mutated(hero) -> None:
    """Assert that the class-level spell_attributes template is still all zeros."""
    for key, value in hero.spell_attributes.items():
        assert value == 0, (
            f"spell_attributes template was mutated: {key}={value}"
        )


# ---------------------------------------------------------------------------- #
# Fire Mage
# ---------------------------------------------------------------------------- #

class TestFireMageSpells:
    """Spell contract tests for FireMageSpells."""

    def setup_method(self):
        self.hero = FireMageSpells()
        self.hero.max_health = 700
        self.hero.max_secondary_pool = 900
        self.hero.spell_power = 110
        self.hero._curr_health = self.hero.max_health
        self.hero._curr_mana = self.hero.max_secondary_pool

    def test_fireball_contract(self):
        """cast_fireball returns a valid contract dict with damage and cooldown."""
        info = self.hero.cast_fireball()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0
        assert info["spell_cost"] > 0

    def test_fireball_deducts_mana(self):
        """cast_fireball deducts mana from the caster."""
        before = self.hero._curr_mana
        info = self.hero.cast_fireball()
        assert self.hero._curr_mana == before - info["spell_cost"]

    def test_fireball_heals_caster(self):
        """cast_fireball heals the caster for 1% of max health."""
        self.hero._curr_health = self.hero.max_health - 100
        before = self.hero._curr_health
        self.hero.cast_fireball()
        assert self.hero._curr_health >= before

    def test_fire_blast_contract(self):
        """cast_fire_blast returns a valid contract dict with damage reduction."""
        info = self.hero.cast_fire_blast()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["damage_reduction"] > 0
        assert info["turns_active"] > 0

    def test_flamestrike_contract(self):
        """cast_flamestrike returns a valid contract dict with DOT and cooldown."""
        info = self.hero.cast_flamestrike()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0
        assert info["turns_active"] > 0

    def test_polymorph_contract(self):
        """cast_polymorph returns a valid contract dict with turns_active."""
        info = self.hero.cast_polymorph()
        assert_spell_contract(info)
        assert info["turns_active"] > 0
        assert info["cooldown"] > 0

    def test_arcane_intellect_contract(self):
        """cast_arcane_intellect returns a valid contract dict."""
        info = self.hero.cast_arcane_intellect()
        assert_spell_contract(info)
        assert info["turns_active"] > 0

    def test_fire_stacks_double_damage(self):
        """Reaching max fire stacks doubles the next fireball's damage."""
        self.hero._curr_fire_stacks = self.hero._max_fire_stacks
        info = self.hero.cast_fireball()
        import math
        base = math.ceil(self.hero.spell_power * 155 / 100)
        assert info["spell_damage"] == base * 2

    def test_template_not_mutated(self):
        """Casting spells must not mutate the shared spell_attributes template."""
        self.hero.cast_fireball()
        self.hero.cast_fire_blast()
        template_not_mutated(self.hero)


# ---------------------------------------------------------------------------- #
# Windwalker Monk
# ---------------------------------------------------------------------------- #

class TestWindwalkerMonkSpells:
    """Spell contract tests for WindwalkerMonkSpells."""

    def setup_method(self):
        self.hero = WindwalkerMonkSpells()
        self.hero.max_health = 800
        self.hero.max_secondary_pool = 300
        self.hero.attack_power = 65
        self.hero._curr_health = self.hero.max_health
        self.hero._curr_energy = self.hero.max_secondary_pool

    def test_tiger_palm_contract(self):
        """cast_tiger_palm returns a valid contract dict with damage and generates chi."""
        before_chi = self.hero._curr_chi
        info = self.hero.cast_tiger_palm()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert self.hero._curr_chi > before_chi

    def test_rising_sun_kick_without_chi(self):
        """cast_rising_sun_kick returns zero damage when chi is insufficient."""
        self.hero._curr_chi = 0
        info = self.hero.cast_rising_sun_kick()
        assert_spell_contract(info)
        assert info["spell_damage"] == 0

    def test_rising_sun_kick_with_chi(self):
        """cast_rising_sun_kick deals damage when chi requirement is met."""
        self.hero._curr_chi = 2
        info = self.hero.cast_rising_sun_kick()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0

    def test_fists_of_fury_without_chi(self):
        """cast_fists_of_fury returns zero damage when chi is insufficient."""
        self.hero._curr_chi = 0
        info = self.hero.cast_fists_of_fury()
        assert_spell_contract(info)
        assert info["spell_damage"] == 0

    def test_fists_of_fury_with_chi(self):
        """cast_fists_of_fury deals damage when chi requirement is met."""
        self.hero._curr_chi = 3
        info = self.hero.cast_fists_of_fury()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0

    def test_whirling_dragon_punch_contract(self):
        """cast_whirling_dragon_punch returns a valid contract dict with high damage."""
        info = self.hero.cast_whirling_dragon_punch()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0

    def test_template_not_mutated(self):
        """Casting spells must not mutate the shared spell_attributes template."""
        self.hero.cast_tiger_palm()
        self.hero.cast_whirling_dragon_punch()
        template_not_mutated(self.hero)


# ---------------------------------------------------------------------------- #
# Brewmaster Monk
# ---------------------------------------------------------------------------- #

class TestBrewmasterMonkSpells:
    """Spell contract tests for BrewmasterMonkSpells."""

    def setup_method(self):
        self.hero = BrewmasterMonkSpells()
        self.hero.max_health = 1100
        self.hero.max_secondary_pool = 200
        self.hero.attack_power = 45
        self.hero._curr_health = self.hero.max_health
        self.hero._curr_energy = self.hero.max_secondary_pool

    def test_keg_smash_contract(self):
        """cast_keg_smash returns damage and a damage_reduction value."""
        info = self.hero.cast_keg_smash()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["damage_reduction"] > 0

    def test_chi_burst_contract(self):
        """cast_chi_burst returns a valid contract dict with high damage."""
        info = self.hero.cast_chi_burst()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0

    def test_rushing_jade_wind_without_chi(self):
        """cast_rushing_jade_wind returns zero damage when chi is insufficient."""
        self.hero._curr_chi = 0
        info = self.hero.cast_rushing_jade_wind()
        assert_spell_contract(info)
        assert info["spell_damage"] == 0

    def test_rushing_jade_wind_with_chi(self):
        """cast_rushing_jade_wind deals damage when chi requirement is met."""
        self.hero._curr_chi = 1
        info = self.hero.cast_rushing_jade_wind()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0

    def test_blackout_kick_with_chi(self):
        """cast_blackout_kick deals damage when chi requirement is met."""
        self.hero._curr_chi = 3
        info = self.hero.cast_blackout_kick()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0

    def test_breath_of_fire_contract(self):
        """cast_breath_of_fire returns a valid contract dict."""
        info = self.hero.cast_breath_of_fire()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0

    def test_template_not_mutated(self):
        """Casting spells must not mutate the shared spell_attributes template."""
        self.hero.cast_keg_smash()
        self.hero.cast_chi_burst()
        template_not_mutated(self.hero)


# ---------------------------------------------------------------------------- #
# Retribution Paladin
# ---------------------------------------------------------------------------- #

class TestRetributionPaladinSpellContracts:
    """Spell contract tests for RetributionPaladinSpells."""

    def setup_method(self):
        self.hero = RetributionPaladinSpells()
        self.hero.max_health = 800
        self.hero.max_secondary_pool = 300
        self.hero.spell_power = 30
        self.hero.attack_power = 75
        self.hero._curr_health = self.hero.max_health
        self.hero._curr_mana = self.hero.max_secondary_pool

    def test_judgement_contract(self):
        """cast_judgement returns damage and generates holy power."""
        before_hp = self.hero._curr_holy_power
        info = self.hero.cast_judgement()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert self.hero._curr_holy_power > before_hp

    def test_divine_protection_contract(self):
        """cast_divine_protection returns damage_reduction and turns_active."""
        info = self.hero.cast_divine_protection()
        assert_spell_contract(info)
        assert info["damage_reduction"] > 0
        assert info["turns_active"] > 0

    def test_blade_of_justice_contract(self):
        """cast_blade_of_justice returns damage and generates holy power."""
        before_hp = self.hero._curr_holy_power
        info = self.hero.cast_blade_of_justice()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert self.hero._curr_holy_power > before_hp

    def test_final_verdict_without_holy_power(self):
        """cast_final_verdict returns None when holy power is insufficient."""
        self.hero._curr_holy_power = 0
        result = self.hero.cast_final_verdict()
        assert result is None

    def test_final_verdict_with_holy_power(self):
        """cast_final_verdict returns a valid contract dict when holy power is sufficient."""
        self.hero._curr_holy_power = 3
        info = self.hero.cast_final_verdict()
        assert info is not None
        assert_spell_contract(info)
        assert info["spell_damage"] > 0

    def test_wake_of_ashes_contract(self):
        """cast_wake_of_ashes returns damage and generates 3 holy power."""
        self.hero._curr_holy_power = 0
        info = self.hero.cast_wake_of_ashes()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert self.hero._curr_holy_power == 3

    def test_template_not_mutated(self):
        """Casting spells must not mutate the shared spell_attributes template."""
        self.hero.cast_judgement()
        self.hero.cast_blade_of_justice()
        template_not_mutated(self.hero)


# ---------------------------------------------------------------------------- #
# Protection Paladin
# ---------------------------------------------------------------------------- #

class TestProtectionPaladinSpellContracts:
    """Spell contract tests for ProtectionPaladinSpells."""

    def setup_method(self):
        self.hero = ProtectionPaladinSpells()
        self.hero.max_health = 1200
        self.hero.max_secondary_pool = 300
        self.hero.spell_power = 30
        self.hero.attack_power = 45
        self.hero._curr_health = self.hero.max_health
        self.hero._curr_mana = self.hero.max_secondary_pool

    def test_consecration_contract(self):
        """cast_consecration returns damage and turns_active."""
        info = self.hero.cast_consecration()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["turns_active"] > 0

    def test_blessed_hammer_contract(self):
        """cast_blessed_hammer returns damage and generates holy power."""
        before_hp = self.hero._curr_holy_power
        info = self.hero.cast_blessed_hammer()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert self.hero._curr_holy_power > before_hp

    def test_shield_of_the_righteous_without_holy_power(self):
        """cast_shield_of_the_righteous returns None when holy power is insufficient."""
        self.hero._curr_holy_power = 0
        result = self.hero.cast_shield_of_the_righteous()
        assert result is None

    def test_shield_of_the_righteous_with_holy_power(self):
        """cast_shield_of_the_righteous returns a valid contract dict when holy power is sufficient."""
        self.hero._curr_holy_power = 3
        info = self.hero.cast_shield_of_the_righteous()
        assert info is not None
        assert_spell_contract(info)
        assert info["spell_damage"] > 0

    def test_crusader_strike_contract(self):
        """cast_crusader_strike returns damage and generates holy power."""
        before_hp = self.hero._curr_holy_power
        info = self.hero.cast_crusader_strike()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert self.hero._curr_holy_power > before_hp

    def test_divine_shield_contract(self):
        """cast_divine_shield returns full damage reduction for 2 turns."""
        info = self.hero.cast_divine_shield()
        assert_spell_contract(info)
        assert info["damage_reduction"] == self.hero.max_damage_reduction
        assert info["turns_active"] == 2

    def test_template_not_mutated(self):
        """Casting spells must not mutate the shared spell_attributes template."""
        self.hero.cast_consecration()
        self.hero.cast_crusader_strike()
        template_not_mutated(self.hero)


# ---------------------------------------------------------------------------- #
# Shadow Priest
# ---------------------------------------------------------------------------- #

class TestShadowPriestSpells:
    """Spell contract tests for ShadowPriestSpells."""

    def setup_method(self):
        self.hero = ShadowPriestSpells()
        self.hero.max_health = 750
        self.hero.max_secondary_pool = 900
        self.hero.spell_power = 90
        self.hero._curr_health = self.hero.max_health
        self.hero._curr_mana = self.hero.max_secondary_pool

    def test_mind_blast_contract(self):
        """cast_mind_blast returns damage and a cooldown."""
        info = self.hero.cast_mind_blast()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0

    def test_mind_blast_deducts_mana(self):
        """cast_mind_blast deducts mana from the caster."""
        before = self.hero._curr_mana
        info = self.hero.cast_mind_blast()
        assert self.hero._curr_mana == before - info["spell_cost"]

    def test_shadow_word_death_contract(self):
        """cast_shadow_word_death returns damage and a cooldown."""
        info = self.hero.cast_shadow_word_death()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0

    def test_devouring_plague_contract(self):
        """cast_devouring_plague returns initial damage, DOT, leech, and turns_active."""
        info = self.hero.cast_devouring_plague()
        assert_spell_contract(info)
        assert info["initial_spell_damage"] > 0
        assert info["damage_over_time"] > 0
        assert info["health_leech"] > 0
        assert info["turns_active"] > 0

    def test_flash_heal_restores_health(self):
        """cast_flash_heal heals the caster."""
        self.hero._curr_health = self.hero.max_health // 2
        before = self.hero._curr_health
        self.hero.cast_flash_heal()
        assert self.hero._curr_health > before

    def test_flash_heal_does_not_overheal(self):
        """cast_flash_heal does not exceed max health."""
        self.hero._curr_health = self.hero.max_health
        self.hero.cast_flash_heal()
        assert self.hero._curr_health <= self.hero.max_health

    def test_power_word_shield_contract(self):
        """cast_power_word_shield returns full damage reduction for 2 turns."""
        info = self.hero.cast_power_word_shield()
        assert_spell_contract(info)
        assert info["damage_reduction"] == self.hero.max_damage_reduction
        assert info["turns_active"] > 0

    def test_template_not_mutated(self):
        """Casting spells must not mutate the shared spell_attributes template."""
        self.hero.cast_mind_blast()
        self.hero.cast_devouring_plague()
        template_not_mutated(self.hero)


# ---------------------------------------------------------------------------- #
# Enhancement Shaman
# ---------------------------------------------------------------------------- #

class TestEnhancementShamanSpells:
    """Spell contract tests for EnhancementShamanSpells."""

    def setup_method(self):
        self.hero = EnhancementShamanSpells()
        self.hero.max_health = 850
        self.hero.max_secondary_pool = 300
        self.hero.attack_power = 35
        self.hero.spell_power = 60
        self.hero._curr_health = self.hero.max_health
        self.hero._curr_mana = self.hero.max_secondary_pool

    def test_lighting_bolt_contract(self):
        """cast_lighting_bolt returns damage and a cooldown."""
        info = self.hero.cast_lighting_bolt()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0

    def test_lighting_bolt_deducts_mana(self):
        """cast_lighting_bolt deducts mana from the caster."""
        before = self.hero._curr_mana
        info = self.hero.cast_lighting_bolt()
        assert self.hero._curr_mana == before - info["spell_cost"]

    def test_flame_shock_contract(self):
        """cast_flame_shock returns initial damage, DOT, cooldown, and turns_active."""
        info = self.hero.cast_flame_shock()
        assert_spell_contract(info)
        assert info["initial_spell_damage"] > 0
        assert info["damage_over_time"] > 0
        assert info["cooldown"] > 0
        assert info["turns_active"] > 0

    def test_flame_shock_deducts_mana_not_health(self):
        """cast_flame_shock deducts cost from mana, not health."""
        before_mana = self.hero._curr_mana
        before_health = self.hero._curr_health
        info = self.hero.cast_flame_shock()
        assert self.hero._curr_mana == before_mana - info["spell_cost"]
        assert self.hero._curr_health == before_health

    def test_primordial_wave_contract(self):
        """cast_primordial_wave returns high damage and a cooldown."""
        info = self.hero.cast_primordial_wave()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0

    def test_stormstrike_contract(self):
        """cast_stormstrike returns damage and a cooldown."""
        info = self.hero.cast_stormstrike()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0

    def test_lava_lash_contract(self):
        """cast_lava_lash returns damage and a cooldown."""
        info = self.hero.cast_lava_lash()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0

    def test_tempest_contract(self):
        """cast_tempest returns high damage and a cooldown."""
        info = self.hero.cast_tempest()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0

    def test_feral_spirit_contract(self):
        """cast_feral_spirit returns damage, cooldown, and turns_active."""
        info = self.hero.cast_feral_spirit()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0
        assert info["turns_active"] > 0

    def test_template_not_mutated(self):
        """Casting spells must not mutate the shared spell_attributes template."""
        self.hero.cast_lighting_bolt()
        self.hero.cast_flame_shock()
        template_not_mutated(self.hero)


# ---------------------------------------------------------------------------- #
# Fury Warrior
# ---------------------------------------------------------------------------- #

class TestFuryWarriorSpells:
    """Spell contract tests for FuryWarriorSpells."""

    def setup_method(self):
        self.hero = FuryWarriorSpells()
        self.hero.max_health = 1000
        self.hero.max_secondary_pool = 200
        self.hero.attack_power = 70
        self.hero._curr_health = self.hero.max_health
        self.hero._curr_rage = 0

    def test_bladestorm_contract(self):
        """cast_bladestorm returns damage, cooldown, and generates rage."""
        before_rage = self.hero._curr_rage
        info = self.hero.cast_bladestorm()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0
        assert self.hero._curr_rage > before_rage

    def test_rampage_without_rage(self):
        """cast_rampage returns None when rage is insufficient."""
        self.hero._curr_rage = 0
        result = self.hero.cast_rampage()
        assert result is None

    def test_rampage_with_rage(self):
        """cast_rampage returns a valid contract dict when rage is sufficient."""
        self.hero._curr_rage = 80
        info = self.hero.cast_rampage()
        assert info is not None
        assert_spell_contract(info)
        assert info["spell_damage"] > 0

    def test_bloodbath_contract(self):
        """cast_bloodbath returns damage, cooldown, and heals the caster."""
        self.hero._curr_health = self.hero.max_health - 100
        before_health = self.hero._curr_health
        info = self.hero.cast_bloodbath()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert self.hero._curr_health >= before_health

    def test_raging_blow_contract(self):
        """cast_raging_blow returns damage, cooldown, and generates rage."""
        before_rage = self.hero._curr_rage
        info = self.hero.cast_raging_blow()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0
        assert self.hero._curr_rage > before_rage

    def test_template_not_mutated(self):
        """Casting spells must not mutate the shared spell_attributes template."""
        self.hero.cast_bladestorm()
        self.hero.cast_raging_blow()
        template_not_mutated(self.hero)


# ---------------------------------------------------------------------------- #
# Protection Warrior
# ---------------------------------------------------------------------------- #

class TestProtectionWarriorSpells:
    """Spell contract tests for ProtectionWarriorSpells."""

    def setup_method(self):
        self.hero = ProtectionWarriorSpells()
        self.hero.max_health = 1500
        self.hero.max_secondary_pool = 200
        self.hero.attack_power = 50
        self.hero._curr_health = self.hero.max_health
        self.hero._curr_rage = 0

    def test_charge_contract(self):
        """cast_charge returns damage, cooldown, and generates rage."""
        before_rage = self.hero._curr_rage
        info = self.hero.cast_charge()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0
        assert self.hero._curr_rage > before_rage

    def test_shield_block_without_rage(self):
        """cast_shield_block returns None when rage is insufficient."""
        self.hero._curr_rage = 0
        result = self.hero.cast_shield_block()
        assert result is None

    def test_shield_block_with_rage(self):
        """cast_shield_block returns full damage reduction when rage is sufficient."""
        self.hero._curr_rage = 30
        info = self.hero.cast_shield_block()
        assert info is not None
        assert_spell_contract(info)
        assert info["damage_reduction"] == self.hero.max_damage_reduction

    def test_champions_spear_contract(self):
        """cast_champions_spear returns damage, cooldown, and generates rage."""
        before_rage = self.hero._curr_rage
        info = self.hero.cast_champions_spear()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0
        assert self.hero._curr_rage > before_rage

    def test_shield_charge_contract(self):
        """cast_shield_charge returns high damage, cooldown, and generates rage."""
        before_rage = self.hero._curr_rage
        info = self.hero.cast_shield_charge()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0
        assert self.hero._curr_rage > before_rage

    def test_shield_slam_contract(self):
        """cast_sheild_slam returns damage, cooldown, and generates rage."""
        before_rage = self.hero._curr_rage
        info = self.hero.cast_sheild_slam()
        assert_spell_contract(info)
        assert info["spell_damage"] > 0
        assert info["cooldown"] > 0
        assert self.hero._curr_rage > before_rage

    def test_ignore_pain_without_rage(self):
        """cast_ignore_pain returns None when rage is insufficient."""
        self.hero._curr_rage = 0
        result = self.hero.cast_ignore_pain()
        assert result is None

    def test_ignore_pain_with_rage(self):
        """cast_ignore_pain returns damage_reduction and turns_active when rage is sufficient."""
        self.hero._curr_rage = 35
        info = self.hero.cast_ignore_pain()
        assert info is not None
        assert_spell_contract(info)
        assert info["damage_reduction"] > 0
        assert info["turns_active"] > 0

    def test_template_not_mutated(self):
        """Casting spells must not mutate the shared spell_attributes template."""
        self.hero.cast_charge()
        self.hero.cast_champions_spear()
        template_not_mutated(self.hero)
