"""
Task 4 – Prolog Queries via janus_swi (SWI-Prolog Python bridge)
CMPM 118

Knowledge Base: f1_kb.pl
Domain: Formula 1 – Drivers, Teams, Champions, Race Wins (2024 season)

We demonstrate:
  • Consulting a .pl file from Python
  • Running ground queries (yes/no)
  • Running open queries (returning all solutions)
  • Verifying the Prolog interpreter gives the same answers we expect

Usage:
    python3 task4.py
"""

import os
import janus_swi as janus

# ------------------------------------------------------------------ #
#  Locate the KB relative to this script so it works from any CWD    #
# ------------------------------------------------------------------ #
KB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "f1_kb.pl")

# ------------------------------------------------------------------ #
#  Helper utilities                                                    #
# ------------------------------------------------------------------ #

def load_kb():
    """Consult the F1 knowledge base into SWI-Prolog."""
    escaped = KB_PATH.replace("\\", "/")
    result = janus.query_once(f"consult('{escaped}')")
    if result.get("truth"):
        print(f"✅  KB loaded: {KB_PATH}\n")
    else:
        raise RuntimeError(f"Failed to consult KB at {KB_PATH}")


def ask_yes_no(description: str, query: str) -> bool:
    """Run a ground query and print YES / NO."""
    result = janus.query_once(query)
    truth = result.get("truth", False)
    label = "YES ✓" if truth else "NO  ✗"
    print(f"  Q: {description}")
    print(f"     Prolog: {query}")
    print(f"     Answer: {label}\n")
    return truth


def ask_all(description: str, query: str, var: str) -> list:
    """
    Run an open query and collect all unique bindings for `var`.
    Uses janus.query() which returns an iterator over solution dicts.
    Deduplication via dict.fromkeys preserves insertion order.
    """
    raw = [sol[var] for sol in janus.query(query)]
    # Prolog backtracking can yield duplicates when multiple fact combos
    # satisfy a rule — deduplicate while preserving order
    solutions = list(dict.fromkeys(raw))
    print(f"  Q: {description}")
    print(f"     Prolog: {query}")
    print(f"     Answers ({len(solutions)}): {solutions}\n")
    return solutions


# ------------------------------------------------------------------ #
#  Main demo                                                           #
# ------------------------------------------------------------------ #

def main():
    load_kb()

    print("=" * 60)
    print("  F1 Knowledge Base – Prolog Query Results")
    print("=" * 60)
    print()

    # ── Section 1: Ground (yes/no) queries ───────────────────────── #
    print("── Ground Queries (Yes / No) ──────────────────────────────\n")

    ask_yes_no(
        "Is Max Verstappen a champion?",
        "champion(max_verstappen, _)"
    )

    ask_yes_no(
        "Does Lewis Hamilton drive for Red Bull?",
        "drives_for(lewis_hamilton, red_bull)"
    )

    ask_yes_no(
        "Did Lando Norris win a race in 2024?",
        "won_race(lando_norris, _, 2024)"
    )

    ask_yes_no(
        "Are Leclerc and Sainz teammates?",
        "teammates(charles_leclerc, carlos_sainz)"
    )

    ask_yes_no(
        "Is Verstappen a multi-champion?",
        "multi_champion(max_verstappen)"
    )

    ask_yes_no(
        "Is Fernando Alonso a multi-champion?",
        "multi_champion(fernando_alonso)"
    )

    ask_yes_no(
        "Did Verstappen dominate 2024 (4+ wins)?",
        "dominant(max_verstappen)"
    )

    ask_yes_no(
        "Is Lance Stroll a 2024 race winner?",
        "race_winner(lance_stroll)"
    )

    # ── Section 2: Open queries (all solutions) ───────────────────── #
    print("── Open Queries (All Solutions) ───────────────────────────\n")

    ask_all(
        "Who are all the 2024 race winners?",
        "race_winner(Driver)",
        "Driver"
    )

    ask_all(
        "Which teams had at least one race win in 2024?",
        "team_winner(Team)",
        "Team"
    )

    ask_all(
        "Who are Lando Norris's teammates?",
        "teammates(lando_norris, Teammate)",
        "Teammate"
    )

    ask_all(
        "Who are all drivers for Ferrari?",
        "drives_for(Driver, ferrari)",
        "Driver"
    )

    ask_all(
        "List all championship years for Hamilton",
        "champion(lewis_hamilton, Year)",
        "Year"
    )

    ask_all(
        "Which drivers are both multi-champions AND 2024 race winners?",
        "experienced(Driver)",
        "Driver"
    )

    ask_all(
        "Which drivers won a race at the Australian GP (any year)?",
        "won_race(Driver, australian_gp, _)",
        "Driver"
    )

    # ── Section 3: Verification assertions ───────────────────────── #
    print("── Verification Assertions ────────────────────────────────\n")

    checks = [
        # (description, query, expected_truth)
        ("Verstappen drives for Red Bull",        "drives_for(max_verstappen, red_bull)",        True),
        ("Hamilton does NOT drive for Red Bull",  "drives_for(lewis_hamilton, red_bull)",        False),
        ("Norris won Miami 2024",                 "won_race(lando_norris, miami_gp, 2024)",      True),
        ("Alonso is a multi-champion",            "multi_champion(fernando_alonso)",             True),
        ("Verstappen dominated 2024",             "dominant(max_verstappen)",                    True),
        ("Stroll did NOT win a 2024 race",        "race_winner(lance_stroll)",                   False),
        ("Russell and Hamilton are teammates",    "teammates(george_russell, lewis_hamilton)",   True),
    ]

    all_passed = True
    for desc, query, expected in checks:
        result = janus.query_once(query)
        actual = result.get("truth", False)
        status = "PASS ✅" if actual == expected else "FAIL ❌"
        if actual != expected:
            all_passed = False
        print(f"  {status}  {desc}")
        print(f"           Expected: {expected}  |  Got: {actual}\n")

    print("=" * 60)
    print(f"  All assertions passed: {all_passed}")
    print("=" * 60)


if __name__ == "__main__":
    main()
