import glob
import os
import shutil
import subprocess
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from os import path

def surfaceFeatureExtract():# 特徴線の抽出
    PWD = os.getcwd()
    file_surfaceFeatureExtract = ParsedParameterFile(path.join(PWD, "system", 'surfaceFeatureExtractDict'))

    modelStlFilePathName = glob.glob('constant/triSurface/*.stl')[0]
    modelName = modelStlFilePathName.split('/')[2]
    print(modelName)
    modelName_m = f"{modelName.split('.')[0]}_m.stl"
    
    # 特徴線の抽出
    print(f'modelName_m : {modelName_m}')
    if modelName_m != 'model_m.stl':
        file_surfaceFeatureExtract[modelName_m] = file_surfaceFeatureExtract['model_m.stl']
        del file_surfaceFeatureExtract['model_m.stl']
        print(file_surfaceFeatureExtract[modelName_m])
        file_surfaceFeatureExtract.writeFile()

    subprocess.run(['surfaceFeatureExtract'])
    subprocess.run(['surfaceFeatureConvert', f"constant/triSurface/{modelName_m.split('.')[0]}.eMesh", f"constant/triSurface/{modelName_m.split('.')[0]}.obj"])