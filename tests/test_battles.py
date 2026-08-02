from turn_based_wow.combat.battles_handler import Attacking
from turn_based_wow.heroes.hero_factory import HeroFactory


def test_attack_applies_damage_and_heal():
    """Attacking with cast_fireball reduces defender health and may heal attacker."""
    factory = HeroFactory()
    attacker = factory.create_hero('mage', 'fire')
    defender = factory.create_hero('paladin', 'protection')

    # ensure predictable starting health
    attacker._curr_health = attacker.max_health
    defender._curr_health = defender.max_health

    before_attacker = attacker._curr_health
    before_defender = defender._curr_health

    attacking = Attacking(attacker, defender)
    defender_after, info = attacking.attack('cast_fireball')

    assert isinstance(info, dict)
    assert 'spell_damage' in info
    assert defender_after._curr_health == max(0, before_defender - info['spell_damage'])
    assert attacker._curr_health >= before_attacker
