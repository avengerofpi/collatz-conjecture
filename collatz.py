#!/usr/bin/python3

# Imports
from math import log10

# Functions
def collatz(n):
    if (n % 2):
        return (3*n+1) // 2
    else:
        return n//2

def count_collatz(n):
    c = 0
    nList = [n]
    while n > 1:
        c = c+1
        n = collatz(n)
        nList.append(n)
    return c, nList

def modifyStart(i):
    #return (2 ** i) - 1
    return (2 ** i) + 1
    
# Main method
minI=1
maxI=100
widthLargestStart =         int(log10(maxI)) + 1
widthLargestCount =         int(log10(maxI)) + 2
widthLargestModifiedStart = int(log10(modifyStart(maxI))) + 1

for i in range(minI, maxI):
    n = modifyStart(i)
    c, nList = count_collatz(n)
    nListReverse = list(nList)
    nListReverse.reverse()
    print(f"{i:>{widthLargestStart}}: {c:>{widthLargestCount}d} {n:>{widthLargestModifiedStart}d}")
    #print(f"  {nListReverse}")
    #print(f"{i:>{widthLargestStart}}: {c:>{widthLargestCount}d} {n:>{widthLargestModifiedStart}d}")
    #print(f"{c:>{widthLargestStart}d} {n:>{widthLargestModifiedStart}d}")
    #print(f"{n:>30d}: {c:>15d}")
    #print(f"{n:>2d}: {c:>3d} - {nList}")

