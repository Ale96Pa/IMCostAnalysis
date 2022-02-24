import pandas as pd
import json

# Prendi i file con categorie e allineamenti
# Per ogni categoria, verifica quali errori ci sono in un dict
# Crea file con lista di errori nelle colonne e categorie nelle righe
# Segna cper ogni categoria quanti errori di ogni tipologia supporta

if __name__ == '__main__':
    dfChecking = pd.read_csv('enriched_result.csv', usecols=['Case IDs','missingN','missingA','missingD','missingY','missingK','missingR','missingC','multipleN','multipleA','multipleW','multipleG','multipleR','multipleC','mismatchN','mismatchR','costMissing','costMultiple','costMismatch','cost','Categories'])
    
    listDictRes = []
    dfResult = pd.DataFrame()

    for i in range(0,len(dfChecking)-1):
        dictCat = json.loads(dfChecking["Categories"].values[i].replace("'", '"'))
        
        listCat = list(dictCat.keys())
        dictByCat = {"mN":0,"mA":0,"mD":0,"mY":0,"mK":0,"mR":0,"mC":0,"nn":0,"aa":0,"ww":0,"gg":0,"rr":0,"cc":0,"n0":0,"r0":0}

        for singleCat in listCat:

            if(dfChecking["missingN"].values[i] == True):
                dictByCat["mN"] += dictCat[singleCat]
            if(dfChecking["missingA"].values[i] == True):
                dictByCat["mA"] += dictCat[singleCat]
            if(dfChecking["missingD"].values[i] == True):
                dictByCat["mD"] += dictCat[singleCat]
            if(dfChecking["missingY"].values[i] == True):
                dictByCat["mY"] += dictCat[singleCat]
            if(dfChecking["missingR"].values[i] == True):
                dictByCat["mR"] += dictCat[singleCat]
            if(dfChecking["missingC"].values[i] == True):
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
        # if i == 3:
        #     break

    dfResult = dfResult.sort_index()
    #dfResult.to_csv("tmp.csv")

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
    #print(finalRes.loc["Category 36"])
    finalRes.sort_index().to_csv("analysis_cat.csv")
        

    