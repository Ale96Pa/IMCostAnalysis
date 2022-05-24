import pandas as pd

"""
This function format data by incident ID
"""
def formatIncidents(inputFile):
    df = pd.read_csv(inputFile, delimiter=";")
    res = []
    
    line_count = 0
    for i, row in df.iterrows():
        if line_count != 0:
            res.append({"incident_id": row["incident_id"], "impact":row["impact"], "urgency":row["urgency"], "priority":row["priority"], "category":row["category"]})
        line_count+=1
    result = list({i['incident_id']:i for i in res}.values())

    incByCat = {}
    for item in result:
        incByCat.setdefault(item['category'], []).append(item["incident_id"])
    
    return incByCat