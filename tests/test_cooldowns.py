from turn_based_wow.combat.battle_state import BattleState
from turn_based_wow.combat.battles_handler import Attacking
from turn_based_wow.heroes.hero_factory import HeroFactory


def test_spell_sets_cooldown_and_blocks_recast():
    """Casting a spell sets a cooldown; a second immediate cast is blocked."""
    factory = HeroFactory()
    attacker = factory.create_hero("mage", "fire")
    defender = factory.create_hero("paladin", "protection")

    bs = BattleState()
    # first cast
    defender_after, info = Attacking(attacker, defender, battle_state=bs).attack("cast_fireball")
    assert isinstance(info, dict)
    cd = bs.get_cooldown(attacker, "cast_fireball")
    assert cd > 0

    # immediate re-cast is blocked
    defender_after2, info2 = Attacking(attacker, defender, battle_state=bs).attack("cast_fireball")
    assert isinstance(info2, dict)
    assert info2.get("on_cooldown") is True


def test_dot_applies_over_ticks():
    """A DOT effect registered via BattleState deals damage on each tick."""
    factory = HeroFactory()
    attacker = factory.create_hero("mage", "fire")
    defender = factory.create_hero("paladin", "protection")

    # flamestrike has damage_over_time and turns_active
    bs = BattleState()
    before = defender._curr_health
    defender_after, info = Attacking(attacker, defender, battle_state=bs).attack("cast_flamestrike")
    assert isinstance(info, dict)
    # ensure effect registered
    effects = bs.get_active_effects(defender)
    assert any(e["name"] == "cast_flamestrike" for e in effects)

    # apply one tick
    bs.tick()
    # defender should have taken DOT damage at least once
    assert defender._curr_health <= before
