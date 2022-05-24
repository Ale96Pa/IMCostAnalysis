import csv
import pandas as pd
from collections import defaultdict

"""
This function format data by incident ID
"""
def formatIncidents(inputFile):
    df = pd.read_csv(inputFile, delimiter=";")

    res = []
    line_count = 0
    for i, row in df.iterrows():
        if line_count != 0:
            # res.append({"incident_id": row[0], "impact":row[20], "urgency":row[21], "priority":row[22], "category":row[16], "openTs":row[10], "closeTs":row[35],
            # "reassignment":row[4], "reopen":row[5], "updates": row[6]})
            # res.append({"incident_id": row[0], "impact":row[26], "urgency":row[27], "priority":row[28], "category":row[16], "openTs":row[10], "closeTs":row[35],
            # "reassignment":row[4], "reopen":row[5], "updates": row[6]})
            res.append({"incident_id": row["incident_id"], "impact":row["impact"], "urgency":row["urgency"], "priority":row["priority"], "category":row["category"]})
        # else:
        #     print(row)
        #     for i in range(0,len(row)):
        #         print(row[i]+"--"+str(i))
        line_count+=1
    result = list({i['incident_id']:i for i in res}.values())

    # res = []
    # with open(inputFile) as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=';')
    #     line_count = 0
    #     for row in csv_reader:
    #         if line_count != 0:
    #             # res.append({"incident_id": row[0], "impact":row[20], "urgency":row[21], "priority":row[22], "category":row[16], "openTs":row[10], "closeTs":row[35],
    #             # "reassignment":row[4], "reopen":row[5], "updates": row[6]})
    #             res.append({"incident_id": row[0], "impact":row[26], "urgency":row[27], "priority":row[28], "category":row[16], "openTs":row[10], "closeTs":row[35],
    #             "reassignment":row[4], "reopen":row[5], "updates": row[6]})
    #         else:
    #             print(row)
    #             for i in range(0,len(row)):
    #                 print(row[i]+"--"+str(i))
    #         line_count+=1
    # result = list({i['incident_id']:i for i in res}.values())

    incByCat = {}
    for item in result:
        incByCat.setdefault(item['category'], []).append(item["incident_id"])
    
    return incByCat

    # return result
