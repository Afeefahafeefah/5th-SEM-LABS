#ouestion: α=A∨B      KB=(A∨C)∧(B∨¬C)
from itertools import product


def KB(A, B, C):
    s1 = A or C    
    s2 = B or (not C)  
    return s1 and s2  


def alpha(A, B):
    return A or B


values = list(product([False, True], repeat=3))

print("A\t\tB\t\tC\t\tA∨C\t\tB∨¬C\tKB\t\tα")
print("-"*50)

models = []
for A, B, C in values:
    s1 = A or C
    s2 = B or (not C)
    kb_val = s1 and s2
    alpha_val = alpha(A, B)
    print(f"{A}\t{B}\t{C}\t{s1}\t{s2}\t{kb_val}\t{alpha_val}")
    if kb_val:
        models.append((A, B, C))

print("\nModels where KB is True:", models)


entails_alpha = all(alpha(A, B) for A, B, C in models)

print("\nEntailment:")
print("KB ⊨ α :", entails_alpha)