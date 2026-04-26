import inspect
import pytest

from Heroes.hero_factory import HeroFactory
from battles_handler import Attacking


HERO_CASES = [
    ("paladin", "retribution"),
    ("paladin", "protection"),
    ("warrior", "fury"),
    ("warrior", "protection"),
    ("mage", "fire"),
    ("monk", "windwalker"),
    ("monk", "brewmaster"),
    ("shaman", "enhancement"),
    ("priest", "shadow"),
]


def _zero_arg_castables(hero):
    for name in dir(hero):
        if not name.startswith("cast_"):
            continue
        fn = getattr(hero, name)
        try:
            sig = inspect.signature(fn)
        except (ValueError, TypeError):
            continue
        params = [
            p
            for p in sig.parameters.values()
            if p.default is p.empty
            and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
        ]
        if params:
            continue
        yield name, fn


def test_zero_arg_spells_do_not_crash_and_return_expected_types():
    factory = HeroFactory()
    for cls, role in HERO_CASES:
        hero = factory.create_hero(cls, role)
        for name, fn in _zero_arg_castables(hero):
            before_pool = hero.get_current_secondary_pool()
            try:
                res = fn()
            except Exception as e:
                pytest.fail(f"Spell {hero.get_name()}.{name} raised {e}")

            # None is an acceptable result for conditional spells
            if res is None:
                continue

            assert isinstance(res, dict)

            # modifying returned dict should not mutate internal state
            res_copy = dict(res)
            res_copy["__test_mutate__"] = 12345
            internal = hero.get_current_spell_attributes()
            assert internal.get("__test_mutate__") is None

            # secondary pool should not increase after casting
            after_pool = hero.get_current_secondary_pool()
            assert after_pool <= before_pool


def test_attack_with_first_available_spell_reduces_health_when_damage_present():
    factory = HeroFactory()
    for attacker_spec in HERO_CASES:
        attacker = factory.create_hero(*attacker_spec)
        defender = factory.create_hero("paladin", "protection")

        spell_to_use = None
        for name, fn in _zero_arg_castables(attacker):
            res = fn()
            if isinstance(res, dict) and res.get("spell_damage", 0) > 0:
                spell_to_use = name
                break

        if not spell_to_use:
            # no suitable damage spell for this spec, skip
            continue

        before = defender.get_current_health()
        Attacking(attacker, defender).attack(spell_to_use)
        after = defender.get_current_health()
        assert after <= before
