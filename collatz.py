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
    #return (2 ** i) - 1
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
    #print(f"  {nListReverse}")
    #print(f"{i:>{widthLargestStart}}: {c:>{widthLargestCount}d} {n:>{widthLargestModifiedStart}d}")
    #print(f"{c:>{widthLargestStart}d} {n:>{widthLargestModifiedStart}d}")
    #print(f"{n:>30d}: {c:>15d}")
    #print(f"{n:>2d}: {c:>3d} - {nList}")
    if (isLoop):
        print("!! LOOP !!")
        print(f"  {n} -> {nList}")
        break

    lastElement = nList[-1]
    tailOffset = countMap[lastElement]
    headCount = len(nList)
    # Subtract 1 for the overlap between lists
    c = headCount + tailOffset - 1
    print(f"{i:>{widthLargestStart}}: {c:>{widthLargestCount}d} {n:>{widthLargestModifiedStart}d}")
    for ii in range(len(nList)):
        nn = nList[ii]
        alreadySeen.add(nn)
        countMap[nn] = (c - ii)

