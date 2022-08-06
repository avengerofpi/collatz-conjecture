#!/usr/bin/python3

# Imports
from math import log10
import sqlite3
import hashlib
import sys

# Main parameters
minI=1
maxI=30
iRange = range(minI, maxI + 1)
databasePath = "data/collatz.02.db"

# Functions
def collatz(n):
    if (n % 2):
        return (3*n+1) // 2
    else:
        return n//2

def insertInitialDbEntry(start, startBitLen):
    """
    Insert initial entry for a Collatz path.
    """
    try:
        sql = """INSERT INTO PathDetails (start, startBitLen)
    VALUES (?,?)"""
        sqlArgs = (str(start), startBitLen)
        cursor.execute(sql, sqlArgs)
    except sqlite3.IntegrityError as error:
        print(f"  Looks like there is already an entry in the database for")
        print(f"    start value:       {start}")
        print(f"    Started from seed: {n}")

def updateDbEntry(start, startBitLen, nPathLen, isLoop):
    """
    Update an entry for a Collatz path with final, full path details.
    """
    try:
        sql = """INSERT OR REPLACE INTO PathDetails (start, startBitLen, pathLen, isLoop) VALUES (?,?,?,?)"""
        sqlArgs = (str(start), startBitLen, nPathLen, isLoop)
        print(f"Executing: {sql} | {sqlArgs}")
        cursor.execute(sql, sqlArgs)
    except OverflowError as error:
        print(f"Error while processing n = {start}. Details: {error}")
        print((start, startBitLen, nPathLen, isLoop))
        raise error

def checkForExistingDbEntry(start):
    sql = """SELECT count(*) FROM PathDetails WHERE start == (?)"""
    sqlArgs = (str(start),)
    print(f"Executing: {sql} | {sqlArgs}", end="")
    cursor.execute(sql, sqlArgs)
    (numAlreadyExist,) = cursor.fetchone()
    print(f" | Got: {numAlreadyExist}")
    return (numAlreadyExist > 0)

def getExistingDbEntry(start):
    return getPathLen(start)

def getPathLen(start):
    sql = """SELECT start, startBitLen, pathLen, isLoop FROM PathDetails WHERE start == (?)"""
    sqlArgs = (str(start),)
    print(f"Executing: {sql} | {sqlArgs}", end="")
    cursor.execute(sql, sqlArgs)
    ret = cursor.fetchone()
    (start, startBitLen, pathLen, isLoop,) = ret
    print(f" | Got: {ret}")
    return pathLen

def getShortcutDetails(n):
    sql = """SELECT start, startBitLen, pathLen, isLoop FROM PathDetails WHERE start == (?)"""
    sqlArgs = (str(n),)
    print(f"Executing: {sql} | {sqlArgs}", end="")
    cursor.execute(sql, sqlArgs)
    ret = cursor.fetchone()
    (n, startBitLen, pathLen, isLoop,) = ret
    print(f" | Got: {ret}")
    return pathLen, isLoop

def gen_collatz(n, cursor):
    # Use this modulus and this residue to flag intermediate
    # value along Collatz paths that should be tracked, to help
    # with short-circuiting future paths
    shortcutModulus = 2 ** 10
    shortcutResidue = 1

    if checkForExistingDbEntry(n):
        print("  Seen before, but continuing anyways")

    start = n
    startBitLen = n.bit_length()

    insertInitialDbEntry(start, startBitLen)

    # Max values seen since the last shortcut value
    isLoop = None
    nPathLen = 1

    nShortcut = n % shortcutModulus
    shortcutsToRemember = list()
    while (n > 1):
        n = collatz(n)
        nPathLen += 1

        # Update and check the shortcut
        nShortcut = n % shortcutModulus
        if (n > shortcutResidue) and (nShortcut == shortcutResidue):
            print(f"FOUND A SHORTCUT CANDIDATE: {n} = {nShortcut} (mod {shortcutModulus}) | at path step {nPathLen}")
            # Check if this shortcut has been seen during this path.
            # If yes, we have a loop!
            if (n in shortcutsToRemember):
                isLoop = True

            # See if the current value of n has been seen before.
            # If yes, use the details from that saved value and
            # update the list of save nShortcut values.
            # If not, save this value of nShortcut to a list
            # for later insertion.
            if checkForExistingDbEntry(n):
                shortcutPathLen, shortcutIsLoop = getShortcutDetails(n)
                nPathLen += (shortcutPathLen - 1)
                isLoop = shortcutIsLoop
                break
            else:
                shortcutsToRemember.append((n, -(nPathLen - 1),))

    updateDbEntry(start, startBitLen, nPathLen, isLoop)
    saveNewShortcutEntries(nPathLen, shortcutsToRemember, isLoop)

    # Save latest changes to database
    conn.commit()

    return nPathLen, isLoop

def saveNewShortcutEntries(nPathLen, shortcutsToRemember, isLoop):
    for (nShortcut, nShortcutPathLenAdjust,) in shortcutsToRemember:
        shortcutPathLen = nPathLen + nShortcutPathLenAdjust
        print(f"Shortcut add: {nShortcut} | pathLen adjustment {nShortcutPathLenAdjust} | pathLen {shortcutPathLen}")
        updateDbEntry(nShortcut, nShortcut.bit_length(), shortcutPathLen, isLoop)

def modifyStart(i):
    ret = (2 ** i) - 1
    print(f"modifyStart: {i} -> {ret}")
    return ret

def md5hash(a):
    f = hashlib.md5()
    f.update(bytes(str(a), 'utf-8'))
    ret = f.hexdigest()
    print(f"md5hash:  {ret}")
    return ret

# SQL connection and query vars
conn = sqlite3.connect(databasePath)
cursor = conn.cursor()

# Main method
for i in iRange:
    n = modifyStart(i)
    nPathLen, isLoop = gen_collatz(n, cursor)

    if (isLoop):
        print("!! LOOP !!")
        print(f"  {n} -> {nPathLen}")
        break

    print()
    sys.stdout.flush()

conn.commit()
conn.close()

