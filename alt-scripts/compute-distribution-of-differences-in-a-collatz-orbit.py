#!/usr/bin/python3

from collections import defaultdict
from copy import copy

# Supporting functions
def collatz(n):
    if (n % 2):
        n = 3*n + 1
    return n // 2

def genCollatzOrbit(n):
    nList = [n]
    while n > 1:
        n = collatz(n)
        nList.append(n)
    return nList

def computeDiffDistribution(aList):
    aList = copy(aList)
    distribution = defaultdict(int)
    while len(aList):
        a = aList.pop()
        for b in aList:
            distribution[a-b] += 1
    return distribution

def computeConsecutiveDiffDistribution(aList):
    """
    Create an { Integer -> Integer } map (defaultdict) where the keys are
    consecutive differences in the possibly onsorted input list, and the values
    are the number of time that difference shows up
    """
    aList = copy(aList)
    distribution = defaultdict(int)
    if len(aList):
        a = aList.pop()
        while len(aList):
            b = aList.pop()
            distribution[a-b] += 1
            a = b
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
minI=2
maxI=128
iRange = range(minI, maxI + 1)

for i in iRange:
    orbit = genCollatzOrbit(i)
    print(f"Consecutive Diffs Distribution for {i}")
    diffDist = computeConsecutiveDiffDistribution(orbit)
    printDistribution(diffDist)
    print(f"All Ordered Diffs Distribution for {i}")
    diffDist = computeDiffDistribution(orbit)
    printDistribution(diffDist)
    print()

