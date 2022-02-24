import pandas as pd

def areSame(str1,str2):
    if "new" in str1 and "new" in str2:
        return True
    if "active" in str1 and "active" in str2:
        return True
    if "awaiting" in str1 and "awaiting" in str2:
        return True
    if "resolved" in str1 and "resolved" in str2:
        return True
    if "closed" in str1 and "closed" in str2:
        return True
    if "assign" in str1 and "assign" in str2:
        return True
    if "double" in str1 and "double" in str2:
        return True
    if "notif" in str1 and "notif" in str2:
        return True
    if "know" in str1 and "know" in str2:
        return True
    return False

# MISSING ACTIVITIES
    # Check if any of the activity is missing
    # Error description: an activity is missing in the right step of the process
    # Output: Dict of boolean
def detectMissingInTrace(trace, isEnriched):
    missingDict = {"N":1,"A":1,"D":int(isEnriched),"Y":int(isEnriched),"K":int(isEnriched),"R":1,"C":1}

    for activity in trace:
        if "S" in activity and "NEW" in activity:
            missingDict["N"] = 0
        elif "S" in activity and ("ACTIVE" in activity or "priority" in activity or "classification" in activity):
            missingDict["A"] = 0
        elif "S" in activity and "RESOLVED" in activity:
            missingDict["R"] = 0
        elif "S" in activity and "CLOSED" in activity:
            missingDict["C"] = 0
        elif isEnriched and "S" in activity and "DOUBLE CHECK" in activity:
            missingDict["D"] = 0
        elif isEnriched and "S" in activity and "NOTIFICATION" in activity:
            missingDict["Y"] = 0
        elif isEnriched and "S" in activity and "KB" in activity:
            missingDict["K"] = 0

    dfMissing = pd.DataFrame.from_dict(missingDict, orient='index').transpose().rename(columns={"N": "missingN", "A": "missingA", "D": "missingD", "Y": "missingY","K": "missingK", "R": "missingR", "C": "missingC"})
    return dfMissing

# MULTIPLE ACTIVITIES
    # Check how many times activities are repeated in the trace
    # Error description: an activity is repeated multiple times
    # Output: Dict of array of int
def detectMultipleInTrace(trace):
    multipleDic = {"N":0,"A":0,"W":0,"G":0,"R":0,"C":0}
    counterN=0
    counterA=0
    counterW=0
    counterG=0
    counterR=0
    counterC=0

    prevActivity = trace[0]
    for i in range(1,len(trace)-1):
        currActivity = trace[i]
        if areSame(prevActivity.lower(),currActivity.lower()):
            if "new" in currActivity.lower():
                counterN +=1
            elif"active" in currActivity.lower():
                counterA +=1
            elif "resolved" in currActivity.lower():
                counterR += 1
            elif "closed" in currActivity.lower():
                counterC += 1
            elif "awaiting" in currActivity.lower():
                counterW +=1
            elif "assign" in currActivity.lower():
                counterG +=1
        prevActivity = currActivity

    multipleDic["N"] = counterN
    multipleDic["A"] = counterA
    multipleDic["W"] = counterW
    multipleDic["G"] = counterG
    multipleDic["R"] = counterR
    multipleDic["C"] = counterC

    dfMultiple = pd.DataFrame.from_dict(multipleDic, orient='index').transpose().rename(columns={"N": "multipleN", "A": "multipleA", "W": "multipleW", "G": "multipleG", "R": "multipleR", "C": "multipleC"})
    return dfMultiple

# MISMATCHING ORDER
    # Check how many times the incident has been reopened (e.g., Resolved followed by new,active or awating activity)
    # Output: int
def detectMismatchingInTrace(trace):
    mismatchDic = {"N":0,"R":0}
    cntN = cntR = 0
    prevActivity = trace[0]
    for i in range(1,len(trace)-1):
        currActivity = trace[i]
        #if "resolved" in prevActivity.lower() and not ("resolved" in currActivity.lower() or "closed" in currActivity.lower()):
        if "resolved" in prevActivity.lower() and not ("closed" in currActivity.lower() or "notification" in currActivity.lower() or "resolved" in currActivity.lower()):
            cntR +=1
        if "new" not in prevActivity.lower() and "new" in currActivity.lower():
            cntN +=1
        prevActivity = currActivity
    
    mismatchDic["N"] = cntN
    mismatchDic["R"] = cntR

    dfMismatch = pd.DataFrame.from_dict(mismatchDic, orient='index').transpose().rename(columns={"N": "mismatchN", "R": "mismatchR"})
    return dfMismatch