from OpenFOAMlibs.mesh_condition import *
from os import path
import os
import shutil
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
import openpyxl
import glob

# ========== stlファイルから面の名前を取得  ==========
glob.glob('model/*.stl')
modelStlFileName_list_ = glob.glob('model/*.stl')
modelStlFilePathName = modelStlFileName_list_[0]
modelName = modelStlFilePathName.split('/')[1]
modelName_m = f"{modelName.split('.')[0]}_m.stl"
modelName_m_eMesh = f'{modelName.split(".")[0]}_m.eMesh'

def getSurfaceName():
    patch_list = []
    print(modelName_m)
    with open(f'constant/triSurface/{modelName}', 'r') as fi:
        for line in fi:
            if line[:5] == 'solid':
                patchName_ = line[6:].split('\n')[0]
                if len(patchName_.split('_'))>=3:
                    patch_list.append(patchName_)

    print('='*50)
    patch_list = sorted(patch_list, key=lambda x: x.split('_')[1])
    print('patch_list:', patch_list)
    print('='*50)

    return patch_list

def makeExcel_boundaryCondition(boundary_file):
    # 境界条件設定用のエクセル作成
    boundary_file = boundary_file
    excelCopy_yesOrno = input(f'{boundary_file}をコピーしますか？(yes/y or no/n)：')

    if excelCopy_yesOrno == 'yes' or excelCopy_yesOrno == 'y':
        base_case = '/mnt/c/work/001_CAE/openfoam'
        shutil.copy(path.join(base_case, boundary_file), './') # コピー
    

def setting_snappyHexMesh():
    PWD = os.getcwd() #現在のディレクトリパス
    snappyHexMeshParsedParameterFile = ParsedParameterFile(path.join(PWD, "system", 'snappyHexMeshDict'))
    print(snappyHexMeshParsedParameterFile['geometry'])
    if modelName_m != 'model_m.stl':
        snappyHexMeshParsedParameterFile['geometry'][modelName_m] = snappyHexMeshParsedParameterFile['geometry']['model_m.stl']
        del snappyHexMeshParsedParameterFile['geometry']['model_m.stl']
        snappyHexMeshParsedParameterFile.writeFile()
    # 特徴線の分割数を指定
    snappyHexMesh_castellatedMeshControlsFeatureExtract_func(snappyHexMeshParsedParameterFile, modelName_m_eMesh) # 分割数の設定

    return snappyHexMeshParsedParameterFile


def writeBoundarycondition_Excel(boundary_file, patch_list, vertexList, snappyHexMeshParsedParameterFile):
    # エクセルから境界条件の読み込み
    wb = openpyxl.load_workbook(boundary_file)
    for i, patch in enumerate(patch_list):
        try:
            patchName = patch
            patchType = patch.split('_')[1]
            levelList = patch.split('_')[2].split('-')
            addlayer = patch.split('_')[3]
            print('='*30)
            print(f'patchName:{patchName}')
            print(f'patchType:{patchType}')
            print(f'levelList:{levelList}')
            print(f'addlayer:{addlayer}')
            snappyHexMesh_geometryRegions_func(snappyHexMeshParsedParameterFile, modelName_m, patchName) #パッチ名の設定
            snappyHexMesh_castellatedMeshControls_func(snappyHexMeshParsedParameterFile, patchName,levelList, patchType) # 分割数の設定
            snappyHexMesh_addLayersControls_func(snappyHexMeshParsedParameterFile, patchName, addlayer) # 境界層の設定
            snappyHexMesh_location_func(snappyHexMeshParsedParameterFile, vertexList) # 内部領域の指定

            ws = wb['境界条件指定']
            ws.cell(row=i+2, column=2, value=patch)
            wb.save(boundary_file)
        except:
            print('='*30)
            print(f'patchName:{patchName}')
