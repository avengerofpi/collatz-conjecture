#!/usr/bin/python3

# Imports
from enum import Enum
from time import time
import sqlite3
import sys

# Main parameters
#minI=83112
#maxI=100000
#iRange = range(minI, maxI + 1)
numIters=10
iRange = range(numIters)
initialStart = 3
databasePath = "data/collatz.04.db
shortcutModulus = 2 ** 10
shortcutResidue = 1
repeatAlreadySeenStarts = False
shortcutMinStepsTillNextShortcut = 10 ** 5

# Helper class to enforce table names
# (poor-quality attempt to avoid SQL injection attack)
class TableNames(Enum):
    PathDetails = "PathDetails"
    ShortcutDetails = "ShortcutDetails"

# Functions
def collatz(n):
    if (n % 2):
        return (3*n+1) // 2
    else:
        return n//2

def updateDbEntry(start, startBitLen, calcTime, nPathLen, isLoop, tableName = TableNames.PathDetails):
    """
    Update an entry for a Collatz path with final, full path details.
    """
    if (type(tableName) != TableNames):
        raise TypeError(f"Input argument 'tableName' should be of type 'TableNames' but was of type {type(tableName)}, with value {tableName}")
    try:
        sql = f"""INSERT OR REPLACE INTO {tableName.value} (startBitLen, calcTime, pathLen, isLoop, start) VALUES (?,?,?,?,?)"""
        sqlArgs = (startBitLen, calcTime, nPathLen, isLoop, str(start))
        print(f"Executing: {sql} | {sqlArgs[0:-1]}")
        cursor.execute(sql, sqlArgs)
    except OverflowError as error:
        print(f"Error while processing n = {start}. Details: {error}")
        print((start, startBitLen, nPathLen, isLoop))
        raise error

def updateShortcutEntry(start, startBitLen, calcTime, nPathLen, isLoop):
    """
    Update an entry for a Collatz path with final, full path details.
    """
    updateDbEntry(start, startBitLen, calcTime, nPathLen, isLoop, tableName = TableNames.ShortcutDetails)

def checkForExistingEntry(start, tableName):
    if (type(tableName) != TableNames):
        raise TypeError(f"Input argument 'tableName' should be of type 'TableNames' but was of type {type(tableName)}, with value {tableName}")
    sql = f"""SELECT count(*) FROM {tableName.value} WHERE start == (?)"""
    sqlArgs = (str(start),)
    #print(f"Executing: {sql} | {sqlArgs}", end="")
    cursor.execute(sql, sqlArgs)
    (numAlreadyExist,) = cursor.fetchone()
    #print(f" | Got: {numAlreadyExist}")
    return (numAlreadyExist > 0)

def checkForExistingStartEntry(start):
    return checkForExistingEntry(start, TableNames.PathDetails)

def checkForExistingShortcutEntry(start):
    return checkForExistingEntry(start, TableNames.ShortcutDetails)

def getShortcutDetails(n):
    sql = f"""SELECT start, startBitLen, pathLen, calcTime, isLoop FROM {TableNames.ShortcutDetails.value} WHERE start == (?)"""
    sqlArgs = (str(n),)
    #print(f"Executing: {sql} | {sqlArgs}", end="")
    cursor.execute(sql, sqlArgs)
    ret = cursor.fetchone()
    (n, startBitLen, pathLen, calcTime, isLoop,) = ret
    #print(f" | Got: {ret}")
    return pathLen, calcTime, isLoop

def gen_collatz(n):
    # Use this modulus and this residue to flag intermediate
    # value along Collatz paths that should be tracked, to help
    # with short-circuiting future paths

    if checkForExistingStartEntry(n):
        if repeatAlreadySeenStarts:
            print("  Seen before, but continuing anyways (REPEATING)")
        else:
            print("  Seen before, NOT repeating")

    # Initial SQL-relevant values
    start = n
    startBitLen = n.bit_length()
    startTime = getTimeInMillis()
    isLoop = None
    nPathLen = 1

    nShortcut = n % shortcutModulus
    shortcutsToRemember = list()
    shortcutCalcTime = 0
    while (n > 1):
        n = collatz(n)
        nPathLen += 1

        # Update and check the shortcut
        nShortcut = n % shortcutModulus
        shortcutCalcTime = 0
        if (n > shortcutResidue) and (nShortcut == shortcutResidue):
            print(f"FOUND A SHORTCUT CANDIDATE at path step {nPathLen} | {nShortcut} (mod {shortcutModulus})")
            # Check if this shortcut has been seen during this path.
            # If yes, we have a loop!
            if (n in shortcutsToRemember):
                isLoop = True

            # See if the current value of n has been seen before.
            # If yes, use the details from that saved value and
            # update the list of save nShortcut values.
            # If not, save this value of nShortcut to a list
            # for later insertion.
            if checkForExistingShortcutEntry(n):
                shortcutPathLen, shortcutCalcTime, shortcutIsLoop = getShortcutDetails(n)
                nPathLen += (shortcutPathLen - 1)
                isLoop = shortcutIsLoop
                break
            else:
                # Only append a new shortcut if it is the first shortcut or is at least
                # shortcutMinStepsTillNextShortcut steps after the previous shorcut.
                appendShortcut = True
                if (len(shortcutsToRemember) != 0):
                    prevShortcut, prevShortcutPathLenAdjustment, prevShortcutCalcTime = shortcutsToRemember[-1]
                    appendShortcut = ((nPathLen + prevShortcutPathLenAdjustment) > shortcutMinStepsTillNextShortcut)
                if appendShortcut:
                    shortcutPathLenAdjustment = -(nPathLen - 1)
                    shortcutCalcTime = getTimeInMillis()
                    shortcutsToRemember.append((n, shortcutPathLenAdjustment, shortcutCalcTime))

    # Get end time
    endTime = getTimeInMillis()
    calcTime = (endTime - startTime) + shortcutCalcTime
    projectedEndTime = endTime + shortcutCalcTime

    # SQL interactions
    updateDbEntry(start, startBitLen, calcTime, nPathLen, isLoop)
    saveNewShortcutEntries(nPathLen, projectedEndTime, shortcutsToRemember, isLoop)

    # Save latest changes to database
    conn.commit()

    return nPathLen, isLoop

def saveNewShortcutEntries(nPathLen, endTime, shortcutsToRemember, isLoop):
    for (nShortcut, nShortcutPathLenAdjust, nShortcutCalcTime) in shortcutsToRemember:
        shortcutPathLen = nPathLen + nShortcutPathLenAdjust
        shortcutCalcTime = endTime - nShortcutCalcTime
        print(f"Shortcut add | pathLen adjustment {nShortcutPathLenAdjust} | calcTime to encounter this shortcut {nShortcutCalcTime} | shortcutCalcTime {shortcutCalcTime} | pathLen {shortcutPathLen} |  {nShortcut}")
        updateShortcutEntry(nShortcut, nShortcut.bit_length(), shortcutCalcTime, shortcutPathLen, isLoop)

def modifyStart(i):
    ret = (2 ** i) - 1
    print(f"modifyStart: {i} -> {ret}")
    return ret

def getTimeInMillis():
    return int(time() * 1000)

# Main method
# SQL connection and query vars - open
conn = sqlite3.connect(databasePath)
cursor = conn.cursor()

# Main loop
n = initialStart
for i in iRange:
    #n = modifyStart(i)
    nPathLen, isLoop = gen_collatz(n)

    if (isLoop):
        print("!! LOOP !!")
        print(f"  {n} -> {nPathLen}")
        break

    n = n + (1 << (n.bit_length() + nPathLen - 1))
    print()
    sys.stdout.flush()

# SQL connection and query vars - close
conn.commit()
conn.close()

