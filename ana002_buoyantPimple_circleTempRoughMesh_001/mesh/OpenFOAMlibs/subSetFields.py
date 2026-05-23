import glob
import os
import shutil
import subprocess
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from os import path


def setting_setField():
    PWD = os.getcwd() #現在のディレクトリパス
    setFieldsParsedParameterFile = ParsedParameterFile(path.join(PWD, "system", 'setFieldsDict'))

    return setFieldsParsedParameterFile

def setFields_set_fuc(file_, setFields_dic):
    minX = setFields_dic['boxToCell']['regions'][0]
    minY = setFields_dic['boxToCell']['regions'][1]
    minZ = setFields_dic['boxToCell']['regions'][2]
    maxX = setFields_dic['boxToCell']['regions'][3]
    maxY = setFields_dic['boxToCell']['regions'][4]
    maxZ = setFields_dic['boxToCell']['regions'][5]
    var1 = setFields_dic['boxToCell']['var']

    p1X = setFields_dic['cylinderToCell']['regions'][0]
    p1Y = setFields_dic['cylinderToCell']['regions'][1]
    p1Z = setFields_dic['cylinderToCell']['regions'][2]
    p2X = setFields_dic['cylinderToCell']['regions'][3]
    p2Y = setFields_dic['cylinderToCell']['regions'][4]
    p2Z = setFields_dic['cylinderToCell']['regions'][5]
    radius = setFields_dic['cylinderToCell']['radius']
    var2 = setFields_dic['cylinderToCell']['var']

    print(p1Y, file_['regions'][2])
    file_['regions'][1]['box'] = f"({minX} {minY} {minZ})  ({maxX} {maxY} {maxZ})"
    file_['regions'][1]['fieldValues'] = ['volScalarFieldValue', 'alpha.water', var1]
    file_['regions'][3]['p1'] = f"({p1X} {p1Y} {p1Z})"
    file_['regions'][3]['p2'] = f"({p2X} {p2Y} {p2Z})"
    file_['regions'][3]['radius'] = radius
    file_['regions'][3]['fieldValues'] = ['volScalarFieldValue', 'alpha.water', var2]
        # 
    file_.writeFile()
    print(file_['regions'])