#!/usr/bin/python3

from collections import defaultdict
from copy import copy

# Main parameters
minI=3
maxI=128
iRange = range(minI, maxI + 1)

# Supporting functions
def filterStarts(n):
    # Even numbers will immediate decrease (boring).
    # Numbers congruent to 2 (mod 3) have an odd predecessar (2n - 1)/3 (also
    # boring, in its own way).
    return ( (n%2)==1 and ((n%3) != 2 ))

def collatz(n):
    if (n % 2):
        n = 3*n + 1
    return n // 2

def genCollatzOrbit(n):
    nList = []
    while (n > 1) and not (n in nList):
        nList.append(n)
        n = collatz(n)
    nList.append(n)
    return nList

def computeDiffDistribution(aList, doLogging=False):
    aList = copy(aList)
    distribution = defaultdict(int)
    doLogging and print(f"diff")
    while len(aList):
        a = aList.pop()
        for b in aList:
            diff = a - b
            distribution[diff] += 1
            doLogging and print(f"{diff:>4d}")
    return distribution

def computeConsecutiveDiffDistribution(aList, doLogging=False):
    """
    Create an { Integer -> Integer } map (defaultdict) where the keys are
    consecutive differences in the possibly onsorted input list, and the values
    are the number of time that difference shows up
    """
    distribution = defaultdict(int)
    for i in range(len(aList)-1):
        a = aList[i+0]
        b = aList[i+1]
        diff = b - a
        distribution[diff] += 1
        doLogging and print(f"{diff:>4d} ({b:>4d} - {a:>4d})")
    return distribution

def printDistribution(dist):
    keyList = sorted(dist.keys())
    print(f"diff  freq")
    print(f"----  ----")
    for key in keyList:
        freq = dist[key]
        stars = "*" * freq
        print(f"{key:>4d}  {freq:>4d} {stars}")

# Main method
for i in iRange:
    if not filterStarts(i):
        continue
    print(f"Performing some analysis on Collatz orbit for {i}")
    orbit = genCollatzOrbit(i)
    diffDist = computeConsecutiveDiffDistribution(orbit, doLogging=True)
    #print(f"Consecutive Diffs Distribution for {i}")
    #printDistribution(diffDist)
    #diffDist = computeDiffDistribution(orbit)
    #print(f"All Ordered Diffs Distribution for {i}")
    #printDistribution(diffDist)
    print()

