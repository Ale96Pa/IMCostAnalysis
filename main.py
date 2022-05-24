import conf
import pandas as pd

import cost_model.procMining as pm
import cost_model.incidentData as id
import analysis_charts.charts as charts

def plotErrorAssessment(alignments):
    # Data for fitness and error assessment
    dataFitness = {}
    dataCost = [[]]
    listMiss = []
    listRep = []
    listMism = []

    # Data for error priority assessment
    counterMiss = {"Detection":0, "Activation":0,"Double-Check":0, "Notification":0, "Resolution":0, "Closure":0}
    counterRep = {"Detection":0, "Activation":0,"Awaiting":0, "Resolution":0, "Closure":0}
    counterMism = {"Detection":0, "Activation":0, "Resolution":0, "Closure":0}
    dictSev = {"none":0, "low":0, "medium":0, "high":0, "critical":0}

    for elem in alignments.keys():
        dataFitness[elem] = alignments[elem]["fitness"]
        listMiss.append(alignments[elem]["costMissing"])
        listRep.append(alignments[elem]["costRepetition"])
        listMism.append(alignments[elem]["costMismatch"])
        
        counterMiss["Detection"] += alignments[elem]["missing"]["N"]
        counterMiss["Activation"] += alignments[elem]["missing"]["A"]
        counterMiss["Double-Check"] += alignments[elem]["missing"]["D"]
        counterMiss["Notification"] += alignments[elem]["missing"]["F"]
        counterMiss["Resolution"] += alignments[elem]["missing"]["R"]
        counterMiss["Closure"] += alignments[elem]["missing"]["C"]

        counterRep["Detection"] += alignments[elem]["repetition"]["N"]
        counterRep["Activation"] += alignments[elem]["repetition"]["A"]
        counterRep["Awaiting"] += alignments[elem]["repetition"]["W"]
        counterRep["Resolution"] += alignments[elem]["repetition"]["R"]
        counterRep["Closure"] += alignments[elem]["repetition"]["C"]

        counterMism["Detection"] += alignments[elem]["mismatch"]["N"]
        counterMism["Activation"] += alignments[elem]["mismatch"]["A"]
        counterMism["Resolution"] += alignments[elem]["mismatch"]["R"]
        counterMism["Closure"] += alignments[elem]["mismatch"]["C"]

        dictSev[alignments[elem]["severity"]] +=  1

        dataCost.append([elem,  alignments[elem]["fitness"], alignments[elem]["costMissing"], alignments[elem]["costRepetition"], alignments[elem]["costMismatch"]])
    

    dataFitness = dict(sorted(dataFitness.items(), key=lambda item: item[1], reverse=True))
    dfCost = pd.DataFrame(dataCost, columns =['incident', 'fitness', "miss", "rep", "mism"])
    dfCost = dfCost.sort_values(by='fitness', ascending=False)

    return dataFitness, dfCost, {"Missing": listMiss, "Repetition": listRep, "Mismatch": listMism}, \
    {"Missing":counterMiss, "Repetition": counterRep, "Mismatch":counterMism}, dictSev


def plotIncidentAssessment(alignments, incByCat):
    # Data for incident analysis
    categoryCount = []
    boxDataFitness = {}
    boxDataCost = {}

    for cat in incByCat.keys():
        incidents = incByCat[cat]
        currCatCount = {"category":"","tot":0,"miss":0,"rep":0,"mism":0}
        listFitness = []
        listCost = []
        for inc in incidents:
            currCatCount["miss"] += alignments[inc]["totMissing"]
            currCatCount["rep"] += alignments[inc]["totRepetition"]
            currCatCount["mism"] += alignments[inc]["totMismatch"]
            listFitness.append(alignments[inc]["fitness"])
            listCost.append(alignments[inc]["costTotal"])

        currCatCount["tot"] = currCatCount["miss"]+currCatCount["rep"]+currCatCount["mism"]
        currCatCount["category"] = cat
        categoryCount.append(currCatCount)

        boxDataFitness[cat] = listFitness
        boxDataCost[cat] = listCost

    categoryCount = sorted(categoryCount, key=lambda d: d['tot'], reverse=True) 
    dfCategory = pd.DataFrame(categoryCount)

    sortCatFit = sorted(boxDataFitness, key=lambda k: sum(boxDataFitness[k]) / len(boxDataFitness[k]), reverse=True)
    boxDataFitnessSort = {}
    boxDataCostSort = {}
    for e in sortCatFit:
        boxDataFitnessSort[e] = boxDataFitness[e]
        boxDataCostSort[e] = boxDataCost[e]

    return dfCategory, boxDataFitnessSort, boxDataCostSort

if __name__ == "__main__":
    aligns = pm.compute_trace_alignment(conf.fileLog, conf.fileModel)
    alignments = pm.compute_deviations(aligns, conf.dictAlfaMiss, conf.Tmiss, conf.dictAlfaMult, conf.Tmult, conf.dictAlfaMismatch, conf.Tmism, conf.dictAlfaCost)
    incByCat = id.formatIncidents(conf.fileLog)

    dataFitness, dfCost, dictError, counterError, dictSev = plotErrorAssessment(alignments)
    dfCategory, boxDataFitness, boxDataCost = plotIncidentAssessment(alignments, incByCat)

    # Plot charts for fitness and cost assessment
    charts.barChartFitness(dataFitness)
    charts.boxPlotFitness(list(dataFitness.values()))

    charts.barChartCost(dfCost)
    charts.boxPlotCost(dictError)


    # Plot charts for errors assessment
    charts.barChartErrors(counterError["Missing"], "missing")
    charts.barChartErrors(counterError["Repetition"], "repetition")
    charts.barChartErrors(counterError["Mismatch"], "mismatch")


    # Plot charts for error priority assessment
    charts.barChartSeverity(dictSev)

    dictNone = {k: v for k, v in alignments.items() if v["severity"] == "none"}
    charts.scatterSeverity(dictNone, "None")
    dictLow = {k: v for k, v in alignments.items() if v["severity"] == "low"}
    charts.scatterSeverity(dictLow, "Low")
    dictMedium = {k: v for k, v in alignments.items() if v["severity"] == "medium"}
    charts.scatterSeverity(dictMedium, "Medium")
    dictHigh = {k: v for k, v in alignments.items() if v["severity"] == "high"}
    charts.scatterSeverity(dictHigh, "High")
    dictCritical = {k: v for k, v in alignments.items() if v["severity"] == "critical"}
    charts.scatterSeverity(dictCritical, "Critical")


    # Plot charts for assessment of incident categories
    charts.barChartCatgory(dfCategory)

    # charts.boxPlotCat(boxDataFitness)
    # charts.boxPlotCat(boxDataCost)
