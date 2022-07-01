#!/usr/bin/python3

# Imports

# Functions
def collatz(n):
    if (n % 2):
        return (3*n+1) // 2
    else:
        return n//2

def collatze_vector(a, b):
    if (b % 2):
        # Can't continue - not sure if even or odd
        return None
    if (a % 2):
        return collatz(a), 3 * b // 2
    else:
        return a // 2, b // 2

def collatzModN(N):
    for a in range(N):
        print(f"Checking a = {a} (mod {N})")
        b = N
        iters = 0
        maxIters = 20
        while ((b >= N) and ((b % 2) == 0) and (iters < maxIters)):
            iters += 1
            print(f"  {a:>4d} + {b:>4d}k")
            a, b = collatze_vector(a, b)
        print(f"  {a:>4d} + {b:>4d}k")

        # Report conclusions
        if (b < N):
            print(f"  Decreases    ((b={b} <  (N={N}))")
        else:
            print(f"  Inconclusive ((b={b} >= (N={N}))")
            if ((b % 2) == 1):
                print(f"  Needs splitting (b={b} is odd)")
            elif (iters >= maxIters):
                print(f"  Needs more iters (current maxIters is {maxIters})")


# Main routine
N = 32
collatzModN(N)
