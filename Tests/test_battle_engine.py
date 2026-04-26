import pytest

from Heroes.hero_factory import HeroFactory
from battles_handler import Attacking


def test_attack_reduces_defender_health():
    factory = HeroFactory()
    attacker = factory.create_hero("paladin", "retribution")
    defender = factory.create_hero("paladin", "protection")

    before = defender.get_current_health()
    Attacking(attacker, defender).attack("cast_judgement")
    after = defender.get_current_health()

    assert after < before
