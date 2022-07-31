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

def insertInitialDbEntry(start, startBitLen, startHash):
    """
    Insert initial entry for a Collatz path.
    """
    try:
        sql = """INSERT INTO PathDetails (start, startBitLen, hash)
    VALUES (?,?,?)"""
        sqlArgs = (str(start), startBitLen, startHash)
        cursor.execute(sql, sqlArgs)
    except sqlite3.IntegrityError as error:
        print(f"  Looks like there is already an entry in the database for")
        print(f"    start value:       {start}")
        print(f"    Started from seed: {n}")
        print("   Gonna proceed anyways.")
        print(f"    In case it didn't complete in a previous run for this starting value.")
        print(f"    I should add a check to see whether it looks completed.")

def updateDbEntry(start, startBitLen, startHash, nListLen, isLoop, maxValue, maxBitLen):
    """
    Update an entry for a Collatz path with final, full path details.
    """
    try:
        sql = """INSERT OR REPLACE INTO PathDetails (start, startBitLen, hash, pathLen, isLoop, largestValue, largestValueBitLen)
    VALUES (?,?,?,?,?,?,?)"""
        sqlArgs = (str(start), startBitLen, startHash, nListLen, isLoop, str(maxValue), maxBitLen)
        print(f"Executing: {sql}\n  values: {sqlArgs}")
        cursor.execute(sql, sqlArgs)
    except OverflowError as error:
        print(f"Error while processing n = {start}. Details: {error}")
        print((start, startBitLen, startHash, nListLen, isLoop, maxValue, maxBitLen))
        raise error

def checkForExistingDbEntry(start):
    sql = """SELECT count(*) FROM PathDetails WHERE start == (?)"""
    sqlArgs = (str(start),)
    print(f"Executing: {sql}\n  values: {sqlArgs}")
    cursor.execute(sql, sqlArgs)
    (numAlreadyExist,) = cursor.fetchone()
    print(f"  Got: {numAlreadyExist}")
    return (numAlreadyExist > 0)

def getExistingDbEntry(start):
    sql = """SELECT start, startBitLen, hash, pathLen, isLoop, largestValue, largestValueBitLen
FROM PathDetails WHERE start == (?)"""
    sqlArgs = (str(start),)
    print(f"Executing: {sql}\n  values: {sqlArgs}")
    cursor.execute(sql, sqlArgs)
    ret = cursor.fetchone()
    (start, startBitLen, startHash, pathLen, isLoop, largestValue, largestValueBitLen,) = ret
    print(f"  Got: {ret}")
    return pathLen, isLoop, largestValueBitLen

def gen_collatz(n, cursor):
    start = n
    startBitLen = n.bit_length()
    startHash = f"{hash(n):016x}"

    if checkForExistingDbEntry(start):
        print("  Skipping")
        return getExistingDbEntry(start)

    insertInitialDbEntry(start, startBitLen, startHash)

    isLoop = False
    maxValue = n
    maxBitLen = startBitLen
    nListLen = 1
    while (n > 1):
        n = collatz(n)
        maxValue = max(maxValue, n)
        maxBitLen = max(maxBitLen, n.bit_length())
        nListLen += 1
    updateDbEntry(start, startBitLen, startHash, nListLen, isLoop, maxValue, maxBitLen)
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

