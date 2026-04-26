import argparse

import inspect

from Heroes.hero_base_stats import IBaseHero
from Heroes.hero_factory import HeroFactory
from battles_handler import Attacking, BattleState

# --------------------------------- Constants -------------------------------- #
AVAILABLE_CLASSES = ["Warrior", "Mage", "Paladin", "Shaman", "Monk", "Priest"]
AVAILABLE_ROLES = {
    "Paladin": {"Tank": "Protection", "Damage": "Retribution"},
    "Warrior": {"Tank": "Protection", "Damage": "Fury"},
    "Monk": {"Tank": "Brewmaster", "Damage": "Windwalker"},
    "Mage": {"Damage": "Fire"},
    "Shaman": {"Damage": "Enhancement"},
    "Priest": {"Damage": "Shadow"},
}


# ------------------------------ Parse argumets ------------------------------ #
def arg_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Turn-based WoW: Create two heroes by specifying their class and role. "
            "The first hero will be the attacker, and the second will be the defender. "
            "You can also run the script interactively without command line arguments."
        )
    )
    parser.add_argument(
        "--show-classes",
        "-C",
        action="store_true",
        help="Show available hero classes and exit",
    )
    parser.add_argument(
        "--show-roles",
        "-R",
        action="store_true",
        help="Show available hero roles and exit",
    )

    return parser.parse_args()


# --------------------------- Create Hero Instance --------------------------- #
def create_hero_instance(hero_class: str, hero_role: str) -> IBaseHero:
    hero_factory = HeroFactory()
    return hero_factory.create_hero(hero_class, hero_role)


# -------------------------- Set Hero Class and Role ------------------------- #
def set_hero_class_and_role(position: int) -> tuple[str, str]:
    counter = 0
    hero_map = {1: "first", 2: "second"}
    hero_class = input(
        f"Enter the class of the {hero_map[position]} hero ({', '.join(AVAILABLE_CLASSES)}): "
    ).capitalize()
    while hero_class not in AVAILABLE_CLASSES:
        hero_class = input(
            f"Invalid class. Enter the class of the {hero_map[position]} hero ({', '.join(AVAILABLE_CLASSES)}): "
        ).capitalize()
        counter += 1
        if counter >= 3:
            print("Too many invalid attempts. Exiting.")
            exit(1)

    # If there is only one possible role for the selected class, auto-select it.
    if len(AVAILABLE_ROLES[hero_class]) == 1:
        only_role = list(AVAILABLE_ROLES[hero_class].keys())[0]
        hero_role = only_role
        print(f"Automatically selected role: {hero_role}")
    else:
        hero_role = input(
            f"Enter the role of the {hero_map[position]} hero ({', '.join(AVAILABLE_ROLES[hero_class])}): "
        ).capitalize()
        while hero_role not in AVAILABLE_ROLES[hero_class]:
            counter += 1
            hero_role = input(
                f"Invalid role. Enter the role of the {hero_map[position]} hero ({', '.join(AVAILABLE_ROLES[hero_class])}): "
            ).capitalize()
            if counter >= 3:
                print("Too many invalid attempts. Exiting.")
                exit(1)

    return hero_class, hero_role


# ---------------------------------------------------------------------------- #
#                                     Main                                     #
# ---------------------------------------------------------------------------- #
def main() -> None:
    args = arg_parser()
    if args.show_classes:
        print("Available classes:", ", ".join(AVAILABLE_CLASSES))
        return

    if args.show_roles:
        print("Available roles:")
        for hero_class, roles in AVAILABLE_ROLES.items():
            print(f"{hero_class}: {', '.join(roles)}")
        return

    first_hero = set_hero_class_and_role(position=1)
    second_hero = set_hero_class_and_role(position=2)

    attacker = create_hero_instance(
        first_hero[0], AVAILABLE_ROLES[first_hero[0]][first_hero[1]]
    )
    defender = create_hero_instance(
        second_hero[0], AVAILABLE_ROLES[second_hero[0]][second_hero[1]]
    )
    # persistent battle state for the encounter (effects, cooldowns)
    battle_state = BattleState(attacker, defender)
    print(f"Created attacker: {attacker.get_name()}, defender: {defender.get_name()}")

    # Turn loop: continue while both heroes are alive
    turn = 1
    while defender.get_current_health() > 0 and attacker.get_current_health() > 0:
        print("\n" + "=" * 60)
        print(f"Turn {turn}: {attacker.get_name()} acting")
        attacking_handler = Attacking(attacker, defender, battle_state)

        # list available zero-arg spells for the attacker
        spells = []
        for name in dir(attacker):
            if name.startswith("cast_"):
                fn = getattr(attacker, name)
                try:
                    sig = inspect.signature(fn)
                except (ValueError, TypeError):
                    continue
                # select only callables without required positional arguments
                params = [p for p in sig.parameters.values() if p.default is p.empty and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
                if len(params) == 0:
                    spells.append(name)

        if not spells:
            print(f"No castable zero-arg spells for {attacker.get_name()}, skipping turn.")
        else:
            print(f"{attacker.get_name()} spells:")
            for i, s in enumerate(spells, start=1):
                print(f"  {i}. {s}")
            choice = input("Choose spell number (default 1): ")
            try:
                idx = int(choice.strip()) - 1 if choice.strip() else 0
            except Exception:
                idx = 0
            idx = max(0, min(idx, len(spells) - 1))
            selected_spell = spells[idx]

            try:
                # capture health before the action for clearer logging
                before_attacker_hp = attacker.get_current_health()
                before_defender_hp = defender.get_current_health()

                ret = attacking_handler.attack(selected_spell)

                # Attacking.attack now returns (defender, info) when available
                if isinstance(ret, tuple) and len(ret) == 2:
                    defender, info = ret
                else:
                    defender = ret
                    info = {}

                # handle cooldown / failed-cast cases first
                if info.get("on_cooldown"):
                    print(f"{attacker.get_name()} tried {selected_spell} but it's on cooldown ({info.get('remaining')} turns left).")
                else:
                    print(f"{attacker.get_name()} used {selected_spell}")
                    raw = info.get("raw_result", {}) if isinstance(info.get("raw_result", {}), dict) else {}
                    cost = raw.get("spell_cost", 0) if isinstance(raw, dict) else 0
                    dmg = info.get("damage_applied", max(0, before_defender_hp - defender.get_current_health()))
                    healed = info.get("healed", max(0, attacker.get_current_health() - before_attacker_hp))
                    cd = info.get("cooldown", raw.get("cooldown", 0) if isinstance(raw, dict) else 0)
                    turns = info.get("turns_active", raw.get("turns_active", 0) if isinstance(raw, dict) else 0)

                    parts = []
                    if cost:
                        parts.append(f"cost={cost}")
                    if dmg:
                        parts.append(f"dmg={dmg}")
                    if healed:
                        parts.append(f"heal={healed}")
                    if cd:
                        parts.append(f"cooldown={cd}")
                    if turns:
                        parts.append(f"turns={turns}")

                    if parts:
                        print(f"  -> {' '.join(parts)}")
                    else:
                        print("  -> No immediate effect")

                    # show immediate health changes
                    print(
                        f"  Health: {attacker.get_name()} {before_attacker_hp} -> {attacker.get_current_health()} | "
                        f"{defender.get_name()} {before_defender_hp} -> {defender.get_current_health()}"
                    )

            except TypeError:
                print("Spell failed to cast due to unexpected signature; skipping.")

        # advance persistent effects and cooldowns (apply DOTs, reduce durations)
        battle_state.tick()

        # show active effects (if any)
        a_effects = battle_state.get_active_effects(attacker)
        d_effects = battle_state.get_active_effects(defender)
        if a_effects or d_effects:
            print("  Active effects:")
            for h, effs in ((attacker, a_effects), (defender, d_effects)):
                for e in effs:
                    name = e.get("name")
                    rem = e.get("remaining")
                    print(f"    - {h.get_name()}: {name} ({rem} turns left)")

        # swap roles each turn
        attacker, defender = defender, attacker
        turn += 1

# Announce winner
    print("\n" + "=" * 60)
    winner = attacker if attacker.get_current_health() > 0 else defender
    print(f"Battle finished. Winner: {winner.get_name()}")


if __name__ == "__main__":
    main()
