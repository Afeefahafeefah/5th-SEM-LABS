def forward_chaining(KB, query):
    inferred = set()
    new_inferred = True

    while new_inferred:
        new_inferred = False
        for rule in KB:
            premises, conclusion = rule
            if all(p in inferred or p in KB for p in premises) and conclusion not in inferred:
                inferred.add(conclusion)
                new_inferred = True
                if conclusion == query:
                    return True
    return False


# Example Knowledge Base
KB = [
    (["American(Robert)", "Weapon(x)", "Sells(Robert, x, A)", "Hostile(A)"],
     "Criminal(Robert)"),
    (["Missile(x)"], "Weapon(x)"),
    (["Owns(A, x)", "Missile(x)"], "Sells(Robert, x, A)"),
    (["Enemy(A, America)"], "Hostile(A)")
]

facts = {
    "American(Robert)",
    "Enemy(A, America)",
    "Owns(A, T1)",
    "Missile(T1)"
}

# Add base facts to KB
for fact in facts:
    KB.append(([], fact))

# Query
query = "Criminal(Robert)"
print("Is Robert a criminal?", forward_chaining(KB, query))
