### Approach for Enhancing Incident Management Process Assessment Through a Process Mining Based Approach

## Description
This program is a proof of concept for an automated approach to perform Incident Management (IM) process accessment leveraging Trace Alignment. In particular, this program performs the analysis of *fitness* as it derives by alignment, *cost* analysis describing the errors causing deviation from the target model, *detailed assessment* of the specific events causing errors, and *incident analysis* basing on their type (i.e., incident categories and affected services).

## Installation requirement
The following libraries are required for the correct execution:
- pip install pm4py
- pip install matplotlib
- pip install numpy
- pip install pandas

## Configuration
If you want to just reproduce a simplified version of the proof-of-concept, follow the installation instructions.

If you want customize your assessment, the following configurations are settable in the file *conf.py*:
- input IM log file: put the file (in format csv) in the folder named "data" and set the filename in the conf.py (fileLog parameter)
- input target model file: put the file (in format .pnml) in the folder named "data" and set the filename in the conf.py (fileModel parameter)
- set the parameters of the cost model with the following notation: N=detection,A=activation,W=awaiting,D=double-check,F=notification,R=resolution,C=closure
- set the weight of missing, repetition and mismatch errors, and the severity thresholds

## Installation
Download this github repositiory, set the configuration (if any) and run the command from your terminal:

$ python -u "<path_to_this_folder>\main.py"