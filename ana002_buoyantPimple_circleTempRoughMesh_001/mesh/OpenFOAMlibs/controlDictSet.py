from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
import os
from os import path
import glob
import shutil

def patchList_otherWall(patch_list):
    outputPatch_list = []
    for patchName in patch_list:
        if len(patchName.split('_'))>=3 and patchName.split('_')[1] != 'wall':
            outputPatch_list.append(patchName)
    print(outputPatch_list)
    return outputPatch_list


def setting_ControlDict(outputPatch_list):
    PWD = os.getcwd()
    control_dict = ParsedParameterFile(path.join(PWD, "system", 'controlDict'))

    for i, pathName in enumerate(outputPatch_list):
        if i == 0:
            control_dict['functions']['inletFlux']['name'] = pathName
            control_dict['functions'][pathName] = control_dict['functions']['inletFlux']
            del control_dict['functions']['inletFlux']
            control_dict.writeFile()
        else:
            control_dict['functions'][pathName] = {
                                                        f'${outputPatch_list[0]}' : '',
                                                        'name' : outputPatch_list[i]
                                                    }
            control_dict.writeFile()
