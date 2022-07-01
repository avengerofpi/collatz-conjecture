#!/usr/bin/python3

# Imports
from math import log10

# Functions
def collatz(n):
    if (n % 2):
        return (3*n+1) // 2
    else:
        return n//2

def gen_collatz(n):
    nList = [n]
    isLoop = False
    while ((n > 1) and not (n in alreadySeen)):
        n = collatz(n)
        nList.append(n)
        if (nList.count(n) > 1):
            isLoop = True
            break
    return nList, isLoop

def modifyStart(i):
    return (2 ** i) + 1
    
# Main method
minI=1
maxI=100

# Help to stop early when we've seen a degenerate case before
alreadySeen = set()
countMap = { 1: 1 }
nToListMap = { 1: [] }

# Printing-help vars
widthLargestStart =         int(log10(maxI)) + 1
widthLargestCount =         int(log10(maxI)) + 2
widthLargestModifiedStart = int(log10(modifyStart(maxI))) + 1

for i in range(minI, maxI):
    n = modifyStart(i)
    nList, isLoop = gen_collatz(n)
    if (isLoop):
        print("!! LOOP !!")
        print(f"  {n} -> {nList}")
        break

    lastElement = nList[-1]
    # Subtract 1 for the overlap between lists
    # Switch to keeping track of a subset of previously seen values, to avoid memory overload
    print(f"{i:>{widthLargestStart}} -> {n:>{widthLargestModifiedStart}d} ({len(nList):>6} steps before a short-circuit route was encountered: {lastElement})")
    alreadySeen.add(n)
    nListLen = len(nList)
    if (nListLen >= 100):
        decimateStepSize = (nListLen - (nListLen % 10)) // 10
        for ii in range(0, nListLen, decimateStepSize):
            a = nList[ii]
            print(a)
            alreadySeen.add(nList[ii])
    for ii in range(len(nList)):
        nn = nList[ii]
        alreadySeen.add(nn)

