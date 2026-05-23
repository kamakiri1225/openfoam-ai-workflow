def snappyHexMesh_geometryRegions_func(file_, modelName_, patchName_): #パッチ名の設定
    file_['geometry'][modelName_]['regions'][patchName_] =  {'name': patchName_}
    file_.writeFile()

def snappyHexMesh_castellatedMeshControlsFeatureExtract_func(file_, modelName_m_eMesh_): # 分割数の設定
    # 特徴線分割数の指定
    file_['castellatedMeshControls']['features'][0]['file'] = modelName_m_eMesh_
    file_.writeFile()

def snappyHexMesh_castellatedMeshControls_func(file_, patchName_, levelList_, patchType_): # 分割数の設定
    # 表面分割数の指定
    if patchType_ == 'wall':
        file_['castellatedMeshControls']['refinementSurfaces']['model']['regions'][patchName_] = {'level': levelList_, 'patchInfo': {'type': patchType_}}
    else:
        file_['castellatedMeshControls']['refinementSurfaces']['model']['regions'][patchName_] = {'level': levelList_, 'patchInfo': {'type': 'patch'}}
    file_.writeFile()
    
def snappyHexMesh_addLayersControls_func(file_, patchName_, nSurfaceLayers_): # 境界層の設定
    file_['addLayersControls']['layers'][patchName_] = {'nSurfaceLayers': nSurfaceLayers_}
    file_.writeFile()

def snappyHexMesh_location_func(file_, vertexList_):
    print("===================",file_['castellatedMeshControls'])
    Xmin_puls = vertexList_[0] + 0.01 + 0.005
    ymin_puls = vertexList_[2] + 0.01 + 0.005
    zmin_puls = vertexList_[4] + 0.01 + 0.005
    print(f'(Xmin_puls, ymin_puls, zmin_puls)=({Xmin_puls}, {ymin_puls}, {zmin_puls})')
    file_['castellatedMeshControls']['locationInMesh'] = f'({Xmin_puls} {ymin_puls} {zmin_puls})'
    file_.writeFile()