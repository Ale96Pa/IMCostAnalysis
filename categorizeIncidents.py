from itertools import groupby
import pandas as pd
import operator

def classifyIncErrors(dfIncident,incList):
    allCat = []
    for elem in incList:
        cat = dfIncident.loc[dfIncident["number"] == elem]
        allCat.append(cat["category"].values.tolist())
    flat_list = [item for sublist in allCat for item in sublist]

    groupedCat = {value: len(list(freq)) for value, freq in groupby(sorted(flat_list))}
    sorted_d = dict( sorted(groupedCat.items(), key=operator.itemgetter(1),reverse=True))

    return sorted_d