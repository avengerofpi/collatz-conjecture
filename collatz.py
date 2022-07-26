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
    maxBitLen = n.bit_length()
    isLoop = False
    while (n > 1):
        n = collatz(n)
        nList.append(n)
        maxBitLen = max(maxBitLen, n.bit_length())
        if (nList.count(n) > 1):
            isLoop = True
            break
    return nList, isLoop, maxBitLen

def modifyStart(i):
    return (2 ** i) - 1
    
# Main method
minI=1
maxI=30

# Help to stop early when we've seen a degenerate case before
countMap = { 1: 1 }
nToListMap = { 1: [] }
nList_lengthList = list()

# Printing-help vars
widthLargestStart =         int(log10(maxI)) + 1
widthLargestCount =         int(log10(maxI)) + 2
widthLargestModifiedStart = int(log10(modifyStart(maxI))) + 1

iRange = range(minI, maxI + 1)
for i in iRange:
    n = modifyStart(i)
    nList, isLoop, maxBitLen = gen_collatz(n)

    if (isLoop):
        print("!! LOOP !!")
        print(f"  {n} -> {nList}")
        break

    lastElement = nList[-1]
    print(f"{i:>{widthLargestStart}} -> {n:>{widthLargestModifiedStart}d} ({len(nList):>6} steps before a short-circuit route was encountered: {lastElement})")
    nListLen = len(nList)
    nList_lengthList.append(nListLen)

# Graph
# Scatterplot (see https://matplotlib.org/stable/plot_types/index
# for a list of matplotlib plot types
import matplotlib.pyplot as plt
import numpy as np
import inspect
import re

plt.style.use('_mpl-gallery')

# make the data
x = iRange
y = nList_lengthList
yFlattened = [ y[i] - x[i] for i in range(len(x))]
print(f"x: {x}")
print(f"y: {y}")
# size and color:
#sizes = np.random.uniform(15, 80, len(x))
#colors = np.random.uniform(15, 80, len(x))
plt.plot(x, y, 'b.')
plt.plot(x, yFlattened, 'r.')

plt.xlabel(f"Lengths of Collatz paths for {re.sub('.*return |def .*', '', inspect.getsource(modifyStart), re.DOTALL)}")

plt.title(f"{inspect.getsource(modifyStart)}")
plt.title('hello world', loc='center')
plt.subplots_adjust(left=0.05, bottom=0.10, right=0.97, top=0.95, wspace=None, hspace=None)

# plot
#fig, ax = plt.subplots()
#
#ax.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=100)
#
#ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
#       ylim=(0, 8), yticks=np.arange(1, 8))

plt.show()

