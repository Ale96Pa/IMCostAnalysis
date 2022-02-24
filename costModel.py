def calculateMissing(dfMiss, dictAlfa, Tmiss):
    tot = dictAlfa["aN"]*dfMiss["missingN"][0]\
    +dictAlfa["aA"]*dfMiss["missingA"][0]\
    +dictAlfa["aK"]*dfMiss["missingK"][0]\
    +dictAlfa["aD"]*dfMiss["missingD"][0]\
    +dictAlfa["aY"]*dfMiss["missingY"][0]\
    +dictAlfa["aR"]*dfMiss["missingR"][0]\
    +dictAlfa["aC"]*dfMiss["missingC"][0]

    if int(dfMiss["missingN"][0])+int(dfMiss["missingA"][0])+int(dfMiss["missingK"][0])+int(dfMiss["missingD"][0])+int(dfMiss["missingY"][0])+int(dfMiss["missingR"][0])+int(dfMiss["missingC"][0]) > Tmiss:
        tot = 1
    return {"costMissing":tot}

def calculateMultiple(dfMult, numEv, dictAlfa, Tmult):
    tot = dictAlfa["aN"]*(int(dfMult["multipleN"][0])/numEv)\
    + dictAlfa["aA"]*(int(dfMult["multipleA"][0])/numEv)\
    + dictAlfa["aW"]*(int(dfMult["multipleW"][0])/numEv)\
    + dictAlfa["aG"]*(int(dfMult["multipleG"][0])/numEv)\
    + dictAlfa["aR"]*(int(dfMult["multipleR"][0])/numEv)\
    + dictAlfa["aC"]*(int(dfMult["multipleC"][0])/numEv)

    if int(dfMult["multipleN"][0]) > Tmult or int(dfMult["multipleA"][0]) > Tmult or int(dfMult["multipleW"][0]) > Tmult:
        tot=1
    return {"costMultiple":tot}

def calculateMismatch(dfMism, numEv, dictAlfa, Tmism):
    tot = dictAlfa["aN"]*(int(dfMism["mismatchN"][0])/numEv) + dictAlfa["aR"]*(int(dfMism["mismatchR"][0])/numEv)

    if int(dfMism["mismatchN"][0]) > Tmism or int(dfMism["mismatchR"][0]) > Tmism:
        tot = 1
    return {"costMismatch":tot}