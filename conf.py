fileLog = "data/dummy_log.csv"
fileModel = "data/base_model.pnml"

listBaseActivities = ["N","A", "D", "F", "W", "R","C"]

dictAlfaMiss = {"N":0.25,"A":0.25, "D":0.2, "F":0.2, "W":0, "R":0.1,"C":0.1}
Tmiss = 1
dictAlfaMult = {"N":0.25,"A":0.25,"W":0.2,"R":0.2,"C":0.1}
Tmult = 10
dictAlfaMismatch = {"N":0.35,"A":0.35,"W":0.1,"R":0.1,"C":0.1}
Tmism = 4
dictAlfaCost = {"miss":0.33,"rep":0.34,"mism":0.33}

threshold = {"low":0.37,"medium":0.69,"high":0.89}