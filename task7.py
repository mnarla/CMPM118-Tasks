# My KB (from task 4) but specfically for task 7
FACTS = {
    ("driver", "lewis_hamilton", "ferrari"),
    ("driver", "charles_leclerc", "ferrari"),
    ("driver", "max_verstappen", "red_bull"),
    ("driver", "isack_hadjar", "red_bull"),
    ("driver", "lando_norris", "mclaren"),
    ("driver", "oscar_piastri", "mclaren"),
    ("driver", "george_russell", "mercedes"),
    ("driver", "kimi_antonelli", "mercedes"),
    ("driver", "fernando_alonso", "aston_martin"),
    ("driver", "lance_stroll", "aston_martin"),
}

RULES = [
    (("teammates", "?x", "?y"),
     [("driver", "?x", "?t"), ("driver", "?y", "?t")]),

    (("drives_for", "?x", "?t"),
     [("driver", "?x", "?t")]),
]


def is_var(term):
    #checks if a term is a variable 
    return isinstance(term, str) and term.startswith("?")

def unify(pattern, fact, bindings):
    #matches a pattern against a fact 
    if len(pattern) != len(fact):
        return None
    b = dict(bindings)
    for p, f in zip(pattern, fact):
        if is_var(p):
            if p in b and b[p] != f:
                return None  
            b[p] = f
        elif p != f:
            return None
    return b

def substitute(pattern, bindings):
    #fills in bound values.
    return tuple(bindings.get(t, t) for t in pattern)

def prove(goal, facts, rules, bindings):
    #The OR step
    goal = substitute(goal, bindings)

    solutions = []
    for fact in facts:
        b = unify(goal, fact, bindings)
        if b is not None:
            solutions.append(b)

    for head, body in rules:
        b = unify(head, goal, bindings)
        if b is None:
            continue
        for final_bindings in prove_body(body, facts, rules, b):
            solutions.append(final_bindings)

    return solutions

def prove_body(goals, facts, rules, bindings):
    #The AND step
    if not goals:
        yield bindings
        return
    head, *rest = goals
    for b in prove(head, facts, rules, bindings):
        yield from prove_body(rest, facts, rules, b)

def query(goal_tuple, facts=FACTS, rules=RULES):
    """Top-level query. Returns all solutions as binding dicts."""
    results = prove(goal_tuple, facts, rules, {})
    if goal_tuple[0] == "teammates":
        results = [b for b in results if b.get("?x") != b.get("?y")]
    return results


# tests
if __name__ == "__main__":
    tests = [
        ("driver", "lewis_hamilton", "ferrari"),     # true
        ("driver", "lewis_hamilton", "red_bull"),    # false
        ("teammates", "lewis_hamilton", "charles_leclerc"),  # true
        ("teammates", "lewis_hamilton", "max_verstappen"),   # false
        ("teammates", "max_verstappen", "max_verstappen"),   # false
        ("drives_for", "george_russell", "mercedes"),        # true
    ]
    for t in tests:
        r = query(t)
        print(f"{t} -> {'TRUE' if r else 'FALSE'}")