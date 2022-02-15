# MISSING ACTIVITIES
    # Se non contiene N,A,R o C --> errore è missing N/A/R/C
    # L'errore è la mancanza di un'attività nel posto giusto
def detectMissingInTrace(trace):
    counter = [0,0,0,0] #N,A,R,C

    for elem in trace:
        if "S" in elem and "NEW" in elem:
            counter[0] = 1
        elif "S" in elem and "ACTIVE" in elem:
            counter[1] = 1
        elif "S" in elem and "RESOLVED" in elem:
            counter[2] = 1
        elif "S" in elem and "CLOSED" in elem:
            counter[3] = 1
    missingDict = {"N":False,"A":False,"R":False,"C":False}
    if counter[0] == 0:
        missingDict["N"] = True
    if counter[1] == 0:
        missingDict["A"] = True
    if counter[2] == 0:
        missingDict["R"] = True
    if counter[3] == 0:
        missingDict["C"] = True

    print("Missing activities")
    print(missingDict)
    return missingDict


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
    #Si valuta quante volte consecutive è ripetuto ogni attività
def detectMultipleInTrace(trace):
    counterN=0
    counterA=0
    counterW=0
    counterR=0
    counterC=0

    cntN=[]
    cntA=[]
    cntW=[]
    cntR=[]
    cntC=[]

    oldElem = trace[0]
    for i in range(1,len(trace)-1):
        elem = trace[i]
        if areSame(oldElem.lower(),elem.lower()):
            if "new" in elem.lower():
                counterN +=1
            elif"active" in elem.lower():
                counterA +=1
            elif "resolved" in elem.lower():
                counterR += 1
            elif "closed" in elem.lower():
                counterC += 1
            elif "awaiting" in elem.lower():
                counterW +=1
        else:
            cntN.append(counterN)
            cntA.append(counterA)
            cntW.append(counterW)
            cntR.append(counterR)
            cntC.append(counterC)
            counterN=0
            counterA=0
            counterW=0
            counterR=0
            counterC=0
        oldElem = elem

    multipleDic = {"N":[],"A":[],"W":[],"R":[],"C":[]}

    cntN = [i for i in cntN if i != 0]
    multipleDic["N"] = cntN

    cntA = [i for i in cntA if i != 0]
    multipleDic["A"] = cntA

    cntW = [i for i in cntW if i != 0]
    multipleDic["W"] = cntW

    cntR = [i for i in cntR if i != 0]
    multipleDic["R"] = cntR

    cntC = [i for i in cntC if i != 0]
    multipleDic["C"] = cntC

    print("Multiple activities")
    print(multipleDic)
    return multipleDic

# MISMATCHING ORDER
    # Si valuta quando RESOLVED non è seguito da RESOLVED/CLOSED
def detectMismatchingInTrace(trace):
    counter = 0
    oldElem = trace[0]
    for i in range(1,len(trace)-1):
        elem = trace[i]
        if "resolved" in oldElem.lower() and not ("resolved" in elem.lower() or "closed" in elem.lower()):
            counter +=1
        oldElem = elem

    print("Mismarching order")
    print(counter)
    return counter