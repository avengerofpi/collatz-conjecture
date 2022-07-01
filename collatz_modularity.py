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

def collatzModN(N, residueList):
    tooManyIters = list()
    needsSplitting = list()
    for A in residueList:
        a = A
        b = N
        print(f"Checking a = {a} (mod {b})")
        iters = 0
        maxIters = 10
        while ((b >= N) and ((b % 2) == 0) and (iters < maxIters)):
            iters += 1
            print(f"  {a:>4d} + {b:>4d}k")
            a, b = collatze_vector(a, b)
        print(f"  {a:>4d} + {b:>4d}k")

        # Report conclusions, checking each of the loop-exiting conditions
        if (b < N):
            print(f"  Decreases       ((b={b}) <(N={N}))")
        elif ((b % 2) == 1):
            print(f"  Needs splitting ((b={b} is odd))")
            needsSplitting.append(A)
        elif (iters >= maxIters):
            print(f"  Needs more iters (current maxIters is {maxIters})")
            tooManyIters.append(A)
        else:
            raise Exception("Error! Should not have reached this point")

    if (len(tooManyIters) > 0):
        print()
        print(f"There are entries that required more iters than were allowed (maxIters was {maxIters})")
        return
    else:
        return needsSplitting

# Main routine
N = 2
needsSplitting = collatzModN(N, range(N))
while needsSplitting:
    print("-"*50)
    print(f"needsSplitting for N = {N}: {needsSplitting}")
    splitInput = sorted([ x for xx in [[ a, a + N ] for a in needsSplitting] for x in xx])
    N *= 2
    print(f"splitInput     for N = {N}: {splitInput}")
    needsSplitting = collatzModN(N, splitInput)
    nLog2 += 1
