import pandas as pd
import detectError
import categorizeIncidents
import costModel

# Params
isEnriched = True
dictAlfaMiss = {"aN":0.25,"aA":0.25,"aK":0.1,"aD":0.1,"aY":0.1,"aR":0.1,"aC":0.1}
Tmiss = 4 #1 per simple, 4 per enriched
dictAlfaMult = {"aN":0.25,"aA":0.25,"aW":0.2,"aG":0.1,"aR":0.1,"aC":0.1}
Tmult = 10
dictAlfaMismatch = {"aN":0.5,"aR":0.5}
Tmism = 4
dictAlfaCost = {"miss":0.33,"mult":0.34,"mism":0.33}

def format_trace(stringMatch):
    return stringMatch.replace("L/M","S").replace("M-REAL","M").replace("[","").replace("]",";").split("|")

def mapResult(inputFile, outputFile, incidentLogFile):
    dfChecking = pd.read_csv(inputFile, delimiter=";", usecols=['Case IDs','NumOfCases','Trace Fitness','Match'])
    dfIncident = pd.read_csv(incidentLogFile, usecols=['number','category']).drop_duplicates()
    dfResult = pd.DataFrame()

    matchList = dfChecking["Match"].values.tolist()
    incList = dfChecking["Case IDs"].values.tolist()

    for i in range(0,len(matchList)-1):
        trace = format_trace(matchList[i])
        numEv = len(trace)
        dfMiss = detectError.detectMissingInTrace(trace, isEnriched)
        dfMult = detectError.detectMultipleInTrace(trace)
        dfMism = detectError.detectMismatchingInTrace(trace)

        costMiss = costModel.calculateMissing(dfMiss, dictAlfaMiss, Tmiss)
        dfCostMiss = pd.DataFrame.from_dict(costMiss, orient='index').transpose()
        costMult = costModel.calculateMultiple(dfMult, numEv, dictAlfaMult, Tmult)
        dfCostMult = pd.DataFrame.from_dict(costMult, orient='index').transpose()
        costMism = costModel.calculateMismatch(dfMism, numEv, dictAlfaMismatch, Tmism)
        dfCostMism = pd.DataFrame.from_dict(costMism, orient='index').transpose()
        costTot = dictAlfaCost["miss"]*costMiss["costMissing"]+ dictAlfaCost["mult"]*costMult["costMultiple"]+ dictAlfaCost["mism"]*costMism["costMismatch"]
        dfCostTot = pd.DataFrame.from_dict({"cost": costTot}, orient='index').transpose()
        
        filterCheck = pd.DataFrame.from_dict(dfChecking.iloc[i].to_dict(), orient='index').transpose()
        errors = pd.concat([filterCheck, dfMiss, dfMult, dfMism, dfCostMiss, dfCostMult, dfCostMism, dfCostTot], axis=1)

        categories = categorizeIncidents.classifyInc(dfIncident,format_trace(incList[i]))
        dfCategories = pd.DataFrame.from_dict({"Categories": str(categories)}, orient='index').transpose()

        fullRow = pd.concat([errors, dfCategories], axis=1)
        dfResult = dfResult.append(fullRow)

        # if i == 0:
        #     break
    dfResult.to_csv(outputFile)

if __name__ == '__main__':
    inputFile=outputFile=""
    incidentLogFile="incident_log.csv"
    if isEnriched:
        inputFile = "enriched-checking.csv"
        outputFile = "result/enrichedResult-na.csv"
    else:
        inputFile = "simple-checking.csv"
        outputFile = "result/simpleResult-na.csv"
        
    mapResult(inputFile, outputFile, incidentLogFile)