
import shutil
import os

def copyBase_systemDict(dirctory, baseFile):
    # ========== パッチリストからメッシュ生成  ==========
    # baseからDictファイルをコピーする
    fileFile_list = os.listdir(f'{dirctory}/base')
    for file in fileFile_list:
        if file == baseFile:
            shutil.copy(f'{dirctory}/base/{file}', 'system')


def copyBase_BoundaryCondition(dirctory):
    # 0フィールドのコピー
    fileFile_list = os.listdir(f'{dirctory}/base')
    print(fileFile_list)
    for file in fileFile_list:
        shutil.copy(f'{dirctory}/base/{file}', '0')

def copyBase(dirctory, baseFile, copydirctory):
    # ========== パッチリストからメッシュ生成  ==========
    # baseからDictファイルをコピーする
    fileFile_list = os.listdir(f'{dirctory}')
    for file in fileFile_list:
        if file == baseFile:
            print(baseFile)
            shutil.copy(f'{dirctory}/{file}', f'{copydirctory}')