#  License:		                BSD License 
#  PythonTOP default license:   license.txt

import os
import json
import numpy as np



# --------------------------------------------------------------------------
def loadJsonData(jsonFile, systemData):
    if not os.path.isfile(jsonFile):
        return False, "File does not exist: " + str(jsonFile) 
    json_data = None
    with open(jsonFile, 'r') as infile:
        json_data = json.load(infile)
    try:
       if json_data["TOP-Version"] == "WS17/18_v01":
           pass
       else:
           return False, "File was created with incompatible TOP-Version: " + str(json_data["TOP-Version"])
    except Exception as ex:
       return False, "File is not a TOP input file: " + str(jsonFile)
    if "Nodes" in json_data:
        systemData.Nodes = np.array(json_data["Nodes"])
    if "Elements" in json_data:
        systemData.Elements = np.array(json_data["Elements"])
    if "Bc_list" in json_data:
        systemData.Bc_list = json_data["Bc_list"]
    if "NodalF" in json_data:
        systemData.NodalF = np.array(json_data["NodalF"])
    if "E" in json_data:
        systemData.E = json_data["E"]
    if "thickness" in json_data:
        systemData.thickness = json_data["thickness"]
    if "prxy" in json_data:
        systemData.prxy = json_data["prxy"]
    if "elem_type" in json_data:
        systemData.elem_type = json_data["elem_type"]
    return True, ""

# --------------------------------------------------------------------------
def dumpJsonData(jsonFile, systemData):
    with open(jsonFile, 'w') as outfile:
        data = {}
        data["TOP-Version"] = "WS17/18_v01"
        if not systemData.Nodes is None:
            data["Nodes"] = systemData.Nodes.tolist()
        if not systemData.Elements is None:
            data["Elements"] = systemData.Elements.tolist()
        if not systemData.Bc_list is None:
            data["Bc_list"] = systemData.Bc_list
        if not systemData.NodalF is None:
            data["NodalF"] = systemData.NodalF.tolist()
        data["E"] = systemData.E
        data["thickness"] = systemData.thickness
        data["prxy"] = systemData.prxy
        if not systemData.elem_type is None:
            data["elem_type"] = systemData.elem_type
        json.dump(data, outfile, indent=4, sort_keys=True)