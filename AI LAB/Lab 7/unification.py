def unify(x, y, substitutions=None):
    if substitutions is None:
        substitutions = {}

    # If both are identical
    if x == y:
        return substitutions

    # If x is a variable
    if isinstance(x, str) and x.islower():
        return unify_var(x, y, substitutions)

    # If y is a variable
    if isinstance(y, str) and y.islower():
        return unify_var(y, x, substitutions)

    # If both are compound expressions (like lists or tuples)
    if isinstance(x, tuple) and isinstance(y, tuple):
        if x[0] != y[0] or len(x) != len(y):
            return None
        for a, b in zip(x[1:], y[1:]):
            substitutions = unify(a, b, substitutions)
            if substitutions is None:
                return None
        return substitutions

    return None


def unify_var(var, x, substitutions):
    if var in substitutions:
        return unify(substitutions[var], x, substitutions)
    elif x in substitutions:
        return unify(var, substitutions[x], substitutions)
    elif occurs_check(var, x, substitutions):
        return None
    else:
        substitutions[var] = x
        return substitutions


def occurs_check(var, x, substitutions):
    if var == x:
        return True
    elif isinstance(x, tuple):
        return any(occurs_check(var, arg, substitutions) for arg in x[1:])
    elif isinstance(x, str) and x in substitutions:
        return occurs_check(var, substitutions[x], substitutions)
    return False


# Example
expr1 = ("Eats", "x", "Apple")
expr2 = ("Eats", "Riya", "y")

result = unify(expr1, expr2)
print("Unification:", result)

