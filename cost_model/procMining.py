import pandas as pd
import pm4py
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments

import cost_model.devDetection as dd
import cost_model.costModel as cm
import utils.utilsPM as upm


"""
This function gets event log from csv file
"""
def getCsvLog(inputFile):
    log_csv = pd.read_csv(inputFile, sep=';')
    log_csv = pm4py.format_dataframe(log_csv, case_id='incident_id', activity_key='event', timestamp_key='timestamp')
    log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
    event_log = log_converter.apply(log_csv)
    return event_log

"""
The function format the results of the trace alignment into a dataframe containing:
List of incidents, Alignment trace structure, Trace Fitness
"""
def compute_trace_alignment(inputFile, modelFile):
    resAlignments = []

    log = getCsvLog(inputFile)
    model_net, initial_marking, final_marking = pnml_importer.apply(modelFile)
    aligned_traces = alignments.apply_log(log, model_net, initial_marking, final_marking)

    i=0
    for trace in aligned_traces:
        traceFormat = ""
        for events in trace["alignment"]:
            if events[0] == events[1]:
                traceFormat+="[S]"+events[0]
            elif events[0] == ">>":
                traceFormat+="[M]"+events[1]
            elif events[1] == ">>":
                traceFormat+="[L]"+events[0]
            traceFormat+=";"

        resAlignments.append({
            "incident_id": log[i].__getitem__(0)["incident_id"],
            "alignment": traceFormat,
            "fitness": trace["fitness"]
        })
        i+=1
    return resAlignments

"""
This function computes the deviation on the alignments and collect data about error categories
of missing, repetition and mismatch
"""
def compute_deviations(traces, dictAlfaMiss, Tmiss, dictAlfaMult, Tmult, dictAlfaMismatch, Tmism, dictAlfaCost):
    deviationsDict = {}
    for elem in traces:
        trace = upm.convertTraceList(elem["alignment"])
        resMissing = dd.detectMissing(trace)
        resRepetition = dd.detectMutliple(trace)
        resMismatch = dd.detectMismatch(trace)

        numEvents = upm.countEvents(trace)
        costMissing = cm.calculateMissing(upm.addAllActivities(resMissing),dictAlfaMiss, Tmiss)
        costRepetition = cm.calculateMultiple(upm.addAllActivities(resRepetition), numEvents, dictAlfaMult, Tmult)
        costMismatch = cm.calculateMismatch(upm.addAllActivities(resMismatch), numEvents, dictAlfaMismatch, Tmism)
        cost = cm.calculateCost(costMissing,costRepetition,costMismatch, dictAlfaCost)

        deviationsDict[elem["incident_id"]] = {
            "alignment": elem["alignment"],
            "fitness": elem["fitness"],
            "missing": resMissing,
            "repetition": resRepetition,
            "mismatch": resMismatch,
            "totMissing": sum(resMissing.values()),
            "totRepetition": sum(resRepetition.values()),
            "totMismatch": sum(resMismatch.values()),
            "costMissing": costMissing,
            "costRepetition": costRepetition,
            "costMismatch": costMismatch,
            "costTotal": cost,
            "severity": cm.calculateSeverity(cost)
        }

    return deviationsDict