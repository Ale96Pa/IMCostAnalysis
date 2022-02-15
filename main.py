from inspect import trace
import pandas as pd
import detectError
from itertools import groupby
import operator

# Format of matching:
# L: log move (L)
# M: model move (M-REAL)
# S: sync move (L/M)
def format_trace(stringMatch):
    return stringMatch.replace("L/M","S").replace("M-REAL","M").replace("[","").replace("]",";").split("|")


def foo():
    df = pd.read_csv('conformanceChecking.csv', usecols=['Match'])
    data_list = df.values.tolist()
    #print(data_list[575])
    a = format_trace(data_list[739][0])
    print(a)
    detectError.detectMissingInTrace(a)
    detectError.detectMultipleInTrace(a)
    detectError.detectMismatchingInTrace(a)

def categorizeIncidents():
    dfTrace = pd.read_csv('conformanceChecking.csv', usecols=['Case IDs'])
    dfIncident = pd.read_csv('incident_event_log.csv', usecols=['number','category']).drop_duplicates()

    traceList = dfTrace.values.tolist()
    #print(traceList)
    #print(dfIncident)

    #print(traceList[80][0])
    a = format_trace(traceList[80][0])
    #print(a)
    allCat = []
    for elem in a:
        cat = dfIncident.loc[dfIncident["number"] == elem]
        #print(cat["category"].values)
        allCat.append(cat["category"].values.tolist())

    flat_list = [item for sublist in allCat for item in sublist]

    groupedCat = {value: len(list(freq)) for value, freq in groupby(sorted(flat_list))}
    sorted_d = dict( sorted(groupedCat.items(), key=operator.itemgetter(1),reverse=True))

    print(sorted_d)



if __name__ == '__main__':
    foo()
    #categorizeIncidents()