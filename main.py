import pandas as pd
import detectError
import categorizeIncidents
import ast

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
        dfMiss = detectError.detectMissingInTrace(trace)
        dfMult = detectError.detectMultipleInTrace(trace)
        dfMism = detectError.detectMismatchingInTrace(trace)

        filterCheck = pd.DataFrame.from_dict(dfChecking.iloc[i].to_dict(), orient='index').transpose()
        errors = pd.concat([filterCheck, dfMiss, dfMult, dfMism], axis=1)

        categories = categorizeIncidents.classifyInc(dfIncident,format_trace(incList[i]))
        dfCategories = pd.DataFrame.from_dict({"Categories": str(categories)}, orient='index').transpose()

        fullRow = pd.concat([errors, dfCategories], axis=1)
        dfResult = dfResult.append(fullRow)


        if i == 3:
            break
    # print(dfResult)
    dfResult.to_csv("result.csv")
