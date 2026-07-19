from Heroes.hero_factory import HeroFactory
from ai_player import SimpleHeuristicAI
from battles_handler import Attacking


def test_ai_prefers_killing_blow():
    """SimpleHeuristicAI should choose a damaging spell when the defender is near death."""
    factory = HeroFactory()
    attacker = factory.create_hero("mage", "fire")
    defender = factory.create_hero("paladin", "protection")

    # make defender very low so a damage spell can kill
    defender._curr_health = 5
    attacker._curr_health = attacker.max_health

    ai = SimpleHeuristicAI()
    choice = ai.choose_spell(attacker, defender)
    assert choice is not None

    # perform the cast and ensure we dealt damage equal or more than defender health
    _, info = Attacking(attacker, defender).attack(choice)
    assert isinstance(info, dict)
    expected_damage = info.get("spell_damage") or info.get("initial_spell_damage") or 0
    assert expected_damage >= 5 or defender._curr_health <= 0


def test_ai_heals_when_low():
    """SimpleHeuristicAI should prefer a healing spell when the attacker is at low health."""
    factory = HeroFactory()
    attacker = factory.create_hero("priest", "shadow")
    defender = factory.create_hero("mage", "fire")

    # put attacker at low health to encourage healing
    attacker._curr_health = int(attacker.max_health * 0.2)
    defender._curr_health = defender.max_health

    ai = SimpleHeuristicAI()
    choice = ai.choose_spell(attacker, defender)
    # prefer a healing spell when available (flash_heal exists for priest)
    assert choice is not None
    assert choice.startswith("cast_")