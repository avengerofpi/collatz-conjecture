#!/usr/bin/python3

# Imports
from math import log10, log2

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
    maxResidueWidth=int(log10(max(residueList))) + 2
    maxResidueWidthBinary=int(log2(max(residueList))) + 2
    maxModulusWidth=int(log10(N)) + 2
    tooManyIters = list()
    needsSplitting = list()
    for A in residueList:
        a = A
        b = N
        print(f"Checking a = {a:>{maxResidueWidth}d} = 0b{a:0>{maxResidueWidthBinary}b} ({b:>d}) -> ", end="")
        iters = 0
        maxIters = 30
        maxIters = 10
        while ((b >= N) and ((b % 2) == 0) and (iters < maxIters)):
            iters += 1
            #print(f"  {a:>4d} + {b:>4d}k")
            a, b = collatze_vector(a, b)
        print(f" {a:>{maxResidueWidth}d} + {b:>{maxModulusWidth}d}k ", end="")

        # Report conclusions, checking each of the loop-exiting conditions
        if (b < N):
            if (a == A):
                aCompare = "="
            elif (a < A):
                aCompare = "<"
            else:
                aCompare = ">"
            print(f"  Decreases       ((a: {a}{aCompare}{A}) (b={b}<{N}))")
        elif ((b % 2) == 1):
            print(f"  Needs splitting (0b{a:0>{maxResidueWidthBinary+4}b})")
            needsSplitting.append(A)
        elif (iters >= maxIters):
            print(f"  Needs more iters (current maxIters is {maxIters})")
            tooManyIters.append(A)
        else:
            raise Exception("Error! Should not have reached this point")

    if (len(tooManyIters) > 0):
        print()
        print(f"There are entries that required more iters than were allowed (maxIters was {maxIters})")
        print("  Exiting.")
        return
    else:
        return needsSplitting

# Main routine
N = 2
nLog2 = 1
maxResidueListLenWidth=4
residueList=[i for i in range(N) if (i % 2)]
while residueList:
    print("-"*50)
    print(f"{len(residueList):>{maxResidueListLenWidth}d} residues to check          for N = {N}: {residueList}")
    needsSplitting = collatzModN(N, residueList)
    if (needsSplitting):
        print(f"{len(needsSplitting):>{maxResidueListLenWidth}d} residues needing splitting for N = {N}: {needsSplitting}")
        if (len(needsSplitting) == len(residueList)):
            print(f"  NO ADDITIONAL PROGRESS FOR N = {N} (2 ** {nLog2})")
        residueList = sorted([ x for xx in [[ a, a + N ] for a in needsSplitting] for x in xx])
    else:
        residueList = list()
    N *= 2
    nLog2 += 1
