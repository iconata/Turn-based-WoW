import inspect

from Heroes.hero_factory import HeroFactory
from battles_handler import Attacking


def _pick_preferred_spell(hero, preferred_names):
    for n in preferred_names:
        if hasattr(hero, n):
            return n

    # fallback: first zero-arg cast_ method
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
        if not params:
            return name

    return None


def test_paladin_duel_ends_with_winner():
    factory = HeroFactory()

    attacker = factory.create_hero("paladin", "retribution")
    defender = factory.create_hero("paladin", "protection")

    attacker_spell = _pick_preferred_spell(
        attacker, ["cast_judgement", "cast_blade_of_justice", "cast_wake_of_ashes"]
    )
    defender_spell = _pick_preferred_spell(
        defender, ["cast_crusader_strike", "cast_shield_of_the_righteous", "cast_blessed_hammer"]
    )

    assert attacker_spell, "No suitable attacker spell found"
    assert defender_spell, "No suitable defender spell found"

    max_turns = 100
    for _ in range(max_turns):
        Attacking(attacker, defender).attack(attacker_spell)
        if not defender.is_alive():
            break

        Attacking(defender, attacker).attack(defender_spell)
        if not attacker.is_alive():
            break

    # the duel should finish with exactly one winner
    assert attacker.is_alive() != defender.is_alive()
