import pandas as pd

# MISSING ACTIVITIES
    # CHeck if any of the activity N,A,R,C is missing
    # Error description: an activity is missing in the right step of the process
    # Output: Dict of boolean
def detectMissingInTrace(trace):
    missingDict = {"N":True,"A":True,"R":True,"C":True}

    for activity in trace:
        if "S" in activity and "NEW" in activity:
            missingDict["N"] = False
        elif "S" in activity and ("ACTIVE" in activity or "priority" in activity or "classification" in activity):
            missingDict["A"] = False
        elif "S" in activity and "RESOLVED" in activity:
            missingDict["R"] = False
        elif "S" in activity and "CLOSED" in activity:
            missingDict["C"] = False

    # print("Missing activities")
    dfMissing = pd.DataFrame.from_dict(missingDict, orient='index').transpose().rename(columns={"N": "missingN", "A": "missingA", "R": "missingR", "C": "missingC"})
    # print(dfMissing)
    return dfMissing


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
    return False
    

# MULTIPLE ACTIVITIES
    # Check how many times activities are repeated in the trace
    # Error description: an activity is repeated multiple times
    # Output: Dict of array of int
# MULTIPLE ACTIVITIES
    # Check how many times activities are repeated in the trace
    # Error description: an activity is repeated multiple times
    # Output: Dict of array of int
def detectMultipleInTrace(trace):
    multipleDic = {"N":0,"A":0,"W":0,"R":0,"C":0}
    counterN=0
    counterA=0
    counterW=0
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
        prevActivity = currActivity

    multipleDic["N"] = counterN
    multipleDic["A"] = counterA
    multipleDic["W"] = counterW
    multipleDic["R"] = counterR
    multipleDic["C"] = counterC

    # multipleDic["N"] = cntN
    # multipleDic["A"] = cntA
    # multipleDic["W"] = cntW
    # multipleDic["R"] = cntR
    # multipleDic["C"] = cntC

    # print("Multiple activities")
    dfMultiple = pd.DataFrame.from_dict(multipleDic, orient='index').transpose().rename(columns={"N": "multipleN", "A": "multipleA", "W": "multipleW", "R": "multipleR", "C": "multipleC"})
    # print(dfMultiple)
    return dfMultiple

# def detectMultipleInTrace(trace):
#     multipleDic = {"N":[],"A":[],"W":[],"R":[],"C":[]}
#     counterN=0
#     counterA=0
#     counterW=0
#     counterR=0
#     counterC=0
#     cntN=[]
#     cntA=[]
#     cntW=[]
#     cntR=[]
#     cntC=[]

#     prevActivity = trace[0]
#     for i in range(1,len(trace)-1):
#         currActivity = trace[i]
#         if areSame(prevActivity.lower(),currActivity.lower()):
#             if "new" in currActivity.lower():
#                 counterN +=1
#             elif"active" in currActivity.lower():
#                 counterA +=1
#             elif "resolved" in currActivity.lower():
#                 counterR += 1
#             elif "closed" in currActivity.lower():
#                 counterC += 1
#             elif "awaiting" in currActivity.lower():
#                 counterW +=1
#         else:
#             cntN.append(counterN)
#             cntA.append(counterA)
#             cntW.append(counterW)
#             cntR.append(counterR)
#             cntC.append(counterC)
#             counterN=0
#             counterA=0
#             counterW=0
#             counterR=0
#             counterC=0
#         prevActivity = currActivity

#     cntN = [i for i in cntN if i != 0]
#     cntA = [i for i in cntA if i != 0]
#     cntW = [i for i in cntW if i != 0]
#     cntR = [i for i in cntR if i != 0]
#     cntC = [i for i in cntC if i != 0]
#     multipleDic["N"] = ''.join(str(e) for e in cntN).replace(" ",";")
#     multipleDic["A"] = ''.join(str(e) for e in cntA).replace(" ",";")
#     multipleDic["W"] = ''.join(str(e) for e in cntW).replace(" ",";")
#     multipleDic["R"] = ''.join(str(e) for e in cntR).replace(" ",";")
#     multipleDic["C"] = ''.join(str(e) for e in cntC).replace(" ",";")

#     # multipleDic["N"] = cntN
#     # multipleDic["A"] = cntA
#     # multipleDic["W"] = cntW
#     # multipleDic["R"] = cntR
#     # multipleDic["C"] = cntC

#     # print("Multiple activities")
#     dfMultiple = pd.DataFrame.from_dict(multipleDic, orient='index').transpose().rename(columns={"N": "multipleN", "A": "multipleA", "W": "multipleW", "R": "multipleR", "C": "multipleC"}).replace(r'^\s*$', 0, regex=True)
#     # print(dfMultiple)
#     return dfMultiple

# MISMATCHING ORDER
    # Check how many times the incident has been reopened (e.g., Resolved followed by new,active or awating activity)
    # Output: int
def detectMismatchingInTrace(trace):
    mismatchDic = {"N":0,"R":0}
    cntN = cntR = 0
    prevActivity = trace[0]
    for i in range(1,len(trace)-1):
        currActivity = trace[i]
        if "resolved" in prevActivity.lower() and not ("resolved" in currActivity.lower() or "closed" in currActivity.lower()):
            cntR +=1
        if "new" not in prevActivity.lower() and "new" in currActivity.lower():
            cntN +=1
        prevActivity = currActivity
    
    mismatchDic["N"] = cntN
    mismatchDic["R"] = cntR

    # print("Mismarching order")
    dfMismatch = pd.DataFrame.from_dict(mismatchDic, orient='index').transpose().rename(columns={"N": "mismatchN", "R": "mismatchR"})
    # print(dfMismatch)
    return dfMismatch