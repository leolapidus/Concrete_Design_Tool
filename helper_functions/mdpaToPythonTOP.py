## this script reades a mdpa file and translates it into a PythonTOP json input file
import glob
import sys
import os
import json_tools
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'FE_code')))
import systemData


if len(sys.argv) != 2:
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    raise ValueError("Wrong number of many arguments")
print ('Argument List:', str(sys.argv))

mdpaFile = sys.argv[1]
if not mdpaFile.endswith(".mdpa"):
    raise ValueError("Need .mdpa file as argument")

jsonSystemDataFile = mdpaFile.replace(".mdpa", ".json")

systemData = systemData.SystemData()

# nodes
# open mdpa to read
with open(mdpaFile, 'r') as mf:

    tmpNodes = []

    inNodes = False
    for line in iter(mf):
        if line.startswith("Begin Nodes"):
            inNodes = True
            continue

        if line.startswith("End Nodes"):
            inNodes = False
            continue

        if inNodes:
            entriesList = line.split()
            if int(entriesList[0]) != len(tmpNodes)+1:
                raise RuntimeError("Nodes are have to be numbered in ascending order starting from 1!")
            if float(entriesList[3]) != 0.0:
                raise RuntimeError("Model is not plane! z-coordinate needs to be 0.0!")
            tmpNodes.append( [len(tmpNodes)+1, float(entriesList[1]), float(entriesList[2])] )

    systemData.Nodes = np.array(tmpNodes)

# elements
# open mdpa to read
with open(mdpaFile, 'r') as mf:

    tmpElements = []

    inElements = False

    for line in iter(mf):
        if line.startswith("Begin Elements"):
            inElements = True
            continue

        if line.startswith("End Elements"):
            inElements = False
            continue

        if inElements:
            entriesList = line.split()

            if len(entriesList) != 6:
                raise RuntimeError("Element does not have 4 nodes: \n" + line)
            tmpElements.append([len(tmpElements)+1, int(entriesList[2]), int(entriesList[3]), int(entriesList[4]), int(entriesList[5]), 1])

    systemData.Elements = np.array(tmpElements)

json_tools.dumpJsonData(jsonSystemDataFile,systemData)

print (" FINISHED CONVERSION FROM:")
print (mdpaFile)
print ("TO:")
print (jsonSystemDataFile)
