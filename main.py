import procMining as pm
import incidentData as id
import conf

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



if __name__ == "__main__":
    aligns = pm.compute_trace_alignment(conf.fileLog, conf.fileModel)
    alignments = pm.compute_deviations(aligns, conf.dictAlfaMiss, conf.Tmiss, conf.dictAlfaMult, conf.Tmult, conf.dictAlfaMismatch, conf.Tmism, conf.dictAlfaCost)

    incidents = id.formatIncidents(conf.fileLog)

    dataFitness = {}
    for elem in alignments.keys():
        dataFitness[elem] = alignments[elem]["fitness"]
    dataFitness = dict(sorted(dataFitness.items(), key=lambda item: item[1], reverse=True))

    # barChartFitness(dataFitness)
    boxPlotFitness(list(dataFitness.values()))

    