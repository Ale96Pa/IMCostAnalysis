from cProfile import label
import procMining as pm
import incidentData as id
import conf

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def barChartFitness(dataFitness):
    incs_x = list(dataFitness.keys())
    fit_y = list(dataFitness.values())
    
    fig = plt.figure(figsize = (20, 5))
    
    # creating the bar plot
    plt.bar(incs_x, fit_y, color ='tab:blue', width = 0.6)
    
    plt.xlabel("Incidents IDs")
    plt.xticks(color='w')

    plt.ylabel("Fitness")
    # plt.title("Students enrolled in different courses")
    plt.show()

def boxPlotFitness(fitnessValues):

    # Creating axes instance
    fig, ax = plt.subplots()

    # Creating plot
    plt.xlabel("Fitness")
    plt.xticks(color='w')
    bp = ax.boxplot(fitnessValues)
    ax.set_ylim([0, 1])

    # show plot
    plt.show()

def barChartCost(dfCost):

    labels = ['None' if v is None else v for v in dfCost['incident'].tolist()]
    miss =  dfCost['miss'].tolist()
    rep = dfCost['rep'].tolist()
    mism = dfCost['mism'].tolist()

    width = 0.6       # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots(figsize = (20, 5))

    print(len(labels), len(miss), len(rep), len(mism))

    ax.bar(labels, miss, width, label='Missing')
    ax.bar(labels, rep, width, bottom=np.array(miss), label='Repetition')
    ax.bar(labels, mism, width, bottom=np.array(miss)+np.array(rep), label='Mismatch')

    plt.xticks(color='w')
    ax.set_ylabel('Cost')
    ax.set_ylim([0, 1])
    ax.legend()
    # ax.set_title('Scores by group and gender')

    plt.show()

def boxPlotCost(dataCost):

    # Creating axes instance
    fig, ax = plt.subplots()

    # Creating plot
    # plt.xlabel("Cost")
    # plt.xticks(color='w')
    bp = ax.boxplot(dataCost.values())
    ax.set_xticklabels(dataCost.keys())
    ax.set_ylim([0, 1])

    # show plot
    plt.show()

def barChartErrors(data):
    incs_x = list(data.keys())
    fit_y = list(data.values())
    
    fig = plt.figure(figsize = (20, 5))
    
    # creating the bar plot
    plt.bar(incs_x, fit_y, color ='tab:blue', width = 0.6)
    
    # plt.xlabel("Incidents IDs")
    # plt.xticks(color='w')

    plt.ylabel("Occurrences")
    # plt.title("Students enrolled in different courses")
    plt.show()

def barChartSeverity(data):
    sev = list(data.keys())
    val = list(data.values())
    
    fig = plt.figure(figsize = (20, 5))
    
    # creating the bar plot
    plt.bar(sev, val, color ='tab:blue', width = 0.6)
    
    # plt.xlabel("Incidents IDs")
    # plt.xticks(color='w')

    plt.ylabel("Number of traces")
    
    # plt.title("Students enrolled in different courses")
    plt.show()

def scatterSeverity(data):
    missing = []
    repetition = []
    mismatch = []
    for elem in data.keys():
        missing.append(data[elem]["totMissing"])
        repetition.append(data[elem]["totRepetition"])
        mismatch.append(data[elem]["totMismatch"])
    # missing = [89, 90, 70, 89, 100, 80, 90, 100, 80, 34]
    # repetition = [30, 29, 49, 48, 100, 48, 38, 45, 20, 30]
    # mismatch = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    r = list(range(1,len(data.keys())+1))
    fig=plt.figure()

    plt.scatter(r, missing, c="r")
    plt.scatter(r, repetition, color='b')
    plt.scatter(r, mismatch, color='g')

    plt.xlabel("Traces")
    plt.ylabel("Number occurrences")

    plt.legend(['Missing', 'Repetition', "Mismatch"])

    # ax=fig.add_axes([0,0,1,1])
    # ax.scatter(range, missing, color='r')
    # ax.scatter(range, repetition, color='b')
    # ax.scatter(range, mismatch, color='g')
    # ax.set_xlabel('Traces')
    # ax.set_ylabel('Number occurrences')
    # ax.legend()
    # ax.set_title('scatter plot')
    plt.show()


def barChartCatgory(dfCat):
    # labels = ['None' if v is None else v for v in dfCat['incident'].tolist()]
    labels =dfCat['category'].tolist()
    miss =  dfCat['miss'].tolist()
    rep = dfCat['rep'].tolist()
    mism = dfCat['mism'].tolist()

    width = 0.6       # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots(figsize = (20, 10))

    print(len(labels), len(miss), len(rep), len(mism))

    ax.bar(labels, miss, width, label='Missing')
    ax.bar(labels, rep, width, bottom=np.array(miss), label='Repetition')
    ax.bar(labels, mism, width, bottom=np.array(miss)+np.array(rep), label='Mismatch')

    # plt.xticks(color='w')
    plt.xticks(rotation=90)
    ax.set_ylabel('Number of errors')
    # ax.set_ylim([0, 1])
    ax.legend()
    # ax.set_title('Scores by group and gender')

    plt.show()

def boxPlotCat(data):
    fig, ax = plt.subplots(figsize = (20, 10))
    ax.boxplot(data.values())
    plt.xticks(rotation=90)
    ax.set_xticklabels(data.keys())
    ax.set_ylim([0, 1])

    plt.show()

if __name__ == "__main__":
    aligns = pm.compute_trace_alignment(conf.fileLog, conf.fileModel)
    alignments = pm.compute_deviations(aligns, conf.dictAlfaMiss, conf.Tmiss, conf.dictAlfaMult, conf.Tmult, conf.dictAlfaMismatch, conf.Tmism, conf.dictAlfaCost)

    

    dataFitness = {}
    dataCost = []
    listMiss = []
    listRep = []
    listMism = []
    l = [[]]
    # listIncidents = listMiss = listRep = listMism = []
    cMissN=0
    cMissA=0 
    cMissR=0 
    cMissC=0 
    cMissD=0 
    cMissF=0

    cRepN=0
    cRepA=0
    cRepW=0
    cRepR=0
    cRepC=0

    cMismN=0
    cMismA=0
    cMismR=0
    cMismC=0

    dictSev = {"none":0, "low":0, "medium":0, "high":0, "critical":0}
    for elem in alignments.keys():
        # print(alignments[elem])
        dataFitness[elem] = alignments[elem]["fitness"]
        # listIncidents.append(str(elem))
        listMiss.append(alignments[elem]["costMissing"])
        listRep.append(alignments[elem]["costRepetition"])
        listMism.append(alignments[elem]["costMismatch"])
        
        cMissN += alignments[elem]["missing"]["N"]
        cMissA += alignments[elem]["missing"]["A"]
        cMissD += alignments[elem]["missing"]["D"]
        cMissF += alignments[elem]["missing"]["F"]
        cMissR += alignments[elem]["missing"]["R"]
        cMissC += alignments[elem]["missing"]["C"]

        cRepN += alignments[elem]["repetition"]["N"]
        cRepA += alignments[elem]["repetition"]["A"]
        cRepW += alignments[elem]["repetition"]["W"]
        cRepR += alignments[elem]["repetition"]["R"]
        cRepC += alignments[elem]["repetition"]["C"]

        cMismN += alignments[elem]["mismatch"]["N"]
        cMismA += alignments[elem]["mismatch"]["A"]
        cMismR += alignments[elem]["mismatch"]["R"]
        cMismC += alignments[elem]["mismatch"]["C"]

        dictSev[alignments[elem]["severity"]] +=  1

        l.append([elem,  alignments[elem]["fitness"], alignments[elem]["costMissing"], alignments[elem]["costRepetition"], alignments[elem]["costMismatch"]])
    
    # print(cMissN, cMissA,cMissR,cMissC,cMissD,cMissF)
    # print(cRepN,cRepA,cRepW,cRepR,cRepC)
    # print(cMismN,cMismA,cMismR,cMismC)

    # print(dictSev)


    dataFitness = dict(sorted(dataFitness.items(), key=lambda item: item[1], reverse=True))
    dfCost = pd.DataFrame(l, columns =['incident', 'fitness', "miss", "rep", "mism"])
    dfCost = dfCost.sort_values(by='fitness', ascending=False)


    # barChartFitness(dataFitness)
    # boxPlotFitness(list(dataFitness.values()))
    # barChartCost(dfCost)
    # boxPlotCost({"Missing": listMiss, "Repetition": listRep, "Mismatch": listMism})

    # barChartErrors({"Detection": cMissN, "Activation":cMissA, "Double Check":cMissD, "Notification":cMissF, "Resolution":cMissR, "Closure":cMissC})
    # barChartErrors({"Detection": cRepN, "Activation":cRepA, "Awaiting":cRepW, "Resolution":cRepR, "Closure":cRepC})
    # barChartErrors({"Detection": cMismN, "Activation":cMismA, "Resolution":cMismR, "Closure":cMismC})

    # barChartSeverity(dictSev)

    # print(len(alignments))
    dictNone = {k: v for k, v in alignments.items() if v["severity"] == "none"}
    dictLow = {k: v for k, v in alignments.items() if v["severity"] == "low"}
    dictMedium = {k: v for k, v in alignments.items() if v["severity"] == "medium"}
    dictHigh = {k: v for k, v in alignments.items() if v["severity"] == "high"}
    dictCritical = {k: v for k, v in alignments.items() if v["severity"] == "critical"}
    # print(len(dictLow), len(dictNone), len(dictCritical), len(dictMedium), len(dictHigh))
    # scatterSeverity(dictNone)
    # scatterSeverity(dictLow)
    # scatterSeverity(dictMedium)
    # scatterSeverity(dictHigh)
    # scatterSeverity(dictCritical)

    incByCat = id.formatIncidents(conf.fileLog)
    catCount = []
    boxDataFit = {}
    boxDataCost = {}
    for cat in incByCat.keys():
        incidents = incByCat[cat]
        currCatCount = {"category":"","tot":0,"miss":0,"rep":0,"mism":0}
        listFitness = []
        listCost = []
        for inc in incidents:
            # print(alignments[inc])
            currCatCount["miss"] += alignments[inc]["totMissing"]
            currCatCount["rep"] += alignments[inc]["totRepetition"]
            currCatCount["mism"] += alignments[inc]["totMismatch"]
            listFitness.append(alignments[inc]["fitness"])
            listCost.append(alignments[inc]["costTotal"])

        currCatCount["tot"] = currCatCount["miss"]+currCatCount["rep"]+currCatCount["mism"]
        currCatCount["category"] = cat
        catCount.append(currCatCount)

        boxDataFit[cat] = listFitness
        boxDataCost[cat] = listCost

    catCount = sorted(catCount, key=lambda d: d['tot'], reverse=True) 
    # print(catCount)

    dfCat = pd.DataFrame(catCount)
    # barChartCatgory(dfCat)

    # print(boxDataFit)
    sortCatFit = sorted(boxDataFit, key=lambda k: sum(boxDataFit[k]) / len(boxDataFit[k]), reverse=True)
    # print(boxDataFit)
    newDFit = {}
    newDCost = {}
    for e in sortCatFit:
        newDFit[e] = boxDataFit[e]
        newDCost[e] = boxDataCost[e]
    boxPlotCat(newDFit)
    boxPlotCat(newDCost)
