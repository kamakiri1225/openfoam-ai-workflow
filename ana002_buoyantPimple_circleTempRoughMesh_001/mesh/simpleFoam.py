from OpenFOAMlibs import stlConvert, blockMesh, surfaceFeatureExtract, snappyHexMesh, controlDictSet, setFieldSets, boundary
from OpenFOAMlibs import subMeshConditon, subBoundaryCondition , subSetFields
from OpenFOAMlibs import fileCopy

boundary_file = "境界条件設定ファイル_ver1.1.xlsx"
print("メッシュ作成の手続きですか？")
print("yes/y : mesh setting file create")
print("no/n/other : boundaryCondition setting file create")
boundarySet_yesOrno = input("yes/y or no/n : ")

if boundarySet_yesOrno == 'yes' or boundarySet_yesOrno == 'y':
    meshsize_ = input("input meshsize(mm) : ")
    
    # stlFiel copy
    print(" ======  stlFiel Start ===========")
    stlConvert.copy_modelTotriSurface()
    stlConvert.modelScaleTrans()

    # blockMesh
    print(" ======  blockMesh Start ===========")
    fileCopy.copyBase_systemDict("system", "blockMeshDict")
    vertexList = blockMesh.vertexListFunc()
    blockMesh.makeblockMesh(vertexList, meshsize_)

    # surfaceFeatureExtract
    print(" ======  surfaceFeatureExtract Start ===========")
    fileCopy.copyBase_systemDict("system", "surfaceFeatureExtractDict")
    surfaceFeatureExtract.surfaceFeatureExtract()

    # snappyHexMesh
    print(" ======  snappyHexMesh Start ===========")
    fileCopy.copyBase_systemDict("system", "snappyHexMeshDict")
    patch_list = snappyHexMesh.getSurfaceName()
    snappyHexMesh.makeExcel_boundaryCondition(boundary_file)
    snappyHexMeshParsedParameterFile = snappyHexMesh.setting_snappyHexMesh()
    snappyHexMesh.writeBoundarycondition_Excel(boundary_file, patch_list, vertexList, snappyHexMeshParsedParameterFile)

    # setFieldDict
    # if setFieldSets.isSetField(boundary_file) is True:
    #     print(" ======  setFieldDict Start ===========")
    #     fileCopy.copyBase_systemDict("system", "setFieldsDict") 
    #     setFieldsParsedParameterFile = subSetFields.setting_setField()
    #     setFields_dic = setFieldSets.inputRegionDict(boundary_file)
    #     setFieldSets.createRegion(setFieldsParsedParameterFile, setFields_dic)

    # ControlDict
    print(" ======  ControlDict Start ===========")
    fileCopy.copyBase_systemDict("system", "controlDict")
    outputPatch_list = controlDictSet.patchList_otherWall(patch_list)
    controlDictSet.setting_ControlDict(outputPatch_list)

else:
    print(" ======  boundary Start ===========")
    fileCopy.copyBase_BoundaryCondition("0")
    boundary.setting_BoundaryCondition(boundary_file)