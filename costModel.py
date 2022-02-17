def calculateMissing(dfMiss):
    countMiss = 0
    if dfMiss["missingN"][0] == True:
        countMiss+=1
    if dfMiss["missingA"][0] == True:
        countMiss+=1
    if dfMiss["missingR"][0] == True:
        countMiss+=1
    if dfMiss["missingC"][0] == True:
        countMiss+=1
    tot = 0.25*countMiss
    return {"costMissing":tot}
    

def calculateMultiple(dfMult, numEv):
    tot = (int(dfMult["multipleN"][0])/numEv) + (int(dfMult["multipleA"][0])/numEv) + (int(dfMult["multipleW"][0])/numEv) + (int(dfMult["multipleR"][0])/numEv) + (int(dfMult["multipleC"][0])/numEv)
    return {"costMultiple":tot}

def calculateMismatch(dfMism, numEv):
    countMism = 0
    countMism+=dfMism["mismatchN"][0]
    countMism+=dfMism["mismatchR"][0]
    return {"costMismatch":countMism/numEv}