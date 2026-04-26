import pytest

from Spells.paladin_spell_handler import RetributionPaladinSpells


def test_cast_divine_shield_returns_dict_and_turns():
    p = RetributionPaladinSpells()
    res = p.cast_divine_shield()
    assert isinstance(res, dict)
    assert res.get("cooldown") == 15
    assert res.get("turns_active") == 2


def test_cast_judgement_reduces_mana_and_has_damage():
    p = RetributionPaladinSpells()
    before = p.get_current_secondary_pool()
    res = p.cast_judgement()
    after = p.get_current_secondary_pool()
    assert isinstance(res, dict)
    assert "spell_damage" in res
    assert after < before


def test_returned_dict_is_a_copy():
    p = RetributionPaladinSpells()
    res = p.cast_judgement()
    res["spell_damage"] = 99999
    internal = p.get_current_spell_attributes()
    assert internal.get("spell_damage") != 99999
