#!/usr/bin/python3

# Imports
from math import log10
import sqlite3

# Functions
def collatz(n):
    if (n % 2):
        return (3*n+1) // 2
    else:
        return n//2

def gen_collatz(n, cursor):
    start = n
    startBitLen = n.bit_length()
    startHash = hash(n)
    try:
        sql = "INSERT INTO PathDetails (start, startBitLen, hash) VALUES (?,?,?)"
        sqlArgs = (start, startBitLen, startHash)
        cursor.execute(sql, sqlArgs)
    except sqlite3.IntegrityError as error:
        print(f"  Looks like there is already an entry for n = {n} in the database. Gonna proceed anyways.", n)

    isLoop = False
    maxValue = n
    maxBitLen = startBitLen
    nListLen = 1
    while (n > 1):
        n = collatz(n)
        maxValue = max(maxValue, n)
        maxBitLen = max(maxBitLen, n.bit_length())
        nListLen += 1
    try:
        sql = "INSERT OR REPLACE INTO PathDetails (start, startBitLen, hash, pathLen, isLoop, largestValue, largestValueBitLen) VALUES (?,?,?,?,?,?,?)"
        sqlArgs = (start, startBitLen, startHash, nListLen, isLoop, str(maxValue), maxBitLen)
        print(f"Executing: {sql}\n  {sqlArgs}")
        cursor.execute(sql, sqlArgs)
    except OverflowError as error:
        print(f"Error while processing n = {start}. Details: {error}")
        print((start, startBitLen, startHash, nListLen, isLoop, maxValue, maxBitLen))
        raise error
    return nListLen, isLoop, maxBitLen

def modifyStart(i):
    return (2 ** i) - 1

# Main method
minI=1
maxI=30

# Help to stop early when we've seen a degenerate case before
countMap = { 1: 1 }
nToListMap = { 1: [] }

# Printing-help vars
widthLargestStart =         int(log10(maxI)) + 1
widthLargestCount =         int(log10(maxI)) + 2
widthLargestModifiedStart = int(log10(modifyStart(maxI))) + 1

conn = sqlite3.connect("data/collatz.db")
cursor = conn.cursor()
iRange = range(minI, maxI + 1)
for i in iRange:
    n = modifyStart(i)
    nListLen, isLoop, maxBitLen = gen_collatz(n, cursor)

    if (isLoop):
        print("!! LOOP !!")
        print(f"  {n} -> {nListLen}")
        break

conn.commit()
conn.close()
#
#

