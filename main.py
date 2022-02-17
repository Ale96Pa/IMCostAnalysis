import pandas as pd
import detectError
import categorizeIncidents
import costModel

# Format of matching:
# L: log move (L)
# M: model move (M-REAL)
# S: sync move (L/M)
def format_trace(stringMatch):
    return stringMatch.replace("L/M","S").replace("M-REAL","M").replace("[","").replace("]",";").split("|")

if __name__ == '__main__':
    dfChecking = pd.read_csv('conformanceChecking.csv', usecols=['Case IDs','NumOfCases','Trace Fitness','Match'])
    dfIncident = pd.read_csv('incident_event_log.csv', usecols=['number','category']).drop_duplicates()
    dfResult = pd.DataFrame()

    matchList = dfChecking["Match"].values.tolist()
    incList = dfChecking["Case IDs"].values.tolist()

    for i in range(0,len(matchList)-1):
        trace = format_trace(matchList[i])
        numEv = len(trace)
        dfMiss = detectError.detectMissingInTrace(trace)
        dfMult = detectError.detectMultipleInTrace(trace)
        dfMism = detectError.detectMismatchingInTrace(trace)

        costMiss = costModel.calculateMissing(dfMiss)
        dfCostMiss = pd.DataFrame.from_dict(costMiss, orient='index').transpose()
        costMult = costModel.calculateMultiple(dfMult, numEv)
        dfCostMult = pd.DataFrame.from_dict(costMult, orient='index').transpose()
        costMism = costModel.calculateMismatch(dfMism, numEv)
        dfCostMism = pd.DataFrame.from_dict(costMism, orient='index').transpose()
        costTot = costMiss["costMissing"]+costMult["costMultiple"]+costMism["costMismatch"]
        dfCostTot = pd.DataFrame.from_dict({"cost": costTot}, orient='index').transpose()
        
        filterCheck = pd.DataFrame.from_dict(dfChecking.iloc[i].to_dict(), orient='index').transpose()
        errors = pd.concat([filterCheck, dfMiss, dfMult, dfMism, dfCostMiss, dfCostMult, dfCostMism, dfCostTot], axis=1)

        categories = categorizeIncidents.classifyInc(dfIncident,format_trace(incList[i]))
        dfCategories = pd.DataFrame.from_dict({"Categories": str(categories)}, orient='index').transpose()

        fullRow = pd.concat([errors, dfCategories], axis=1)
        dfResult = dfResult.append(fullRow)

        # if i == 3:
        #     break
    # print(dfResult)
    dfResult.to_csv("result.csv")
