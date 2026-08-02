from turn_based_wow.combat.battle_state import BattleState
from turn_based_wow.combat.battles_handler import Attacking
from turn_based_wow.heroes.hero_factory import HeroFactory

MAX_TURNS = 100


def _current_health(hero) -> int:
    # Temporary compatibility helper.
    # Replace with the public Hero API in TBW-201.
    return hero._curr_health


def _choose_available_action(
    hero,
    battle_state: BattleState,
    preferred: str,
    fallback: str,
) -> str | None:
    if not battle_state.is_on_cooldown(hero, preferred):
        return preferred

    if not battle_state.is_on_cooldown(hero, fallback):
        return fallback

    return None


def _run_battle(
    first_hero,
    second_hero,
    battle_state: BattleState,
    first_actions: tuple[str, str],
    second_actions: tuple[str, str],
) -> dict[str, object]:
    active = first_hero
    passive = second_hero
    turns = 0
    action_history = []

    while _current_health(first_hero) > 0 and _current_health(second_hero) > 0:
        turns += 1
        assert turns <= MAX_TURNS, "Battle exceeded the deterministic turn limit"

        actions = first_actions if active is first_hero else second_actions
        selected_action = _choose_available_action(
            active,
            battle_state,
            preferred=actions[0],
            fallback=actions[1],
        )

        if selected_action is not None:
            action_history.append(selected_action)
            handler = Attacking(active, passive, battle_state=battle_state)
            passive, _ = handler.attack(selected_action)

        battle_state.tick()

        if _current_health(first_hero) <= 0 or _current_health(second_hero) <= 0:
            break

        active, passive = passive, active

    winner = first_hero if _current_health(first_hero) > 0 else second_hero
    loser = second_hero if winner is first_hero else first_hero

    return {
        "winner": winner,
        "loser": loser,
        "turns": turns,
        "actions": action_history,
    }


def test_battle_reaches_a_winner_with_deterministic_actions():
    factory = HeroFactory()

    first_hero = factory.create_hero("Warrior", "Fury")
    second_hero = factory.create_hero("Warrior", "Fury")

    first_actions = ("cast_bloodbath", "cast_raging_blow")
    second_actions = ("cast_raging_blow", "cast_bloodbath")

    for action in first_actions:
        assert callable(getattr(first_hero, action, None))

    for action in second_actions:
        assert callable(getattr(second_hero, action, None))

    result = _run_battle(
        first_hero,
        second_hero,
        BattleState(),
        first_actions,
        second_actions,
    )

    assert result["winner"] is first_hero
    assert _current_health(result["loser"]) == 0
    assert _current_health(first_hero) == 29
    assert result["turns"] == 79
    assert result["actions"][:4] == [
        "cast_bloodbath",
        "cast_raging_blow",
        "cast_raging_blow",
        "cast_bloodbath",
    ]
