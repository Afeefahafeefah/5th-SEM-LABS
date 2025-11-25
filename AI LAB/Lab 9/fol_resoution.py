import copy

# ------------------------------
# Predicate Structure
# ------------------------------
class Predicate:
    def __init__(self, name, args, negated=False):
        self.name = name
        self.args = args if isinstance(args, tuple) else tuple(args)
        self.negated = negated

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.args == other.args and
            self.negated == other.negated
        )

    def __hash__(self):
        return hash((self.name, self.args, self.negated))

    def __repr__(self):
        neg = "~" if self.negated else ""
        args_str = ",".join(str(a) for a in self.args)
        return f"{neg}{self.name}({args_str})"

    def negate(self):
        return Predicate(self.name, self.args, not self.negated)

    def substitute(self, theta):
        """Apply substitution theta to this predicate"""
        new_args = tuple(substitute_term(arg, theta) for arg in self.args)
        return Predicate(self.name, new_args, self.negated)


def substitute_term(term, theta):
    """Apply substitution to a term"""
    if isinstance(term, str) and term.islower():  # variable
        if term in theta:
            return substitute_term(theta[term], theta)
        return term
    elif isinstance(term, tuple):
        return tuple(substitute_term(t, theta) for t in term)
    return term


# ------------------------------
# Unification Algorithm
# ------------------------------
def unify(x, y, theta=None):
    if theta is None:
        theta = {}

    if theta == "FAIL":
        return "FAIL"
    elif x == y:
        return theta
    elif isinstance(x, str) and x.islower():  # variable
        return unify_var(x, y, theta)
    elif isinstance(y, str) and y.islower():  # variable
        return unify_var(y, x, theta)
    elif isinstance(x, tuple) and isinstance(y, tuple):
        if len(x) != len(y):
            return "FAIL"
        theta = unify(x[0], y[0], theta)
        if theta == "FAIL":
            return "FAIL"
        return unify(x[1:], y[1:], theta)
    else:
        return "FAIL"


def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    elif isinstance(x, str) and x.islower() and x in theta:
        return unify(var, theta[x], theta)
    elif occurs_check(var, x, theta):
        return "FAIL"
    else:
        new_theta = copy.deepcopy(theta)
        new_theta[var] = x
        return new_theta


def occurs_check(var, x, theta):
    if var == x:
        return True
    elif isinstance(x, str) and x.islower() and x in theta:
        return occurs_check(var, theta[x], theta)
    elif isinstance(x, tuple):
        return any(occurs_check(var, xi, theta) for xi in x)
    return False


# ------------------------------
# Variable Standardization
# ------------------------------
var_counter = 0

def standardize_variables(clause):
    """Rename all variables in a clause to unique names"""
    global var_counter
    mapping = {}
    new_clause = []

    for pred in clause:
        new_args = []
        for arg in pred.args:
            if isinstance(arg, str) and arg.islower():  # variable
                if arg not in mapping:
                    mapping[arg] = f"{arg}{var_counter}"
                    var_counter += 1
                new_args.append(mapping[arg])
            else:
                new_args.append(arg)
        new_clause.append(Predicate(pred.name, new_args, pred.negated))

    return new_clause


# ------------------------------
# Resolution Algorithm
# ------------------------------
def resolve(ci, cj):
    """Resolve two clauses using FOL resolution"""
    ci = standardize_variables(ci)
    cj = standardize_variables(cj)

    resolvents = []

    for i, pi in enumerate(ci):
        for j, pj in enumerate(cj):
            # Opposite sign, same predicate name
            if pi.negated != pj.negated and pi.name == pj.name:
                theta = unify(pi.args, pj.args)

                if theta != "FAIL":
                    new_clause = []

                    # Add literals from ci except pi
                    for k, pred in enumerate(ci):
                        if k != i:
                            new_clause.append(pred.substitute(theta))

                    # Add literals from cj except pj
                    for k, pred in enumerate(cj):
                        if k != j:
                            new_clause.append(pred.substitute(theta))

                    # Remove duplicates
                    new_clause = list(set(new_clause))
                    resolvents.append(new_clause)

    return resolvents


def fol_resolution(kb, query):
    """FOL resolution algorithm"""

    clauses = [clause[:] for clause in kb]
    clauses.append([query.negate()])

    print("\nKnowledge Base + Negated Query:")
    for i, clause in enumerate(clauses):
        print(f"  {i+1}. {clause}")
    print()

    iteration = 0

    while True:
        iteration += 1
        n = len(clauses)

        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i + 1, n)]

        new_clauses = []
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)

            for resolvent in resolvents:
                if len(resolvent) == 0:
                    print(f"Iteration {iteration}: Derived empty clause from:")
                    print(f"  {ci}")
                    print(f"  {cj}")
                    print("  → [] (Contradiction found!)")
                    return True

                if resolvent not in clauses and resolvent not in new_clauses:
                    new_clauses.append(resolvent)

        if not new_clauses:
            print(f"Iteration {iteration}: No new clauses derived. Query cannot be proved.")
            return False

        print(f"Iteration {iteration}: Generated {len(new_clauses)} new clause(s)")
        for clause in new_clauses:
            clauses.append(clause)


# ------------------------------
# Example Usage
# ------------------------------
if __name__ == "__main__":

    kb = [
        [Predicate("Food", ("x",), negated=True), Predicate("Likes", ("John", "x"))],

        [Predicate("Food", ("Apple",))],

        [Predicate("Food", ("Vegetables",))],

        [Predicate("Eats", ("Anil", "Peanuts"))],

        [Predicate("Alive", ("Anil",))],

        [Predicate("Alive", ("x",), negated=True),
         Predicate("Eats", ("x", "y"), negated=True),
         Predicate("Food", ("y",))],

        [Predicate("Eats", ("Anil", "y"), negated=True),
         Predicate("Eats", ("Harry", "y"))]
    ]

    query = Predicate("Likes", ("John", "Peanuts"))

    print("=" * 60)
    print("FIRST-ORDER LOGIC RESOLUTION THEOREM PROVER")
    print("=" * 60)
    print(f"\nQuery: {query}")
    print("-" * 60)

    result = fol_resolution(kb, query)

    print("\n" + "=" * 60)
    if result:
        print("✅ Query is PROVED using resolution!")
    else:
        print("❌ Query CANNOT be proved.")
    print("=" * 60)
