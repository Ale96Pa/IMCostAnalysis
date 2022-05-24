from turtle import color
import numpy as np
import matplotlib.pyplot as plt

c = {"neutral": 'lightskyblue', "miss": 'tab:blue', "rep": 'tab:orange', "mism": 'tab:green',
"n": "dodgerblue", "a":"orange","w":"forestgreen","d":"darkmagenta","f":"darkgrey","r":"gold","c":"brown",
"none":"lime","low":"green","medium":"gold","high":"darkorange","critical":"crimson"}

def barChartFitness(databar):
    incs_x = list(databar.keys())
    fit_y = list(databar.values())
    
    plt.figure(figsize = (20, 5))
    plt.grid(axis="y", linewidth = 0.5)

    plt.bar(incs_x, fit_y, color = c["neutral"], width = 0.6)
    
    plt.xlabel("Incidents IDs")
    plt.xticks(color='w')

    plt.ylabel("Fitness")
    plt.yticks(np.arange(0, 1.1, step=0.1))
    
    plt.title("Fitness distribution")
    plt.show()

def boxPlotFitness(fitnessValues):
    plt.figure(figsize = (5, 5))

    bp = plt.boxplot(fitnessValues, patch_artist=True)
    for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bp[element], color="black")
    for patch in bp['boxes']:
        patch.set(facecolor=c["neutral"])
    
    plt.grid(axis="y", linewidth = 0.5)

    plt.xlabel("Fitness")
    plt.xticks(color='w')

    plt.yticks(np.arange(0, 1.1, step=0.1))

    plt.title("Fitness distribution")
    plt.show()

def barChartCost(dfCost):
    labels = ['None' if v is None else v for v in dfCost['incident'].tolist()]
    miss =  dfCost['miss'].tolist()
    rep = dfCost['rep'].tolist()
    mism = dfCost['mism'].tolist()

    width = 0.6

    plt.figure(figsize = (20, 5))
    plt.grid(axis="y", linewidth = 0.5)

    plt.bar(labels, miss, width, label='Missing', color=c["miss"])
    plt.bar(labels, rep, width, label='Repetition', color=c["rep"])
    plt.bar(labels, mism, width, label='Mismatch', color=c["mism"])

    plt.xlabel("Incidents IDs")
    plt.xticks(color='w')

    plt.ylabel("Cost")
    plt.yticks(np.arange(0, 1.1, step=0.1))

    plt.legend()

    plt.title("Cost distribution")
    plt.show()

def boxPlotCost(dataCost):
    plt.figure(figsize = (5, 5))

    bp = plt.boxplot(dataCost.values(), patch_artist=True)
    for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bp[element], color="black")
    i=0
    for patch in bp['boxes']:
        if i==0:
            patch.set(facecolor=c["miss"])
        elif i==1:
            patch.set(facecolor=c["rep"])
        else:
            patch.set(facecolor=c["mism"])
        i+=1

    plt.grid(axis="y", linewidth = 0.5)

    plt.xticks([1,2,3], labels=dataCost.keys())

    plt.yticks(np.arange(0, 1.1, step=0.1))

    plt.title("Cost distribution")
    plt.show()


def barChartErrors(databar, error):
    activities = list(databar.keys())
    value = list(databar.values())
    
    if(error == "missing"):
        listColor = [c["n"],c["a"],c["d"],c["f"]]
    elif(error == "repetition"):
        listColor = [c["n"],c["a"],c["w"],c["r"],c["c"]]
    else:
        listColor = [c["n"],c["a"],c["r"],c["c"]]

    plt.figure(figsize = (10, 5))
    plt.grid(axis="y", linewidth = 0.5)

    plt.bar(activities, value, color = listColor, width = 0.6)
    for i, v in enumerate(activities):
        plt.text(v, value[i], str(value[i]))

    plt.yticks(np.arange(0, max(value)+10, step=10))
    plt.ylabel("Occurrences")
    
    plt.title("Occurrences of "+error+" error")
    plt.show()


def barChartSeverity(databar):
    sev = list(databar.keys())
    val = list(databar.values())

    plt.figure(figsize = (10, 5))
    plt.grid(axis="y", linewidth = 0.5)

    plt.bar(sev, val, color = [c["none"],c["low"],c["medium"],c["high"],c["critical"]], width = 0.6)
    for i, v in enumerate(sev):
        plt.text(v, val[i], str(val[i]))

    plt.yticks(np.arange(0, max(val)+10, step=10))
    plt.ylabel("Number of incidents")
    
    plt.title("Error priority")
    plt.show()

def scatterSeverity(data, severity):
    missing = []
    repetition = []
    mismatch = []
    for elem in data.keys():
        missing.append(data[elem]["totMissing"])
        repetition.append(data[elem]["totRepetition"])
        mismatch.append(data[elem]["totMismatch"])
    r = list(range(1,len(data.keys())+1))
    maxVal = max(max(missing, default=0), max(repetition, default=0), max(mismatch, default=0))

    plt.figure(figsize = (20, 5))
    plt.grid(axis="y", linewidth = 0.5)

    plt.scatter(r, missing, color=c["miss"])
    plt.scatter(r, repetition, color=c["rep"])
    plt.scatter(r, mismatch, color=c["mism"])

    plt.xlabel("Incidents")
    if len(r) > 40:
        step = 10
    else:
        step=1
    plt.xticks(np.arange(0, len(r)+1, step=step))

    plt.ylabel("Occurrences")
    plt.yticks(np.arange(0, maxVal+10, step=10))

    # plt.legend(['Missing', 'Repetition', "Mismatch"])
    plt.title("Breakdowns for "+severity+" errors")
    plt.show()

def barChartCatgory(dfCat):
    labels =dfCat['category'].tolist()
    miss =  dfCat['miss'].tolist()
    rep = dfCat['rep'].tolist()
    mism = dfCat['mism'].tolist()
    print(miss, rep, mism)
    maxVal = max(miss, default=0)+ max(rep, default=0)+ max(mism, default=0)

    width = 0.6

    plt.figure(figsize = (20, 10))
    plt.grid(axis="y", linewidth = 0.5)

    plt.bar(labels, miss, width, label='Missing', color=c["miss"])
    plt.bar(labels, rep, width, bottom=np.array(miss), label='Repetition', color=c["rep"])
    plt.bar(labels, mism, width, bottom=np.array(miss)+np.array(rep), label='Mismatch', color=c["mism"])

    plt.xticks(rotation=90)

    plt.ylabel("Number of errors")
    plt.yticks(np.arange(0, maxVal+10, step=10))

    plt.legend()

    plt.title("Cost distribution")
    plt.legend(['Missing', 'Repetition', "Mismatch"])
    plt.show()

def boxPlotCat(data):
    fig, ax = plt.subplots(figsize = (20, 10))
    ax.boxplot(data.values())
    plt.xticks(rotation=90)
    ax.set_xticklabels(data.keys())
    ax.set_ylim([0, 1])

    plt.show()