import glob
import os
import shutil
import subprocess
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from os import path

def copy_modelTotriSurface():
    PWD = os.getcwd()
    modelStlFileName_list_ = glob.glob('model/*.stl')
    # stlファイルをmodelからconstant/triSurfaceにコピー
    if len(modelStlFileName_list_) != 1:
        print(f'modelStlFileName_list_ : {modelStlFileName_list_}')
        print('stlファイルが複数あります。1つにしてください.')
    else:
        modelStlFilePathName = modelStlFileName_list_[0]
        modelName = modelStlFilePathName.split('/')[1]
        shutil.copy(modelStlFilePathName, 'constant/triSurface')
        print(f'{modelStlFilePathName}({modelName})をconstant/triSurfaceにコピーしました。')

def modelScaleTrans():
    modelStlFilePathName = glob.glob('constant/triSurface/*.stl')[0]
    modelName = modelStlFilePathName.split('/')[2]
    modelName_m = f"{modelName.split('.')[0]}_m.stl"
    print(modelName_m)
    # スケール変換(mm=>m)
    scaleConvert_yesOrno = input('スケール変換しますか?(yes/y or no/n):')
    if scaleConvert_yesOrno == 'yes' or scaleConvert_yesOrno == 'y':
        subprocess.run(['surfaceConvert','-scale', '0.001', f'constant/triSurface/{modelName}', f"constant/triSurface/{modelName_m}"])
    else:
        subprocess.run(['cp','-r', f'constant/triSurface/{modelName}', f"constant/triSurface/{modelName_m}"])
