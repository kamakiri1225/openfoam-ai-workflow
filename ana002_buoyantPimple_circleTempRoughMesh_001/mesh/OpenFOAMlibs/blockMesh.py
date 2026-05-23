from statistics import mode
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
import os
from os import path
import shutil
import glob
import subprocess

def vertexListFunc():
    # ========== stlファイルから面の名前を取得  ==========
    vertexX_list = []
    vertexY_list = []
    vertexZ_list = []

    modelStlFileName_list_ = glob.glob('constant/triSurface/*_m.stl')
    print(modelStlFileName_list_)
    modelStlFilePathName = modelStlFileName_list_[0]
    modelName_m = modelStlFilePathName.split('/')[2]
    print(modelName_m)

    with open(f'constant/triSurface/{modelName_m}', 'r') as fi:
        vertexX_list = [float(line.split()[1]) for line in fi if 'vertex' in line]
    with open(f'constant/triSurface/{modelName_m}', 'r') as fi:
        vertexY_list = [float(line.split()[2]) for line in fi if 'vertex' in line]
    with open(f'constant/triSurface/{modelName_m}', 'r') as fi:
        vertexZ_list = [float(line.split()[3]) for line in fi if 'vertex' in line]

    scaleValue = 1.0
    mergin = 0.01*scaleValue
    xMin = round(min(vertexX_list)*scaleValue - mergin,2)
    xMax = round(max(vertexX_list)*scaleValue + mergin,2)
    yMin = round(min(vertexY_list)*scaleValue - mergin,2)
    yMax = round(max(vertexY_list)*scaleValue + mergin,2)
    zMin = round(min(vertexZ_list)*scaleValue - mergin,2)
    zMax = round(max(vertexZ_list)*scaleValue + mergin,2)

    vertexList = [xMin, xMax, yMin, yMax, zMin, zMax]

    print(f'minX={xMin}')
    print(f'minY={xMax}')
    print(f'minZ={yMin}')
    print(f'maxX={yMax}')
    print(f'maxY={zMin}')
    print(f'maxZ={zMax}')

    return vertexList

def makeblockMesh(vertexList, meshsize_):
    PWD = os.getcwd()
    mesh_blockMeshDict = ParsedParameterFile(path.join(PWD, "system", 'blockMeshDict'))

    xMin = vertexList[0]
    xMax = vertexList[1]
    yMin = vertexList[2]
    yMax = vertexList[3]
    zMin = vertexList[4]
    zMax = vertexList[5]

    mesh_blockMeshDict['vertices'] = [
    [xMin, yMin, zMin],
    [xMax, yMin, zMin],
    [xMax, yMax, zMin],
    [xMin, yMax, zMin],
    [xMin, yMin, zMax],
    [xMax, yMin, zMax],
    [xMax, yMax, zMax],
    [xMin, yMax, zMax]
    ]

    meshsize = float(meshsize_)
    xn = int((xMax - xMin)*1000/meshsize)
    yn = int((yMax - yMin)*1000/meshsize)
    zn = int((zMax - zMin)*1000/meshsize)

    mesh_blockMeshDict['blocks'][2] = f'({xn} {yn} {zn})'
    mesh_blockMeshDict.writeFile()

    subprocess.run(['blockMesh'])
