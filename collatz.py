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
numIters=15
iRange = range(1, numIters + 1)
initialStart = 0b1001011
START_BIT_LEN_UPPER_BOUND = 10 ** 10
PRINT_STATUS_UDPATE_RATE = 10 ** 6
SAVE_T0_DATABASE=True
databasePath = "data/collatz.07.db"
SHORTCUT_MODULUS = 2 ** 100
SHORTCUT_RESIDUE = SHORTCUT_MODULUS - 1
shortcutMinStepsTillNextShortcut = 10 ** 1
repeatAlreadySeenStarts = True

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

def modifyStart(i):
    ret = i
    return ret

def insertOrUpdateDbEntries(valuesList, tableName = TableNames.PathDetails):
    """
    Update an entry for a Collatz path with final, full path details.
    """
    if (type(tableName) != TableNames):
        raise TypeError(f"Input argument 'tableName' should be of type 'TableNames' but was of type {type(tableName)}, with value {tableName}")
    try:
        sql = f"""INSERT OR REPLACE INTO {tableName.value} (startBitLen, calcTime, pathLen, isLoop, start) VALUES (?,?,?,?,?)"""
        print(f"Executing: {sql}")
        sys.stdout.flush()
        for values in valuesList:
            print(f"  {values[0:-1]}")
            sys.stdout.flush()
        if SAVE_T0_DATABASE:
            cursor.executemany(sql, valuesList)
        else:
            print(f"  skipping - NOT SAVING TO DB")
    except OverflowError as error:
        print(f"Error while processing n = {start}. Details: {error}")
        print((start, startBitLen, nPathLen, isLoop))
        sys.stdout.flush()
        raise error

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
        sys.stdout.flush()
        if SAVE_T0_DATABASE:
            cursor.execute(sql, sqlArgs)
            sys.stdout.flush()
        else:
            print(f"  skipping - NOT SAVING TO DB")
    except OverflowError as error:
        print(f"Error while processing n = {start}. Details: {error}")
        print((start, startBitLen, nPathLen, isLoop))
        sys.stdout.flush()
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


    # Initial SQL-relevant values
    start = n
    startBitLen = n.bit_length()
    startTime = getTimeInMillis()
    isLoop = None
    nPathLen = 1
    print(f"Starting new collatz orbit | bit_len = {startBitLen} | start = {start}")
    sys.stdout.flush()

    shortcutsToRemember = list()
    shortcutCalcTime = 0
    while (n > 1):
        n = collatz(n)
        nPathLen += 1
        if (nPathLen % PRINT_STATUS_UDPATE_RATE == 0):
            print(f"  completed step # {nPathLen}")
        if (n in shortcutsToRemember):
            isLoop = True
            break

        appendShortcut = False
        if (n > SHORTCUT_RESIDUE):
            nShortcutResidue = n % SHORTCUT_MODULUS
            if (nShortcutResidue == SHORTCUT_RESIDUE):
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
    if len(shortcutsToRemember) == 0:
        return
    valuesList = []
    for (nShortcut, nShortcutPathLenAdjust, nShortcutCalcTime) in shortcutsToRemember:
        shortcutPathLen = nPathLen + nShortcutPathLenAdjust
        shortcutCalcTime = endTime - nShortcutCalcTime
        print(f"Shortcut add | pathLen adjustment {nShortcutPathLenAdjust} | calcTime to encounter this shortcut {nShortcutCalcTime} | shortcutCalcTime {shortcutCalcTime} | pathLen {shortcutPathLen} | {nShortcut}")
        sys.stdout.flush()
        values = (nShortcut.bit_length(), shortcutCalcTime, shortcutPathLen, isLoop, str(nShortcut))
        valuesList.append(values)
    insertOrUpdateDbEntries(valuesList, TableNames.ShortcutDetails)

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
        sys.stdout.flush()
        break

    n = n + (1 << (nPathLen - n.bit_length()))
    if n.bit_length() > START_BIT_LEN_UPPER_BOUND:
        print(f"""The next start value has {n.bit_length()} bits.
This exceeds the allowed upper bound of {START_BIT_LEN_UPPER_BOUND} bits.
So we are stopping this execution""")
        break
    print()
    sys.stdout.flush()

# SQL connection and query vars - close
conn.commit()
conn.close()

