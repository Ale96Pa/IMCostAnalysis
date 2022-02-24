import pandas as pd
import json
import statistics

def buildCategories(resultFile, outputCat):
    dfChecking = pd.read_csv(resultFile)
    dfResult = pd.DataFrame()

    for i in range(0,len(dfChecking)-1):
        dictCat = json.loads(dfChecking["Categories"].values[i].replace("'", '"'))
        
        listCat = list(dictCat.keys())
        dictByCat = {"mN":0,"mA":0,"mD":0,"mY":0,"mK":0,"mR":0,"mC":0,"nn":0,"aa":0,"ww":0,"gg":0,"rr":0,"cc":0,"n0":0,"r0":0}

        for singleCat in listCat:

            if(dfChecking["missingN"].values[i] == 1):
                dictByCat["mN"] += dictCat[singleCat]
            if(dfChecking["missingA"].values[i] == 1):
                dictByCat["mA"] += dictCat[singleCat]
            if(dfChecking["missingD"].values[i] == 1):
                dictByCat["mD"] += dictCat[singleCat]
            if(dfChecking["missingY"].values[i] == 1):
                dictByCat["mY"] += dictCat[singleCat]
            if(dfChecking["missingR"].values[i] == 1):
                dictByCat["mR"] += dictCat[singleCat]
            if(dfChecking["missingC"].values[i] == 1):
                dictByCat["mC"] += dictCat[singleCat]
            
            if(dfChecking["multipleN"].values[i] > 0):
                dictByCat["nn"] += dictCat[singleCat]
            if(dfChecking["multipleA"].values[i] > 0):
                dictByCat["aa"] += dictCat[singleCat]
            if(dfChecking["multipleW"].values[i] > 0):
                dictByCat["ww"] += dictCat[singleCat]
            if(dfChecking["multipleG"].values[i] > 0):
                dictByCat["gg"] += dictCat[singleCat]
            if(dfChecking["multipleR"].values[i] > 0):
                dictByCat["rr"] += dictCat[singleCat]

            if(dfChecking["mismatchN"].values[i] > 0):
                dictByCat["n0"] += dictCat[singleCat]
            if(dfChecking["mismatchR"].values[i] > 0):
                dictByCat["r0"] += dictCat[singleCat]
            
            dfResult = dfResult.append(pd.DataFrame.from_dict({singleCat: dictByCat}, orient='index'))

    dfResult = dfResult.sort_index()

    finalRes = pd.DataFrame()
    oldCat = dfResult.iloc[0]
    mN=oldCat["mN"]
    mA=oldCat["mA"]
    mD=oldCat["mD"]
    mY=oldCat["mY"]
    mK=oldCat["mK"]
    mR=oldCat["mR"]
    mC=oldCat["mC"]
    nn=oldCat["nn"]
    aa=oldCat["aa"]
    ww=oldCat["ww"]
    gg=oldCat["gg"]
    rr=oldCat["rr"]
    cc=oldCat["cc"]
    n0=oldCat["n0"]
    r0=oldCat["r0"]
    for i in range(1,len(dfResult)-1):
        currCat = dfResult.iloc[i]
        if oldCat.name == currCat.name:
            mN+=currCat["mN"]
            mA+=currCat["mA"]
            mD+=currCat["mD"]
            mY+=currCat["mY"]
            mK+=currCat["mK"]
            mR+=currCat["mR"]
            mC+=currCat["mC"]
            nn+=currCat["nn"]
            aa+=currCat["aa"]
            ww+=currCat["ww"]
            gg+=currCat["gg"]
            rr+=currCat["rr"]
            cc+=currCat["cc"]
            n0+=currCat["n0"]
            r0+=currCat["r0"]
        else:
            finalRes = finalRes.append(pd.DataFrame.from_dict({oldCat.name: {"mN":mN,"mA":mA,"mD":mD,"mY":mY,"mK":mK,"mR":mR,"mC":mC,"nn":nn,"aa":aa,"ww":ww,"gg":gg,"rr":rr,"cc":cc,"n0":n0,"r0":r0}}, orient='index'))
            mN=currCat["mN"]
            mA=currCat["mA"]
            mD=currCat["mD"]
            mY=currCat["mY"]
            mK=currCat["mK"]
            mR=currCat["mR"]
            mC=currCat["mC"]
            nn=currCat["nn"]
            aa=currCat["aa"]
            ww=currCat["ww"]
            gg=currCat["gg"]
            rr=currCat["rr"]
            cc=currCat["cc"]
            n0=currCat["n0"]
            r0=currCat["r0"]
        oldCat = currCat

    finalRes.sort_index().to_csv(outputCat)

def buildCategoriesFitness(resultFile, outputCat):
    dfChecking = pd.read_csv(resultFile)
    dfResult = pd.DataFrame()

    for i in range(0,len(dfChecking)):
        dictCat = json.loads(dfChecking["Categories"].values[i].replace("'", '"'))
        fitVal = dfChecking["Trace Fitness"].values[i]
        
        listCat = list(dictCat.keys())

        for singleCat in listCat:
            dfResult = dfResult.append(pd.DataFrame.from_dict({singleCat: fitVal}, orient='index'))

    dfResult = dfResult.sort_index().rename(columns={0: "fitness"})

    finalRes = pd.DataFrame()
    oldCat = dfResult.iloc[0]
    listFit=[]
    listFit.append(oldCat["fitness"])
    for i in range(1,len(dfResult)):
        currCat = dfResult.iloc[i]
        if oldCat.name == currCat.name:
            listFit.append(currCat["fitness"])
        else:
            finalRes = finalRes.append(pd.DataFrame.from_dict({oldCat.name: listFit}, orient='index'))
            listFit=[]
            listFit.append(currCat["fitness"])
        oldCat = currCat

    finalAvgResult = pd.DataFrame()
    for j in range(0,len(finalRes)):
        noNanList = [x for x in finalRes.iloc[j].tolist() if str(x) != 'nan']
        noNanListFloat = [float(i) for i in [x.replace(',', '.') for x in noNanList]]
        finalAvgResult = finalAvgResult.append(pd.DataFrame.from_dict({finalRes.iloc[j].name: statistics.mean(noNanListFloat)}, orient='index'))

    finalAvgResult.sort_index().to_csv(outputCat)



if __name__ == '__main__':
    # buildCategories("result/enrichedResult-equal.csv", "result/categories/enriched-equal-cat.csv")
    # buildCategories("result/enrichedResult-na.csv", "result/categories/enriched-na-cat.csv")
    # buildCategories("result/simpleResult-equal.csv", "result/categories/simple-equal-cat.csv")
    # buildCategories("result/simpleResult-na.csv", "result/categories/simple-na-cat.csv")
    buildCategoriesFitness("result/enrichedResult-equal.csv", "result/categories/enriched-equal-cat-fitness.csv")
    buildCategoriesFitness("result/enrichedResult-na.csv", "result/categories/enriched-na-cat-fitness.csv")
    buildCategoriesFitness("result/simpleResult-equal.csv", "result/categories/simple-equal-cat-fitness.csv")
    buildCategoriesFitness("result/simpleResult-na.csv", "result/categories/simple-na-cat-fitness.csv")
